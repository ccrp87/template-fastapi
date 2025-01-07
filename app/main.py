from sys import prefix
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.core.exceptions import setup_exception_handlers
from app.core.middlewares import setup_meddlewares_handlers
from app.db.session import init_db
from app.routers.users_router import routerUser
from app.routers.auth_router import routerAuth
from app.core.config_open_api import customize_openapi, doc_responses
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicialización
    print("Initializing database...")
    await init_db()  # Llama a tu función de inicialización de la base de datos
    yield  # Espera aquí mientras la aplicación está corriendo
    # Código de cierre
    print("Cleaning up resources...")
    

app = FastAPI(
    title="FastAPI Template",
    description="A template for FastAPI projects",
    version="1.0.0",
    lifespan=lifespan,
    responses=doc_responses,
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations related to users",
        },
    ],
)

app.openapi = customize_openapi(app.openapi)  # Customiza el esquema OpenAPI


# Configurar los manejadores de excepciones
setup_exception_handlers(app)

# Configurar los middlewares
setup_meddlewares_handlers(app)  # Configura el middleware de logs

# Include routers
prefix: str = "/api/v1"  # Prefix for all routes
app.include_router(router=routerUser, prefix=prefix, responses=doc_responses)
app.include_router(router=routerAuth, prefix=prefix, responses=doc_responses)

@app.get("/", tags=["Test"],responses={200: {"description": "Welcome message", "content": {"application/json": {"example": {"message": "Welcome to FastAPI Template"}}}}})
async def test_api():
    return {"message": "Welcome to FastAPI Template", "success": True,"date":datetime.now()}

