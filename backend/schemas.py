# schemas.py
# Esquemas Pydantic - Getsemani Vivo

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


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
# SCHEMAS DE USUARIO
# =============================================================================

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreateByAdmin(UserCreate):
    role: UserRole = UserRole.USER


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class UserUpdateRole(BaseModel):
    role: UserRole


class User(UserBase):
    id: int
    role: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserSimple(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    role: str
    
    class Config:
        from_attributes = True


# =============================================================================
# SCHEMAS DE IMAGEN
# =============================================================================

class BusinessImageBase(BaseModel):
    is_primary: Optional[bool] = False
    order: Optional[int] = 0


class BusinessImageCreate(BusinessImageBase):
    pass


class BusinessImage(BusinessImageBase):
    id: int
    filename: str
    url: str
    business_id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# =============================================================================
# SCHEMAS DE NEGOCIO
# =============================================================================

class BusinessBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: BusinessCategory = BusinessCategory.OTHER
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    schedule_monday: Optional[str] = None
    schedule_tuesday: Optional[str] = None
    schedule_wednesday: Optional[str] = None
    schedule_thursday: Optional[str] = None
    schedule_friday: Optional[str] = None
    schedule_saturday: Optional[str] = None
    schedule_sunday: Optional[str] = None


class BusinessCreate(BusinessBase):
    points_per_10000: Optional[int] = 1


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[BusinessCategory] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    schedule_monday: Optional[str] = None
    schedule_tuesday: Optional[str] = None
    schedule_wednesday: Optional[str] = None
    schedule_thursday: Optional[str] = None
    schedule_friday: Optional[str] = None
    schedule_saturday: Optional[str] = None
    schedule_sunday: Optional[str] = None
    points_per_10000: Optional[int] = None


class BusinessUpdateStatus(BaseModel):
    status: BusinessStatus


class Business(BusinessBase):
    id: int
    status: str
    is_featured: bool
    owner_id: int
    points_per_10000: int
    created_at: Optional[datetime] = None
    images: List[BusinessImage] = []
    
    class Config:
        from_attributes = True


class BusinessWithOwner(Business):
    owner: UserSimple
    
    class Config:
        from_attributes = True


class BusinessSimple(BaseModel):
    id: int
    name: str
    category: str
    address: str
    status: str
    is_featured: bool
    
    class Config:
        from_attributes = True


# =============================================================================
# SCHEMAS DE CONSUMO (PUNTOS)
# =============================================================================

class ConsumptionCreate(BaseModel):
    user_email: EmailStr
    amount: float
    description: Optional[str] = None


class ConsumptionResponse(BaseModel):
    id: int
    amount: float
    points_earned: int
    description: Optional[str] = None
    user_id: int
    business_id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ConsumptionWithDetails(BaseModel):
    id: int
    amount: float
    points_earned: int
    description: Optional[str] = None
    business_name: str
    business_category: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ConsumptionWithUser(BaseModel):
    id: int
    amount: float
    points_earned: int
    description: Optional[str] = None
    user_email: str
    user_name: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PointsSummary(BaseModel):
    business_id: int
    business_name: str
    total_points: int
    total_spent: float
    visit_count: int


class UserPointsSummary(BaseModel):
    total_points: int
    total_spent: float
    businesses_visited: int
    points_by_business: List[PointsSummary]


# =============================================================================
# SCHEMAS DE AUTENTICACION
# =============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# =============================================================================
# SCHEMAS DE RESPUESTA
# =============================================================================

class MessageResponse(BaseModel):
    message: str