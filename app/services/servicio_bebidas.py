"""
Servicio principal para manejo de bebidas con patrón Strategy integrado.
"""
import csv
from pathlib import Path
from typing import Dict, List, Optional
from app.models.beverage import Bebida
from app.strategies.estrategias_busqueda import EstrategiaBusquedaCompuesta, EstrategiaBusqueda
from app.strategies.estrategias_precio import ContextoEstrategiaPrecio, EstrategiaPrecioPremium
from app.strategies.estrategias_respuesta import ContextoFormateoRespuesta, EstrategiaRespuestaEstandar
from app.strategies.estrategias_sugerencia import ContextoSugerencia, EstrategiaSugerenciaHibrida


class ServicioBebidas:
    """Servicio principal para manejo de bebidas con estrategias configurables."""
    
    def __init__(self, ruta_csv: Path):
        self.ruta_csv = ruta_csv
        self.bebidas: List[Bebida] = []
        
        # Inicializar contextos de estrategias
        self.estrategia_busqueda = EstrategiaBusquedaCompuesta()
        self.contexto_precio = ContextoEstrategiaPrecio(EstrategiaPrecioPremium())
        self.contexto_respuesta = ContextoFormateoRespuesta(EstrategiaRespuestaEstandar())
        self.contexto_sugerencia = ContextoSugerencia(EstrategiaSugerenciaHibrida())
        
        # Cargar bebidas al inicializar
        self.cargar_bebidas()
    
    def establecer_estrategia_busqueda(self, estrategia: EstrategiaBusqueda):
        """Configura la estrategia de búsqueda."""
        self.estrategia_busqueda = estrategia
    
    def establecer_estrategia_precio(self, estrategia):
        """Configura la estrategia de estimación de precios."""
        self.contexto_precio.establecer_estrategia(estrategia)
    
    def establecer_estrategia_respuesta(self, estrategia):
        """Configura la estrategia de formateo de respuestas."""
        self.contexto_respuesta.establecer_estrategia(estrategia)
    
    def establecer_estrategia_sugerencia(self, estrategia):
        """Configura la estrategia de sugerencias."""
        self.contexto_sugerencia.establecer_estrategia(estrategia)
    
    def cargar_bebidas(self) -> None:
        """Carga las bebidas desde el archivo CSV."""
        if not self.ruta_csv.exists():
            raise FileNotFoundError(f"No se encontró el archivo CSV en: {self.ruta_csv}")
        
        ultimo_error: Optional[Exception] = None
        for codificacion in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                with self.ruta_csv.open("r", encoding=codificacion, newline="") as f:
                    # Detectar el separador del CSV
                    muestra = f.read(1024)
                    f.seek(0)
                    detector = csv.Sniffer()
                    delimitador = detector.sniff(muestra).delimiter
                    lector = csv.DictReader(f, delimiter=delimitador)
                    
                    if lector.fieldnames is None:
                        raise ValueError("El CSV no contiene encabezados (fila de columnas)")
                    
                    mapeo = self._adivinar_mapeo_columnas(lector.fieldnames)
                    requeridos = ["nombre", "metodo", "calorias", "grasa_total"]
                    faltantes = [k for k in requeridos if k not in mapeo]
                    
                    if faltantes:
                        raise ValueError(
                            "No se pudieron identificar las columnas requeridas en el CSV. "
                            f"Faltan: {', '.join(faltantes)}. Encabezados detectados: {lector.fieldnames}"
                        )
                    
                    self.bebidas = []
                    for fila in lector:
                        bebida = self._crear_bebida_desde_fila(fila, mapeo)
                        if bebida:
                            # Estimar precio si no existe
                            if bebida.precio is None:
                                bebida.precio = self.contexto_precio.estimar_precio(bebida)
                            self.bebidas.append(bebida)
                    
                    return
            except Exception as exc:
                ultimo_error = exc
                continue
        
        if ultimo_error:
            raise ultimo_error
    
    def buscar_bebida(self, consulta: str) -> Optional[Bebida]:
        """Busca una bebida usando la estrategia de búsqueda configurada."""
        return self.estrategia_busqueda.buscar(self.bebidas, consulta)
    
    def obtener_sugerencias(self, consulta: str = "", max_sugerencias: int = 10) -> List[Bebida]:
        """Obtiene sugerencias de bebidas."""
        if consulta:
            return self.contexto_sugerencia.generar_sugerencias(
                self.bebidas, consulta, max_sugerencias
            )
        else:
            # Devolver las más populares (por frecuencia)
            return self._obtener_sugerencias_principales(max_sugerencias)
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """Formatea la respuesta para una bebida encontrada."""
        return self.contexto_respuesta.formatear_respuesta_encontrada(bebida)
    
    def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
        """Formatea la respuesta para una bebida no encontrada."""
        return self.contexto_respuesta.formatear_respuesta_no_encontrada(consulta, sugerencias)
    
    def _adivinar_mapeo_columnas(self, encabezados) -> Dict[str, str]:
        """Adivina el mapeo de columnas del CSV."""
        normalizados = {h: self._normalizar_encabezado(h) for h in encabezados}
        
        def encontrar(candidatos: List[str]) -> Optional[str]:
            mejor_opcion: Optional[tuple] = None
            for original, normalizado in normalizados.items():
                for candidato in candidatos:
                    if normalizado == candidato:
                        puntuacion = 3
                    elif normalizado.startswith(candidato + " ") or normalizado.endswith(" " + candidato) or (" " + candidato + " ") in normalizado:
                        puntuacion = 2
                    elif candidato in normalizado:
                        puntuacion = 1
                    else:
                        continue
                    clave = (puntuacion, -len(normalizado), original)
                    if mejor_opcion is None or clave > mejor_opcion:
                        mejor_opcion = clave
            return mejor_opcion[2] if mejor_opcion else None
        
        # Mapeo para starbucks2.csv (formato español)
        columna_nombre = encontrar([
            "nombre bebida", "nombre de la bebida", "bebida", "nombre", "name es", "spanish name",
            "nombre espanol", "nombre en espanol", "nombre español", "nombre en español",
            "beverage es", "drink es", "nombre de la bebida en espanol", "nombre de la bebida en español",
        ])
        columna_metodo = encontrar([
            "tiempo de preparacion", "tiempo preparacion", "tiempo", "preparacion", "tiempo de preparación",
            "method", "preparation", "metodo de preparacion", "metodo", "preparacion",
            "metodo de preparación", "método de preparación", "beverage prep",
        ])
        columna_calorias = encontrar(["calories", "calorias", "calorias kcal", "calorias (kcal)", "caloria"])
        columna_grasa = encontrar(["grasa total", "total fat", "fat", "grasa", "total fat g"])
        columna_precio = encontrar(["price", "precio", "price usd", "precio usd", "precio (usd)", "price ($)"])
        columna_descripcion = encontrar(["descripcion", "description", "descripción"])
        columna_imagen = encontrar(["imagen", "image", "image url", "url imagen", "imagen url"])
        
        mapeo = {}
        if columna_nombre:
            mapeo["nombre"] = columna_nombre
        if columna_metodo:
            mapeo["metodo"] = columna_metodo
        if columna_calorias:
            mapeo["calorias"] = columna_calorias
        if columna_grasa:
            mapeo["grasa_total"] = columna_grasa
        if columna_precio:
            mapeo["precio"] = columna_precio
        if columna_descripcion:
            mapeo["descripcion"] = columna_descripcion
        if columna_imagen:
            mapeo["url_imagen"] = columna_imagen
        
        return mapeo
    
    def _normalizar_encabezado(self, encabezado: str) -> str:
        """Normaliza encabezados de CSV."""
        clave = encabezado.strip().lower()
        reemplazos = {
            "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n",
        }
        for origen, destino in reemplazos.items():
            clave = clave.replace(origen, destino)
        clave = clave.replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ")
        clave = clave.replace("-", " ").replace("/", " ").replace(".", " ").replace("_", " ")
        clave = " ".join(clave.split())
        return clave
    
    def _crear_bebida_desde_fila(self, fila: dict, mapeo: dict) -> Optional[Bebida]:
        """Crea una bebida desde una fila del CSV."""
        nombre = (fila.get(mapeo["nombre"], "") or "").strip()
        metodo = (fila.get(mapeo["metodo"], "") or "").strip()
        calorias = self._a_flotante(fila.get(mapeo["calorias"]))
        grasa_total = self._a_flotante(fila.get(mapeo["grasa_total"]))
        categoria = (fila.get(mapeo.get("categoria", ""), "") or "").strip() if mapeo.get("categoria") else None
        valor_precio = self._a_flotante(fila.get(mapeo.get("precio", ""))) if mapeo.get("precio") else None
        url_imagen = (fila.get(mapeo.get("url_imagen", ""), "") or "").strip() if mapeo.get("url_imagen") else None
        descripcion = (fila.get(mapeo.get("descripcion", ""), "") or "").strip() if mapeo.get("descripcion") else None
        
        if not nombre:
            return None
        
        return Bebida(
            nombre=nombre,
            metodo_preparacion=metodo,
            calorias=calorias,
            grasa_total=grasa_total,
            categoria=categoria,
            precio=valor_precio,
            url_imagen=url_imagen or None,
            descripcion=descripcion,
        )
    
    def _a_flotante(self, valor: str) -> Optional[float]:
        """Convierte string a float manejando diferentes formatos."""
        if valor is None:
            return None
        texto = str(valor).strip().lower()
        if not texto:
            return None
        
        # Remover unidades y símbolos de moneda
        for sufijo in ["kcal", "g", "cal", "grams", "gramos", "usd", "$"]:
            if texto.endswith(sufijo):
                texto = texto[: -len(sufijo)].strip()
        
        # Manejar formato decimal europeo
        if "," in texto and "." not in texto:
            texto = texto.replace(",", ".")
        elif "," in texto and "." in texto:
            pos_coma = texto.rfind(",")
            pos_punto = texto.rfind(".")
            if pos_coma > pos_punto:
                texto = texto.replace(".", "").replace(",", ".")
            else:
                texto = texto.replace(",", "")
        
        # Filtrar caracteres no numéricos
        filtrado = "".join(ch for ch in texto if (ch.isdigit() or ch == "." or ch == "-"))
        
        try:
            return float(filtrado) if filtrado else None
        except ValueError:
            return None
    
    def _obtener_sugerencias_principales(self, limite: int = 12) -> List[Bebida]:
        """Obtiene las sugerencias más populares."""
        conteos: Dict[str, int] = {}
        primera_vista: Dict[str, Bebida] = {}
        
        for bebida in self.bebidas:
            clave = bebida.nombre
            conteos[clave] = conteos.get(clave, 0) + 1
            if clave not in primera_vista:
                primera_vista[clave] = bebida
        
        claves_ordenadas = sorted(conteos.items(), key=lambda kv: kv[1], reverse=True)
        principales: List[Bebida] = []
        
        for (nombre, _conteo) in claves_ordenadas[:limite]:
            principales.append(primera_vista[nombre])
        
        return principales
