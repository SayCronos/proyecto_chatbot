#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos MySQL
"""
import pymysql
import sys

def test_mysql_connection():
    """Prueba la conexión directa a MySQL"""
    try:
        print("🔍 Probando conexión a MySQL...")
        
        # Configuración de conexión
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',  # Sin contraseña por defecto en XAMPP
            database='starbucks',
            charset='utf8mb4'
        )
        
        print("✅ Conexión exitosa a MySQL!")
        
        # Probar una consulta simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 Versión de MySQL: {version[0]}")
            
            # Verificar que la tabla pedido existe
            cursor.execute("SHOW TABLES LIKE 'pedido'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                print("✅ Tabla 'pedido' encontrada")
                
                # Mostrar estructura de la tabla
                cursor.execute("DESCRIBE pedido")
                columns = cursor.fetchall()
                print("📋 Estructura de la tabla 'pedido':")
                for column in columns:
                    print(f"   - {column[0]}: {column[1]}")
                    
                # Contar registros existentes
                cursor.execute("SELECT COUNT(*) FROM pedido")
                count = cursor.fetchone()
                print(f"📈 Registros existentes: {count[0]}")
                
            else:
                print("❌ Tabla 'pedido' no encontrada")
                print("🔧 Creando tabla 'pedido'...")
                
                create_table_sql = """
                CREATE TABLE pedido (
                    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_usuario VARCHAR(100) NOT NULL,
                    direccion VARCHAR(100) NOT NULL,
                    telefono INT NOT NULL,
                    nombre_bebida VARCHAR(100),
                    precio FLOAT,
                    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_sql)
                print("✅ Tabla 'pedido' creada exitosamente")
        
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error de MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def test_sqlalchemy_connection():
    """Prueba la conexión usando SQLAlchemy"""
    try:
        print("\n🔍 Probando conexión con SQLAlchemy...")
        
        from app.database.config import engine, test_connection
        
        if test_connection():
            print("✅ SQLAlchemy conectado exitosamente")
            return True
        else:
            print("❌ Error con SQLAlchemy")
            return False
            
    except Exception as e:
        print(f"❌ Error con SQLAlchemy: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de conexión a base de datos...\n")
    
    # Probar conexión directa
    mysql_ok = test_mysql_connection()
    
    # Probar conexión con SQLAlchemy
    sqlalchemy_ok = test_sqlalchemy_connection()
    
    print(f"\n📊 Resultados:")
    print(f"   MySQL directo: {'✅' if mysql_ok else '❌'}")
    print(f"   SQLAlchemy: {'✅' if sqlalchemy_ok else '❌'}")
    
    if mysql_ok and sqlalchemy_ok:
        print("\n🎉 ¡Todas las conexiones funcionan correctamente!")
        sys.exit(0)
    else:
        print("\n⚠️  Hay problemas de conexión. Verifica que:")
        print("   1. XAMPP esté ejecutándose")
        print("   2. MySQL esté activo en el puerto 3306")
        print("   3. La base de datos 'starbucks' exista")
        print("   4. La tabla 'pedido' tenga la estructura correcta")
        sys.exit(1)
