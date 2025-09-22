"""
Pruebas unitarias para las implementaciones del patrón Strategy.
"""
import pytest
from typing import List
from app.models.beverage import Bebida
from app.strategies.estrategias_busqueda import (
    EstrategiaCoincidenciaExacta, EstrategiaSolapamientoTokens, 
    EstrategiaBusquedaDifusa, EstrategiaBusquedaCompuesta
)
from app.strategies.estrategias_precio import (
    EstrategiaPrecioBasico, EstrategiaPrecioPorFamilia, EstrategiaPrecioPremium
)
from app.strategies.estrategias_respuesta import (
    EstrategiaRespuestaEstandar, EstrategiaRespuestaDetallada, EstrategiaRespuestaCompacta
)
from app.strategies.estrategias_sugerencia import (
    EstrategiaSugerenciaPorSimilitud, EstrategiaSugerenciaPorCategoria, 
    EstrategiaSugerenciaPorPopularidad, EstrategiaSugerenciaHibrida
)


class TestEstrategiasBusqueda:
    """Casos de prueba para las estrategias de búsqueda."""
    
    @pytest.fixture
    def bebidas_muestra(self) -> List[Bebida]:
        """Bebidas de muestra para las pruebas."""
        return [
            Bebida(
                nombre="Café con Leche",
                metodo_preparacion="Espresso con leche vaporizada",
                calorias=190.0,
                grasa_total=7.0,
                categoria="Café",
                precio=4.50
            ),
            Bebida(
                nombre="Capuchino",
                metodo_preparacion="Espresso con espuma de leche",
                calorias=120.0,
                grasa_total=4.0,
                categoria="Café",
                precio=4.25
            ),
            Bebida(
                nombre="Té Verde con Leche",
                metodo_preparacion="Matcha con leche vaporizada",
                calorias=240.0,
                grasa_total=7.0,
                categoria="Té",
                precio=5.25
            )
        ]
    
    def test_estrategia_coincidencia_exacta(self, bebidas_muestra):
        """Prueba la estrategia de búsqueda por coincidencia exacta."""
        estrategia = EstrategiaCoincidenciaExacta()
        
        # Prueba coincidencia exacta
        resultado = estrategia.buscar(bebidas_muestra, "Café con Leche")
        assert resultado is not None
        assert resultado.nombre == "Café con Leche"
        
        # Prueba coincidencia exacta con acentos
        resultado = estrategia.buscar(bebidas_muestra, "Capuchino")
        assert resultado is not None
        assert resultado.nombre == "Capuchino"
        
        # Prueba sin coincidencia
        resultado = estrategia.buscar(bebidas_muestra, "Bebida Inexistente")
        assert resultado is None
    
    def test_estrategia_solapamiento_tokens(self, bebidas_muestra):
        """Prueba la estrategia de búsqueda por solapamiento de tokens."""
        estrategia = EstrategiaSolapamientoTokens()
        
        # Prueba coincidencia parcial
        resultado = estrategia.buscar(bebidas_muestra, "Café")
        assert resultado is not None
        assert "Café" in resultado.nombre
        
        # Prueba múltiples tokens
        resultado = estrategia.buscar(bebidas_muestra, "Té Verde")
        assert resultado is not None
        assert resultado.nombre == "Té Verde con Leche"
    
    def test_estrategia_busqueda_difusa(self, bebidas_muestra):
        """Prueba la estrategia de búsqueda difusa."""
        estrategia = EstrategiaBusquedaDifusa(umbral=0.6)
        
        # Prueba coincidencia difusa con error tipográfico
        resultado = estrategia.buscar(bebidas_muestra, "Capucino")  # Falta 'h'
        assert resultado is not None
        assert resultado.nombre == "Capuchino"
        
        # Prueba coincidencia difusa
        resultado = estrategia.buscar(bebidas_muestra, "Cafe con Leche")  # Sin acento
        assert resultado is not None
        assert resultado.nombre == "Café con Leche"
    
    def test_estrategia_busqueda_compuesta(self, bebidas_muestra):
        """Prueba la estrategia de búsqueda compuesta."""
        estrategia = EstrategiaBusquedaCompuesta()
        
        # Debe encontrar coincidencias exactas primero
        resultado = estrategia.buscar(bebidas_muestra, "Capuchino")
        assert resultado is not None
        assert resultado.nombre == "Capuchino"
        
        # Debe recurrir a búsqueda difusa
        resultado = estrategia.buscar(bebidas_muestra, "Capucino")
        assert resultado is not None
        assert resultado.nombre == "Capuchino"


class TestEstrategiasPrecio:
    """Casos de prueba para las estrategias de estimación de precios."""
    
    @pytest.fixture
    def bebida_muestra(self) -> Bebida:
        """Bebida de muestra para las pruebas."""
        return Bebida(
            nombre="Café con Leche",
            metodo_preparacion="Grande",
            calorias=190.0,
            grasa_total=7.0,
            categoria="Café"
        )
    
    def test_estrategia_precio_basico(self, bebida_muestra):
        """Prueba la estrategia de estimación de precio básico."""
        estrategia = EstrategiaPrecioBasico()
        precio = estrategia.estimar_precio(bebida_muestra)
        assert isinstance(precio, float)
        assert precio > 0
    
    def test_estrategia_precio_por_familia(self, bebida_muestra):
        """Prueba la estrategia de estimación de precio por familia."""
        estrategia = EstrategiaPrecioPorFamilia()
        precio = estrategia.estimar_precio(bebida_muestra)
        assert isinstance(precio, float)
        assert precio > 0
    
    def test_estrategia_precio_premium(self, bebida_muestra):
        """Prueba la estrategia de estimación de precio premium."""
        estrategia = EstrategiaPrecioPremium()
        precio = estrategia.estimar_precio(bebida_muestra)
        assert isinstance(precio, float)
        assert precio > 0


class TestEstrategiasRespuesta:
    """Casos de prueba para las estrategias de formateo de respuesta."""
    
    @pytest.fixture
    def bebida_muestra(self) -> Bebida:
        """Bebida de muestra para las pruebas."""
        return Bebida(
            nombre="Café con Leche",
            metodo_preparacion="Espresso con leche vaporizada",
            calorias=190.0,
            grasa_total=7.0,
            categoria="Café",
            precio=4.50,
            descripcion="Una bebida clásica de café"
        )
    
    @pytest.fixture
    def sugerencias_muestra(self) -> List[Bebida]:
        """Sugerencias de muestra para las pruebas."""
        return [
            Bebida(
                nombre="Capuchino",
                metodo_preparacion="Espresso con espuma de leche",
                calorias=120.0,
                grasa_total=4.0,
                precio=4.25
            )
        ]
    
    def test_estrategia_respuesta_estandar(self, bebida_muestra, sugerencias_muestra):
        """Prueba la estrategia de formateo de respuesta estándar."""
        estrategia = EstrategiaRespuestaEstandar()
        
        # Prueba respuesta encontrada
        respuesta = estrategia.formatear_respuesta_encontrada(bebida_muestra)
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0
        assert "Café con Leche" in respuesta
        
        # Prueba respuesta no encontrada
        respuesta = estrategia.formatear_respuesta_no_encontrada("consulta prueba", sugerencias_muestra)
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0
    
    def test_estrategia_respuesta_detallada(self, bebida_muestra, sugerencias_muestra):
        """Prueba la estrategia de formateo de respuesta detallada."""
        estrategia = EstrategiaRespuestaDetallada()
        
        # Prueba respuesta encontrada
        respuesta = estrategia.formatear_respuesta_encontrada(bebida_muestra)
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0
        assert "Café con Leche" in respuesta
    
    def test_estrategia_respuesta_compacta(self, bebida_muestra, sugerencias_muestra):
        """Prueba la estrategia de formateo de respuesta compacta."""
        estrategia = EstrategiaRespuestaCompacta()
        
        # Prueba respuesta encontrada
        respuesta = estrategia.formatear_respuesta_encontrada(bebida_muestra)
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0


class TestEstrategiasSugerencia:
    """Casos de prueba para las estrategias de sugerencias."""
    
    @pytest.fixture
    def bebidas_muestra(self) -> List[Bebida]:
        """Bebidas de muestra para las pruebas."""
        return [
            Bebida(
                nombre="Café con Leche",
                metodo_preparacion="Espresso con leche vaporizada",
                calorias=190.0,
                grasa_total=7.0,
                categoria="Café",
                precio=4.50
            ),
            Bebida(
                nombre="Capuchino",
                metodo_preparacion="Espresso con espuma de leche",
                calorias=120.0,
                grasa_total=4.0,
                categoria="Café",
                precio=4.25
            ),
            Bebida(
                nombre="Té Verde con Leche",
                metodo_preparacion="Matcha con leche vaporizada",
                calorias=240.0,
                grasa_total=7.0,
                categoria="Té",
                precio=5.25
            )
        ]
    
    def test_estrategia_sugerencia_por_similitud(self, bebidas_muestra):
        """Prueba la estrategia de sugerencias por similitud."""
        estrategia = EstrategiaSugerenciaPorSimilitud()
        sugerencias = estrategia.generar_sugerencias(bebidas_muestra, "café", 2)
        assert isinstance(sugerencias, list)
        assert len(sugerencias) <= 2
    
    def test_estrategia_sugerencia_por_categoria(self, bebidas_muestra):
        """Prueba la estrategia de sugerencias por categoría."""
        estrategia = EstrategiaSugerenciaPorCategoria()
        sugerencias = estrategia.generar_sugerencias(bebidas_muestra, "café", 2)
        assert isinstance(sugerencias, list)
        assert len(sugerencias) <= 2
    
    def test_estrategia_sugerencia_por_popularidad(self, bebidas_muestra):
        """Prueba la estrategia de sugerencias por popularidad."""
        estrategia = EstrategiaSugerenciaPorPopularidad()
        sugerencias = estrategia.generar_sugerencias(bebidas_muestra, "café", 2)
        assert isinstance(sugerencias, list)
        assert len(sugerencias) <= 2
    
    def test_estrategia_sugerencia_hibrida(self, bebidas_muestra):
        """Prueba la estrategia de sugerencias híbrida."""
        estrategia = EstrategiaSugerenciaHibrida()
        sugerencias = estrategia.generar_sugerencias(bebidas_muestra, "café", 2)
        assert isinstance(sugerencias, list)
        assert len(sugerencias) <= 2
        assert all(isinstance(b, Bebida) for b in sugerencias)
