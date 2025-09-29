# 🌐 Configuración de Acceso de Red Local - FastAPI

Esta guía te ayuda a configurar tu aplicación FastAPI para que sea accesible desde otros dispositivos en tu red local (Wi-Fi).

## 🚀 Inicio Rápido

### 1. Configuración Automática (Recomendado)

**Windows:**
```powershell
# Ejecutar como Administrador
PowerShell -ExecutionPolicy Bypass -File setup_network_access.ps1
```

**Linux:**
```bash
chmod +x setup_network_access.sh
sudo ./setup_network_access.sh
```

### 2. Configuración Manual

#### Paso 1: Iniciar el servidor en todas las interfaces
```bash
# En lugar de 127.0.0.1, usar 0.0.0.0
python main_refactored.py --serve --host 0.0.0.0 --port 8000
```

#### Paso 2: Obtener tu IP local

**Windows:**
```cmd
ipconfig | findstr "IPv4"
```

**Linux/macOS:**
```bash
ip addr show | grep "inet " | grep -v "127.0.0.1"
# o
hostname -I
```

#### Paso 3: Configurar el firewall

**Windows (PowerShell como Administrador):**
```powershell
New-NetFirewallRule -DisplayName "FastAPI Port 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

**Linux:**
```bash
sudo ufw allow 8000
```

#### Paso 4: Acceder desde otro dispositivo
1. Conecta el dispositivo a la misma red Wi-Fi
2. Abre un navegador
3. Ve a: `http://[TU_IP_LOCAL]:8000`

## 📋 Ejemplos de Uso

### Usando tu aplicación principal
```bash
# Acceso de red local
python main_refactored.py --serve --host 0.0.0.0 --port 8000

# Solo acceso local
python main_refactored.py --serve --host 127.0.0.1 --port 8000
```

### Usando el ejemplo de red
```bash
# Solo acceso local (por defecto)
python network_example.py

# Acceso de red local
uvicorn network_example:app --host 0.0.0.0 --port 8000
```

### Usando uvicorn directamente
```bash
# Con tu aplicación
uvicorn main_refactored:app --host 0.0.0.0 --port 8000

# Con recarga automática (desarrollo)
uvicorn main_refactored:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Configuración con Variables de Entorno

Crea un archivo `.env`:
```env
# Para acceso de red local
HOST=0.0.0.0
PORT=8000

# Para acceso solo local
# HOST=127.0.0.1
# PORT=8000
```

## 📱 Acceso desde Dispositivos Móviles

### iPhone/iPad:
1. Conectar a la misma red Wi-Fi
2. Abrir Safari
3. Ir a: `http://192.168.1.100:8000` (reemplazar con tu IP)

### Android:
1. Conectar a la misma red Wi-Fi
2. Abrir Chrome
3. Ir a: `http://192.168.1.100:8000` (reemplazar con tu IP)

### Computadora en la red:
1. Conectar a la misma red Wi-Fi/Ethernet
2. Abrir cualquier navegador
3. Ir a: `http://192.168.1.100:8000` (reemplazar con tu IP)

## 🔍 Verificación y Troubleshooting

### Verificar que el servidor esté corriendo:
```bash
# Windows
netstat -an | findstr :8000

# Linux/macOS
netstat -an | grep :8000
ss -tuln | grep :8000
```

### Verificar conectividad:
```bash
# Ping a la computadora servidor
ping 192.168.1.100

# Verificar puerto específico (Linux/macOS)
telnet 192.168.1.100 8000
```

### Problemas comunes:

1. **"Connection refused"**
   - ✅ Verificar que el servidor use `host="0.0.0.0"`
   - ✅ Verificar configuración del firewall

2. **"Timeout"**
   - ✅ Verificar que ambos dispositivos estén en la misma red
   - ✅ Verificar configuración del router

3. **"Can't reach this page"**
   - ✅ Verificar la IP local correcta
   - ✅ Verificar que el puerto 8000 esté abierto

## 🛡️ Consideraciones de Seguridad

⚠️ **IMPORTANTE**: Al exponer tu aplicación en la red local:

- ✅ **Solo en redes confiables**: Úsalo solo en tu red doméstica o de oficina
- ✅ **Firewall**: Mantén el firewall habilitado
- ✅ **Puertos**: Solo abre los puertos necesarios
- ✅ **Monitoreo**: Supervisa los logs de acceso
- ⚠️ **Autenticación**: Considera agregar autenticación para datos sensibles
- ⚠️ **HTTPS**: Para producción, usa HTTPS en lugar de HTTP

## 📊 Comandos de Referencia Rápida

```bash
# Obtener IP local
# Windows: ipconfig | findstr "IPv4"
# Linux: hostname -I

# Iniciar servidor de red
python main_refactored.py --serve --host 0.0.0.0 --port 8000

# Configurar firewall
# Windows: New-NetFirewallRule -DisplayName "FastAPI Port 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
# Linux: sudo ufw allow 8000

# Verificar puerto
# Windows: netstat -an | findstr :8000
# Linux: ss -tuln | grep :8000
```

## 🎯 URLs de Ejemplo

Si tu IP local es `192.168.1.100`:

- **Aplicación principal**: `http://192.168.1.100:8000`
- **Documentación API**: `http://192.168.1.100:8000/docs`
- **API interactiva**: `http://192.168.1.100:8000/redoc`
- **Ejemplo de red**: `http://192.168.1.100:8000` (si usas `network_example.py`)

## 📁 Archivos Incluidos

- `setup_network_access.ps1` - Script automático para Windows
- `setup_network_access.sh` - Script automático para Linux
- `network_example.py` - Ejemplo simple de FastAPI con acceso de red
- `NETWORK_ACCESS_GUIDE.md` - Guía completa detallada
- `.env.example` - Archivo de configuración de ejemplo

## 🆘 Soporte

Si tienes problemas:

1. Revisa la guía completa en `NETWORK_ACCESS_GUIDE.md`
2. Ejecuta el script de configuración automática
3. Verifica que el firewall permita el puerto 8000
4. Asegúrate de que ambos dispositivos estén en la misma red
5. Prueba con el ejemplo simple: `python network_example.py`
