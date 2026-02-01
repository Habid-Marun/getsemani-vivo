# models.py
# Modelos SQLAlchemy - Getsemani Vivo

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

from database import Base


# =============================================================================
# ENUMERACIONES
# =============================================================================

class UserRole(str, Enum):
    USER = "user"
    BUSINESS = "business"
    ADMIN = "admin"


class BusinessCategory(str, Enum):
    BAR = "bar"
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    HOSTEL = "hostel"
    HOTEL = "hotel"
    TOUR_GUIDE = "tour_guide"
    SHOP = "shop"
    ART_GALLERY = "art_gallery"
    RENTAL = "rental"
    OTHER = "other"


class BusinessStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


# =============================================================================
# MODELO DE USUARIO
# =============================================================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.USER.value, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    businesses = relationship("Business", back_populates="owner")
    consumptions = relationship("Consumption", back_populates="user", foreign_keys="Consumption.user_id")


# =============================================================================
# MODELO DE NEGOCIO
# =============================================================================

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informacion basica
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String, default=BusinessCategory.OTHER.value, nullable=False)
    
    # Contacto
    phone = Column(String(20), nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    
    # Ubicacion
    address = Column(String(200), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Horarios
    schedule_monday = Column(String(50), nullable=True)
    schedule_tuesday = Column(String(50), nullable=True)
    schedule_wednesday = Column(String(50), nullable=True)
    schedule_thursday = Column(String(50), nullable=True)
    schedule_friday = Column(String(50), nullable=True)
    schedule_saturday = Column(String(50), nullable=True)
    schedule_sunday = Column(String(50), nullable=True)
    
    # Configuracion de puntos
    points_per_10000 = Column(Integer, default=1)
    
    # Estado
    status = Column(String, default=BusinessStatus.PENDING.value, nullable=False)
    is_featured = Column(Boolean, default=False)
    
    # Relaciones
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="businesses")
    consumptions = relationship("Consumption", back_populates="business")
    images = relationship("BusinessImage", back_populates="business", cascade="all, delete-orphan")
    
    # Fechas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# =============================================================================
# MODELO DE IMAGEN DE NEGOCIO
# =============================================================================

class BusinessImage(Base):
    __tablename__ = "business_images"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Nombre del archivo guardado
    filename = Column(String(255), nullable=False)
    
    # URL relativa para acceder a la imagen
    url = Column(String(500), nullable=False)
    
    # Es la imagen principal del negocio?
    is_primary = Column(Boolean, default=False)
    
    # Orden de la imagen en la galeria
    order = Column(Integer, default=0)
    
    # Relacion con el negocio
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    business = relationship("Business", back_populates="images")
    
    # Fecha de subida
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# =============================================================================
# MODELO DE CONSUMO (PUNTOS)
# =============================================================================

class Consumption(Base):
    __tablename__ = "consumptions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Monto del consumo en COP
    amount = Column(Float, nullable=False)
    
    # Puntos generados
    points_earned = Column(Integer, nullable=False)
    
    # Descripcion opcional
    description = Column(String(200), nullable=True)
    
    # Relaciones
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="consumptions", foreign_keys=[user_id])
    
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    business = relationship("Business", back_populates="consumptions")
    
    # Quien registro el consumo
    registered_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Fecha
    created_at = Column(DateTime(timezone=True), server_default=func.now())