# Getsemaní Vivo API

API REST para la aplicación móvil del barrio Getsemaní, Cartagena de Indias.

## Descripción

Getsemaní Vivo es una plataforma que conecta a turistas y visitantes con los negocios locales del barrio Getsemaní. Los usuarios pueden:

- Descubrir negocios locales (bares, restaurantes, cafés, hostales, etc.)
- Acumular puntos por sus consumos
- Ver horarios, ubicación e imágenes de los negocios

## Tecnologías

- **Python 3.10+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos (desarrollo)
- **JWT** - Autenticación con tokens
- **Pydantic** - Validación de datos

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
.\venv\Scripts\Activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crear archivo `.env` con:
```env
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=sqlite:///./getsemani.db
APP_ENV=development
ALLOWED_ORIGINS=http://localhost:3000
```

### 6. Ejecutar el servidor
```bash
uvicorn main:app --reload
```

### 7. Abrir documentación

Ir a: http://127.0.0.1:8000/docs

## Estructura del Proyecto
```
backend/
├── main.py           # Endpoints de la API
├── database.py       # Configuración de base de datos
├── models.py         # Modelos SQLAlchemy (tablas)
├── schemas.py        # Schemas Pydantic (validación)
├── crud.py           # Operaciones de base de datos
├── auth.py           # Autenticación JWT
├── create_admin.py   # Script para crear admin
├── requirements.txt  # Dependencias
├── .env              # Variables de entorno
├── .gitignore        # Archivos ignorados por Git
├── uploads/          # Imágenes subidas
│   └── businesses/
└── getsemani.db      # Base de datos SQLite
```

## Endpoints Principales

### Públicos (sin autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Bienvenida |
| GET | `/health` | Estado de la API |
| POST | `/register` | Registrar usuario |
| POST | `/login` | Iniciar sesión |
| GET | `/businesses` | Listar negocios aprobados |
| GET | `/businesses/featured` | Negocios destacados |
| GET | `/businesses/{id}` | Detalle de negocio |
| GET | `/businesses/{id}/images` | Imágenes del negocio |

### Usuario autenticado

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users/me` | Mi perfil |
| PUT | `/users/me` | Actualizar perfil |
| GET | `/my-points` | Mis puntos |
| GET | `/my-points/history` | Historial de consumos |

### Dueño de negocio

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/my-businesses` | Mis negocios |
| POST | `/my-businesses` | Crear negocio |
| PUT | `/my-businesses/{id}` | Actualizar negocio |
| DELETE | `/my-businesses/{id}` | Eliminar negocio |
| POST | `/my-businesses/{id}/images` | Subir imagen |
| POST | `/my-businesses/{id}/consumptions` | Registrar consumo |
| GET | `/my-businesses/{id}/customers` | Ver clientes |

### Administrador

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/users` | Listar usuarios |
| PUT | `/admin/users/{id}/role` | Cambiar rol |
| PUT | `/admin/users/{id}/deactivate` | Desactivar usuario |
| GET | `/admin/businesses` | Listar negocios |
| GET | `/admin/businesses/pending` | Negocios pendientes |
| PUT | `/admin/businesses/{id}/status` | Aprobar/rechazar |
| PUT | `/admin/businesses/{id}/featured` | Destacar negocio |

## Roles

| Rol | Descripción |
|-----|-------------|
| `user` | Usuario normal, puede acumular puntos |
| `business` | Dueño de negocio, puede gestionar sus negocios |
| `admin` | Administrador, acceso total |

## Sistema de Puntos

- Por cada $10,000 COP gastados = 1 punto (configurable por negocio)
- El dueño del negocio registra el consumo con el email del cliente
- El cliente puede ver sus puntos acumulados por negocio

## Autor

Desarrollado para el barrio Getsemaní, Cartagena de Indias, Colombia.

## Licencia

Proyecto privado - Todos los derechos reservados.