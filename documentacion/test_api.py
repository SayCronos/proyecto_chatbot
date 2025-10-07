#!/usr/bin/env python3
"""
Script para probar las APIs de pedidos
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/pedidos"

def test_conexion():
    """Prueba el endpoint de conexión"""
    try:
        print("🔍 Probando conexión a la API...")
        response = requests.get(f"{BASE_URL}/test-conexion")
        
        if response.status_code == 200:
            print("✅ API de conexión funcionando")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Error en API: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando a API: {e}")
        return False

def test_registro_usuario():
    """Prueba el registro de usuario"""
    try:
        print("\n🔍 Probando registro de usuario...")
        
        datos_usuario = {
            "nombre": "Juan Pérez",
            "direccion": "Calle 123 #45-67, Bogotá",
            "celular": "3001234567"
        }
        
        response = requests.post(
            f"{BASE_URL}/registrar-usuario",
            json=datos_usuario,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print("✅ Usuario registrado exitosamente")
            print(f"   ID del pedido: {resultado.get('id_pedido')}")
            print(f"   Nombre: {resultado.get('nombre_usuario')}")
            print(f"   Dirección: {resultado.get('direccion')}")
            print(f"   Teléfono: {resultado.get('telefono')}")
            return resultado.get('id_pedido')
        else:
            print(f"❌ Error registrando usuario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return None

def test_crear_pedido():
    """Prueba la creación de un pedido completo"""
    try:
        print("\n🔍 Probando creación de pedido completo...")
        
        datos_pedido = {
            "nombre_usuario": "María García",
            "direccion": "Carrera 15 #30-45, Medellín",
            "telefono": "3109876543",
            "nombre_bebida": "Latte Grande",
            "precio": 8500.0
        }
        
        response = requests.post(
            f"{BASE_URL}/crear-pedido",
            json=datos_pedido,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print("✅ Pedido creado exitosamente")
            print(f"   ID del pedido: {resultado.get('id_pedido')}")
            print(f"   Bebida: {resultado.get('nombre_bebida')}")
            print(f"   Precio: ${resultado.get('precio')}")
            return resultado.get('id_pedido')
        else:
            print(f"❌ Error creando pedido: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en pedido: {e}")
        return None

def test_obtener_todos_pedidos():
    """Prueba obtener todos los pedidos"""
    try:
        print("\n🔍 Probando obtener todos los pedidos...")
        
        response = requests.get(f"{BASE_URL}/todos?limit=10")
        
        if response.status_code == 200:
            pedidos = response.json()
            print(f"✅ Se obtuvieron {len(pedidos)} pedidos")
            
            for i, pedido in enumerate(pedidos[:3], 1):  # Mostrar solo los primeros 3
                print(f"   {i}. {pedido.get('nombre_usuario')} - {pedido.get('nombre_bebida', 'Sin bebida')} - ${pedido.get('precio', 0)}")
            
            return len(pedidos)
        else:
            print(f"❌ Error obteniendo pedidos: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Error obteniendo pedidos: {e}")
        return 0

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de API de pedidos...\n")
    
    # Probar conexión
    conexion_ok = test_conexion()
    
    if not conexion_ok:
        print("❌ No se puede continuar sin conexión a la API")
        exit(1)
    
    # Probar registro de usuario
    id_usuario = test_registro_usuario()
    
    # Probar creación de pedido completo
    id_pedido = test_crear_pedido()
    
    # Probar obtener todos los pedidos
    total_pedidos = test_obtener_todos_pedidos()
    
    print(f"\n📊 Resumen de pruebas:")
    print(f"   Conexión API: {'✅' if conexion_ok else '❌'}")
    print(f"   Registro usuario: {'✅' if id_usuario else '❌'}")
    print(f"   Crear pedido: {'✅' if id_pedido else '❌'}")
    print(f"   Total pedidos en DB: {total_pedidos}")
    
    if conexion_ok and id_usuario and id_pedido:
        print("\n🎉 ¡Todas las APIs funcionan correctamente!")
        print("✅ La base de datos está lista para recibir pedidos desde el frontend")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
