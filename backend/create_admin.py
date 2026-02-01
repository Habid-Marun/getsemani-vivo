# create_admin.py
# Script para crear el primer administrador del sistema
# Ejecutar UNA SOLA VEZ con: python create_admin.py

from database import SessionLocal, engine
import models
from passlib.context import CryptContext

# Crear las tablas si no existen
models.Base.metadata.create_all(bind=engine)

# Configuración de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =============================================================================
# DATOS DEL ADMINISTRADOR (CAMBIA ESTOS VALORES)
# =============================================================================

ADMIN_EMAIL = "camilo22armundo@gmail.com"
ADMIN_PASSWORD = "jesusteamo0120"
ADMIN_NAME = "Camilo"

# =============================================================================
# CREAR EL ADMINISTRADOR
# =============================================================================

def create_first_admin():
    db = SessionLocal()
    
    try:
        # Verificar si ya existe
        existing = db.query(models.User).filter(
            models.User.email == ADMIN_EMAIL
        ).first()
        
        if existing:
            print(f"⚠️  Ya existe un usuario con el email: {ADMIN_EMAIL}")
            print(f"   Rol actual: {existing.role}")
            return
        
        # Crear el admin
        hashed_password = pwd_context.hash(ADMIN_PASSWORD)
        
        admin = models.User(
            email=ADMIN_EMAIL,
            hashed_password=hashed_password,
            role="admin",
            full_name=ADMIN_NAME,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        
        print("✅ Administrador creado exitosamente!")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Contraseña: {ADMIN_PASSWORD}")
        print(f"   Rol: admin")
        print("")
        print("⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
    finally:
        db.close()


if __name__ == "__main__":
    create_first_admin()