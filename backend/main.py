# main.py
# API Principal de Getsemani Vivo

import os
import uuid
from datetime import timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, Query, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, get_db
import models
import schemas
import crud
from auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    require_admin,
    require_business,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Cargar variables de entorno
load_dotenv()

# Crear tablas
models.Base.metadata.create_all(bind=engine)

# Crear app
app = FastAPI(
    title="Getsemani Vivo API",
    description="API para la aplicacion movil del barrio Getsemani, Cartagena",
    version="1.0.0"
)

# =============================================================================
# CONFIGURACION DE CORS
# =============================================================================

# Obtener origenes permitidos desde .env
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# En desarrollo, permitir todos los origenes
if os.getenv("APP_ENV") == "development":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# CONFIGURACION DE UPLOADS
# =============================================================================

UPLOAD_DIR = "uploads"
os.makedirs(f"{UPLOAD_DIR}/businesses", exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# =============================================================================
# ENDPOINTS PUBLICOS
# =============================================================================

@app.get("/", tags=["General"])
def read_root():
    return {
        "mensaje": "Bienvenido a Getsemani Vivo API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["General"])
def health_check():
    """Endpoint para verificar que la API esta funcionando"""
    return {"status": "ok", "message": "API funcionando correctamente"}


@app.post("/register", response_model=schemas.User, status_code=201, tags=["Autenticacion"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Este email ya esta registrado")
    return crud.create_user(db=db, user=user, role="user")


@app.post("/login", response_model=schemas.Token, tags=["Autenticacion"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email o contrasena incorrectos")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Cuenta desactivada")
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# =============================================================================
# ENDPOINTS PUBLICOS DE NEGOCIOS
# =============================================================================

@app.get("/businesses", response_model=List[schemas.BusinessSimple], tags=["Negocios - Publico"])
def list_businesses(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_businesses(db, skip=skip, limit=limit, category=category, only_approved=True)


@app.get("/businesses/featured", response_model=List[schemas.BusinessSimple], tags=["Negocios - Publico"])
def list_featured_businesses(db: Session = Depends(get_db)):
    return crud.get_featured_businesses(db)


@app.get("/businesses/{business_id}", response_model=schemas.Business, tags=["Negocios - Publico"])
def get_business(business_id: int, db: Session = Depends(get_db)):
    business = crud.get_business(db, business_id)
    if not business or business.status != "approved":
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return business


@app.get("/businesses/{business_id}/images", response_model=List[schemas.BusinessImage], tags=["Negocios - Publico"])
def get_business_images_public(business_id: int, db: Session = Depends(get_db)):
    business = crud.get_business(db, business_id)
    if not business or business.status != "approved":
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return crud.get_business_images(db, business_id)


# =============================================================================
# ENDPOINTS DE USUARIO
# =============================================================================

@app.get("/users/me", response_model=schemas.User, tags=["Usuarios"])
def get_my_profile(current_user = Depends(get_current_active_user)):
    return current_user


@app.put("/users/me", response_model=schemas.User, tags=["Usuarios"])
def update_my_profile(
    user_update: schemas.UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.update_user(db, current_user.id, user_update)


# =============================================================================
# ENDPOINTS DE MIS PUNTOS
# =============================================================================

@app.get("/my-points", response_model=schemas.UserPointsSummary, tags=["Mis Puntos"])
def get_my_points(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_points_summary(db, current_user.id)


@app.get("/my-points/history", response_model=List[schemas.ConsumptionWithDetails], tags=["Mis Puntos"])
def get_my_consumption_history(
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    consumptions = crud.get_user_consumptions(db, current_user.id, skip=skip, limit=limit)
    result = []
    for c in consumptions:
        result.append({
            "id": c.id,
            "amount": c.amount,
            "points_earned": c.points_earned,
            "description": c.description,
            "business_name": c.business.name,
            "business_category": c.business.category,
            "created_at": c.created_at
        })
    return result


# =============================================================================
# ENDPOINTS DE MIS NEGOCIOS
# =============================================================================

@app.get("/my-businesses", response_model=List[schemas.Business], tags=["Mis Negocios"])
def list_my_businesses(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.get_businesses_by_owner(db, current_user.id)


@app.post("/my-businesses", response_model=schemas.Business, status_code=201, tags=["Mis Negocios"])
def create_my_business(
    business: schemas.BusinessCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "user":
        crud.update_user_role(db, current_user.id, "business")
    return crud.create_business(db, business, current_user.id)


@app.put("/my-businesses/{business_id}", response_model=schemas.Business, tags=["Mis Negocios"])
def update_my_business(
    business_id: int,
    business_update: schemas.BusinessUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    return crud.update_business(db, business_id, business_update)


@app.delete("/my-businesses/{business_id}", response_model=schemas.MessageResponse, tags=["Mis Negocios"])
def delete_my_business(
    business_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    crud.delete_business(db, business_id)
    return {"message": "Negocio eliminado"}


# =============================================================================
# ENDPOINTS DE IMAGENES DE MIS NEGOCIOS
# =============================================================================

@app.post("/my-businesses/{business_id}/images", response_model=schemas.BusinessImage, tags=["Imagenes de Negocios"])
async def upload_business_image(
    business_id: int,
    file: UploadFile = File(...),
    is_primary: bool = False,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido. Use JPG, PNG o WEBP")
    
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="La imagen no puede superar 5MB")
    
    extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = f"{UPLOAD_DIR}/businesses/{unique_filename}"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    url = f"/uploads/businesses/{unique_filename}"
    db_image = crud.create_business_image(db, business_id, unique_filename, url, is_primary)
    
    return db_image


@app.get("/my-businesses/{business_id}/images", response_model=List[schemas.BusinessImage], tags=["Imagenes de Negocios"])
def get_my_business_images(
    business_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    return crud.get_business_images(db, business_id)


@app.delete("/my-businesses/{business_id}/images/{image_id}", response_model=schemas.MessageResponse, tags=["Imagenes de Negocios"])
def delete_business_image(
    business_id: int,
    image_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    
    image = crud.get_image(db, image_id)
    if not image or image.business_id != business_id:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    file_path = f"{UPLOAD_DIR}/businesses/{image.filename}"
    if os.path.exists(file_path):
        os.remove(file_path)
    
    crud.delete_image(db, image_id)
    return {"message": "Imagen eliminada"}


@app.put("/my-businesses/{business_id}/images/{image_id}/primary", response_model=schemas.BusinessImage, tags=["Imagenes de Negocios"])
def set_primary_image(
    business_id: int,
    image_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    
    image = crud.get_image(db, image_id)
    if not image or image.business_id != business_id:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    return crud.set_primary_image(db, image_id)


# =============================================================================
# ENDPOINTS DE GESTION DE PUNTOS
# =============================================================================

@app.post("/my-businesses/{business_id}/consumptions", response_model=schemas.ConsumptionResponse, tags=["Gestion de Puntos"])
def register_consumption(
    business_id: int,
    consumption: schemas.ConsumptionCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    if business.status != "approved":
        raise HTTPException(status_code=400, detail="El negocio no esta aprobado")
    
    client = crud.get_user_by_email(db, consumption.user_email)
    if not client:
        raise HTTPException(status_code=404, detail=f"No existe usuario con email: {consumption.user_email}")
    
    db_consumption = crud.create_consumption(
        db=db,
        user_id=client.id,
        business_id=business_id,
        amount=consumption.amount,
        registered_by_id=current_user.id,
        description=consumption.description
    )
    return db_consumption


@app.get("/my-businesses/{business_id}/consumptions", response_model=List[schemas.ConsumptionWithUser], tags=["Gestion de Puntos"])
def get_business_consumptions(
    business_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    consumptions = crud.get_business_consumptions(db, business_id, skip=skip, limit=limit)
    result = []
    for c in consumptions:
        result.append({
            "id": c.id,
            "amount": c.amount,
            "points_earned": c.points_earned,
            "description": c.description,
            "user_email": c.user.email,
            "user_name": c.user.full_name,
            "created_at": c.created_at
        })
    return result


@app.get("/my-businesses/{business_id}/customers", tags=["Gestion de Puntos"])
def get_business_customers(
    business_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    if business.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    customers = crud.get_business_customers(db, business_id)
    return [
        {
            "user_id": c.id,
            "email": c.email,
            "full_name": c.full_name,
            "total_points": c.total_points,
            "total_spent": c.total_spent,
            "visit_count": c.visit_count
        }
        for c in customers
    ]


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - USUARIOS
# =============================================================================

@app.get("/admin/users", response_model=List[schemas.UserSimple], tags=["Admin - Usuarios"])
def admin_list_users(skip: int = 0, limit: int = 100, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/admin/users/{user_id}", response_model=schemas.User, tags=["Admin - Usuarios"])
def admin_get_user(user_id: int, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@app.put("/admin/users/{user_id}/role", response_model=schemas.User, tags=["Admin - Usuarios"])
def admin_change_role(user_id: int, role_update: schemas.UserUpdateRole, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    user = crud.update_user_role(db, user_id, role_update.role.value)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@app.put("/admin/users/{user_id}/deactivate", response_model=schemas.MessageResponse, tags=["Admin - Usuarios"])
def admin_deactivate_user(user_id: int, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes desactivarte a ti mismo")
    user = crud.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": f"Usuario {user.email} desactivado"}


@app.put("/admin/users/{user_id}/activate", response_model=schemas.MessageResponse, tags=["Admin - Usuarios"])
def admin_activate_user(user_id: int, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    user = crud.activate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": f"Usuario {user.email} activado"}


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - NEGOCIOS
# =============================================================================

@app.get("/admin/businesses", response_model=List[schemas.BusinessWithOwner], tags=["Admin - Negocios"])
def admin_list_businesses(
    skip: int = 0, limit: int = 100,
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return crud.get_businesses(db, skip=skip, limit=limit, status=status, category=category)


@app.get("/admin/businesses/pending", response_model=List[schemas.BusinessWithOwner], tags=["Admin - Negocios"])
def admin_list_pending(current_user = Depends(require_admin), db: Session = Depends(get_db)):
    return crud.get_businesses(db, status="pending")


@app.put("/admin/businesses/{business_id}/status", response_model=schemas.Business, tags=["Admin - Negocios"])
def admin_change_status(business_id: int, status_update: schemas.BusinessUpdateStatus, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    business = crud.update_business_status(db, business_id, status_update.status.value)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return business


@app.put("/admin/businesses/{business_id}/featured", response_model=schemas.Business, tags=["Admin - Negocios"])
def admin_toggle_featured(business_id: int, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    business = crud.toggle_featured(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return business


@app.delete("/admin/businesses/{business_id}", response_model=schemas.MessageResponse, tags=["Admin - Negocios"])
def admin_delete_business(business_id: int, current_user = Depends(require_admin), db: Session = Depends(get_db)):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    crud.delete_business(db, business_id)
    return {"message": f"Negocio '{business.name}' eliminado"}