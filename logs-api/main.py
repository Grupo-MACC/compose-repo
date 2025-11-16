from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
import asyncio
from contextlib import asynccontextmanager

# Import de router
from router.logs_router import router

# Import servicio broker
from broker.logs_broker_service import consume_auth_events


# ===========================
# CONFIGURACIÓN FASTAPI
# ===========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Reemplazo de on_event(startup) con lifespan."""
    task = asyncio.create_task(consume_auth_events())
    yield
    task.cancel()


app = FastAPI(
    title="Factory Data API",
    description="API REST para consultar datos de InfluxDB (solo admin)",
    version="1.0.0",
#    lifespan=lifespan
)


# ===========================
# CORS
# ===========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================
# ENDPOINTS PÚBLICOS
# ===========================

@app.get("/")
async def root():
    return {
        "service": "Factory Data API",
        "version": "1.0.0",
        "note": "Todos los endpoints /logs requieren rol admin",
        "endpoints": {
            "errors": "/logs/errors",
            "monitoring": "/logs/monitoring",
            "debug": "/logs/debug",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ===========================
# REGISTRO DEL ROUTER /logs
# ===========================

app.include_router(router)


# ===========================
# EJECUCIÓN DIRECTA
# ===========================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)
