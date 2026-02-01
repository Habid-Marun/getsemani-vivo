# crud.py
# Operaciones CRUD - Getsemani Vivo

from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
from typing import Optional, List

import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =============================================================================
# OPERACIONES DE USUARIO
# =============================================================================

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_users_by_role(db: Session, role: str, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.role == role).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, role: str = "user"):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=role,
        full_name=user.full_name,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_role(db: Session, user_id: int, new_role: str):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.role = new_role
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return db_user


# =============================================================================
# OPERACIONES DE NEGOCIO
# =============================================================================

def get_business(db: Session, business_id: int):
    return db.query(models.Business).filter(models.Business.id == business_id).first()


def get_businesses(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category: Optional[str] = None,
    status: Optional[str] = None,
    only_approved: bool = False
):
    query = db.query(models.Business)
    
    if only_approved:
        query = query.filter(models.Business.status == "approved")
    elif status:
        query = query.filter(models.Business.status == status)
    
    if category:
        query = query.filter(models.Business.category == category)
    
    return query.offset(skip).limit(limit).all()


def get_businesses_by_owner(db: Session, owner_id: int):
    return db.query(models.Business).filter(models.Business.owner_id == owner_id).all()


def get_featured_businesses(db: Session, limit: int = 10):
    return db.query(models.Business).filter(
        models.Business.is_featured == True,
        models.Business.status == "approved"
    ).limit(limit).all()


def create_business(db: Session, business: schemas.BusinessCreate, owner_id: int):
    db_business = models.Business(
        name=business.name,
        description=business.description,
        category=business.category.value,
        phone=business.phone,
        email=business.email,
        website=business.website,
        instagram=business.instagram,
        address=business.address,
        latitude=business.latitude,
        longitude=business.longitude,
        schedule_monday=business.schedule_monday,
        schedule_tuesday=business.schedule_tuesday,
        schedule_wednesday=business.schedule_wednesday,
        schedule_thursday=business.schedule_thursday,
        schedule_friday=business.schedule_friday,
        schedule_saturday=business.schedule_saturday,
        schedule_sunday=business.schedule_sunday,
        points_per_10000=business.points_per_10000 or 1,
        owner_id=owner_id,
        status="pending"
    )
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def update_business(db: Session, business_id: int, business_update: schemas.BusinessUpdate):
    db_business = get_business(db, business_id)
    if not db_business:
        return None
    
    update_data = business_update.model_dump(exclude_unset=True)
    
    if 'category' in update_data and update_data['category']:
        update_data['category'] = update_data['category'].value
    
    for field, value in update_data.items():
        setattr(db_business, field, value)
    
    db.commit()
    db.refresh(db_business)
    return db_business


def update_business_status(db: Session, business_id: int, new_status: str):
    db_business = get_business(db, business_id)
    if not db_business:
        return None
    db_business.status = new_status
    db.commit()
    db.refresh(db_business)
    return db_business


def toggle_featured(db: Session, business_id: int):
    db_business = get_business(db, business_id)
    if not db_business:
        return None
    db_business.is_featured = not db_business.is_featured
    db.commit()
    db.refresh(db_business)
    return db_business


def delete_business(db: Session, business_id: int):
    db_business = get_business(db, business_id)
    if not db_business:
        return None
    db.delete(db_business)
    db.commit()
    return True


# =============================================================================
# OPERACIONES DE IMAGENES
# =============================================================================

def create_business_image(db: Session, business_id: int, filename: str, url: str, is_primary: bool = False):
    """Crea un registro de imagen para un negocio"""
    
    # Si es imagen primaria, quitar el flag de las otras
    if is_primary:
        db.query(models.BusinessImage).filter(
            models.BusinessImage.business_id == business_id,
            models.BusinessImage.is_primary == True
        ).update({"is_primary": False})
    
    # Obtener el orden mas alto actual
    max_order = db.query(func.max(models.BusinessImage.order)).filter(
        models.BusinessImage.business_id == business_id
    ).scalar() or 0
    
    db_image = models.BusinessImage(
        business_id=business_id,
        filename=filename,
        url=url,
        is_primary=is_primary,
        order=max_order + 1
    )
    
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_business_images(db: Session, business_id: int):
    """Obtiene todas las imagenes de un negocio"""
    return db.query(models.BusinessImage).filter(
        models.BusinessImage.business_id == business_id
    ).order_by(models.BusinessImage.order).all()


def get_image(db: Session, image_id: int):
    """Obtiene una imagen por ID"""
    return db.query(models.BusinessImage).filter(models.BusinessImage.id == image_id).first()


def delete_image(db: Session, image_id: int):
    """Elimina una imagen"""
    db_image = get_image(db, image_id)
    if not db_image:
        return None
    db.delete(db_image)
    db.commit()
    return True


def set_primary_image(db: Session, image_id: int):
    """Establece una imagen como principal"""
    db_image = get_image(db, image_id)
    if not db_image:
        return None
    
    # Quitar flag de las otras imagenes del mismo negocio
    db.query(models.BusinessImage).filter(
        models.BusinessImage.business_id == db_image.business_id,
        models.BusinessImage.is_primary == True
    ).update({"is_primary": False})
    
    # Establecer esta como principal
    db_image.is_primary = True
    db.commit()
    db.refresh(db_image)
    return db_image


# =============================================================================
# OPERACIONES DE CONSUMO (PUNTOS)
# =============================================================================

def create_consumption(
    db: Session,
    user_id: int,
    business_id: int,
    amount: float,
    registered_by_id: int,
    description: Optional[str] = None
):
    business = get_business(db, business_id)
    if not business:
        return None
    
    points_earned = int(amount / 10000) * business.points_per_10000
    
    db_consumption = models.Consumption(
        user_id=user_id,
        business_id=business_id,
        amount=amount,
        points_earned=points_earned,
        description=description,
        registered_by_id=registered_by_id
    )
    
    db.add(db_consumption)
    db.commit()
    db.refresh(db_consumption)
    
    return db_consumption


def get_user_consumptions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Consumption).filter(
        models.Consumption.user_id == user_id
    ).order_by(models.Consumption.created_at.desc()).offset(skip).limit(limit).all()


def get_business_consumptions(db: Session, business_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Consumption).filter(
        models.Consumption.business_id == business_id
    ).order_by(models.Consumption.created_at.desc()).offset(skip).limit(limit).all()


def get_user_points_summary(db: Session, user_id: int):
    results = db.query(
        models.Consumption.business_id,
        models.Business.name.label('business_name'),
        func.sum(models.Consumption.points_earned).label('total_points'),
        func.sum(models.Consumption.amount).label('total_spent'),
        func.count(models.Consumption.id).label('visit_count')
    ).join(
        models.Business, models.Consumption.business_id == models.Business.id
    ).filter(
        models.Consumption.user_id == user_id
    ).group_by(
        models.Consumption.business_id,
        models.Business.name
    ).all()
    
    points_by_business = []
    total_points = 0
    total_spent = 0
    
    for r in results:
        points_by_business.append({
            "business_id": r.business_id,
            "business_name": r.business_name,
            "total_points": r.total_points or 0,
            "total_spent": r.total_spent or 0,
            "visit_count": r.visit_count or 0
        })
        total_points += r.total_points or 0
        total_spent += r.total_spent or 0
    
    return {
        "total_points": total_points,
        "total_spent": total_spent,
        "businesses_visited": len(points_by_business),
        "points_by_business": points_by_business
    }


def get_business_customers(db: Session, business_id: int):
    results = db.query(
        models.User.id,
        models.User.email,
        models.User.full_name,
        func.sum(models.Consumption.points_earned).label('total_points'),
        func.sum(models.Consumption.amount).label('total_spent'),
        func.count(models.Consumption.id).label('visit_count')
    ).join(
        models.Consumption, models.User.id == models.Consumption.user_id
    ).filter(
        models.Consumption.business_id == business_id
    ).group_by(
        models.User.id,
        models.User.email,
        models.User.full_name
    ).order_by(
        func.sum(models.Consumption.points_earned).desc()
    ).all()
    
    return results