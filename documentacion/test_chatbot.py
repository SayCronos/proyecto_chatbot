#!/usr/bin/env python3
"""
Script para probar que todas las APIs del chatbot funcionen
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api_buscar():
    """Prueba la API de búsqueda"""
    try:
        print("🔍 Probando API de búsqueda...")
        
        data = {
            "consulta": "cappuccino",
            "idioma": "es"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/buscar",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Búsqueda exitosa - Encontrado: {result.get('encontrado')}")
            if result.get('sugerencias'):
                print(f"   Sugerencias: {len(result['sugerencias'])} bebidas")
            return True
        else:
            print(f"❌ Error en búsqueda: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return False

def test_api_sugerencias():
    """Prueba la API de sugerencias"""
    try:
        print("\n🔍 Probando API de sugerencias...")
        
        response = requests.get(f"{BASE_URL}/api/sugerencias?consulta=café&limite=3")
        
        if response.status_code == 200:
            result = response.json()
            elementos = result.get('elementos', [])
            print(f"✅ Sugerencias exitosas - {len(elementos)} bebidas")
            for i, bebida in enumerate(elementos[:2], 1):
                print(f"   {i}. {bebida.get('nombre_es')} - ${bebida.get('precio', 0)}")
            return True
        else:
            print(f"❌ Error en sugerencias: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en sugerencias: {e}")
        return False

def test_homepage():
    """Prueba que la página principal cargue"""
    try:
        print("\n🔍 Probando página principal...")
        
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            print("✅ Página principal carga correctamente")
            return True
        else:
            print(f"❌ Error cargando página: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error cargando página: {e}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        print("\n🔍 Probando conexión a base de datos...")
        
        response = requests.get(f"{BASE_URL}/api/pedidos/test-conexion")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Base de datos: {result.get('message')}")
            return True
        else:
            print(f"❌ Error en base de datos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas completas del chatbot...\n")
    
    # Ejecutar todas las pruebas
    tests = [
        ("Homepage", test_homepage),
        ("API Búsqueda", test_api_buscar),
        ("API Sugerencias", test_api_sugerencias),
        ("Base de Datos", test_database_connection)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Mostrar resumen
    print(f"\n📊 Resumen de pruebas:")
    all_passed = True
    for test_name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ¡Todas las pruebas pasaron! El chatbot está funcionando correctamente.")
        print("✅ Puedes usar la aplicación en: http://127.0.0.1:8000")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
