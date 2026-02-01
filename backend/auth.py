# auth.py
# Sistema de autenticación con JWT para Getsemaní Vivo

from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

SECRET_KEY = "tu_clave_secreta_muy_larga_y_segura_cambiar_en_produccion_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# =============================================================================
# CONFIGURACIÓN DE CONTRASEÑAS Y OAUTH2
# =============================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# =============================================================================
# FUNCIONES DE CONTRASEÑA
# =============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Convierte una contraseña a hash seguro"""
    return pwd_context.hash(password)

# =============================================================================
# FUNCIONES DE TOKEN JWT
# =============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# =============================================================================
# FUNCIONES DE AUTENTICACIÓN
# =============================================================================

def authenticate_user(db: Session, email: str, password: str):
    """Verifica las credenciales de un usuario"""
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

# =============================================================================
# DEPENDENCIAS DE SEGURIDAD
# =============================================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Obtiene el usuario actual a partir del token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    """Verifica que el usuario esté activo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

# =============================================================================
# VERIFICADORES DE ROL
# =============================================================================

def require_role(allowed_roles: List[str]):
    """
    Crea una dependencia que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
        @app.get("/admin-only")
        def admin_route(user = Depends(require_role(["admin"]))):
            ...
    """
    async def role_checker(current_user = Depends(get_current_active_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere rol: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


# Dependencias predefinidas para cada rol
require_admin = require_role(["admin"])
require_business = require_role(["admin", "business"])
require_user = require_role(["admin", "business", "user"])