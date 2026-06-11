from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from database import init_db
from endpoints import router

# Inicializar aplicación FastAPI
app = FastAPI(
    title="CRUD API REST - Sistema de Reservas de Salas",
    description="API para gestionar salas de conferencias con operaciones CRUD completas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Inicializar base de datos
init_db()

# Incluir rutas
app.include_router(router)


@app.get("/", tags=["root"])
def read_root():
    """
    Endpoint raíz para verificar que la API está funcionando
    """
    return {
        "mensaje": "Bienvenido a la API de Reservas de Salas",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Verificar el estado de salud de la API
    """
    return {
        "status": "healthy",
        "message": "La API está funcionando correctamente"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
