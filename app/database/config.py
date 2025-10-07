# Configuración de la base de datos MySQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

# Configuración de la conexión a MySQL (XAMPP)
# Formato: mysql+pymysql://usuario:contraseña@host:puerto/base_de_datos
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/starbucks?charset=utf8mb4"

# Crear el engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Para ver las consultas SQL en los logs
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300  # Reciclar conexiones cada 5 minutos
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para probar la conexión
def test_connection():
    try:
        from sqlalchemy import text
        connection = engine.connect()
        result = connection.execute(text("SELECT 1"))
        connection.close()
        print("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False
