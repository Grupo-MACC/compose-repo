from fastapi import APIRouter, HTTPException, Query, Depends, Header
from influxdb_client import InfluxDBClient
from typing import Optional
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import jwt
import os

router = APIRouter(prefix="/logs", tags=["logs"])


# ===========================
# CONFIGURACIÓN GLOBAL
# ===========================

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "https://auth:5004")
PUBLIC_KEY_PATH = "/app/public_key.pem"

INFLUX_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUXDB_TOKEN", "MY_CUSTOM_TOKEN_123456")
INFLUX_ORG = os.getenv("INFLUXDB_ORG", "my-org")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()


# ===========================
# TOKEN & KEY
# ===========================

def load_public_key():
    if not os.path.exists(PUBLIC_KEY_PATH):
        raise HTTPException(status_code=500, detail="Clave pública no disponible")

    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key_pem = f.read()

    try:
        return load_pem_public_key(public_key_pem)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar clave pública: {str(e)}")


async def verify_admin(authorization: str = Header(None)):
    """Verifica token con rol admin (role_id = 1)."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autorización requerido")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato inválido. Use: Bearer <token>")

    token = authorization.replace("Bearer ", "")

    try:
        public_key = load_public_key()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

        if payload.get("role_id") != 1:
            raise HTTPException(status_code=403, detail="Se requiere rol admin.")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando token: {str(e)}")


# ===========================
# ENDPOINTS
# ===========================

@router.get("/errors")
async def get_errors(
    start: str = Query("-1h"),
    stop: str = Query("now()"),
    limit: int = Query(100, ge=1, le=1000),
    service: Optional[str] = None,
    severity: Optional[str] = None,
#    current_user: dict = Depends(verify_admin)
):
    try:
        filters = []
        if service:
            filters.append(f'|> filter(fn: (r) => r["service"] == "{service}")')
        if severity:
            filters.append(f'|> filter(fn: (r) => r["severity"] == "{severity}")')

        filter_str = "\n  ".join(filters)

        query = f'''
        from(bucket: "factory_errors")
          |> range(start: {start}, stop: {stop})
          |> filter(fn: (r) => r["_measurement"] == "logs")
          {filter_str}
          |> limit(n: {limit})
          |> sort(columns: ["_time"], desc: true)
        '''

        result = query_api.query(query)

        data = []
        for table in result:
            for record in table.records:
                data.append({
                    "time": record.get_time().isoformat(),
                    "service": record.values.get("service"),
                    "severity": record.values.get("severity"),
                    "field": record.get_field(),
                    "value": record.get_value()
                })

        return {
            "bucket": "factory_errors",
            "count": len(data),
            "filters": {"service": service, "severity": severity},
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {str(e)}")


@router.get("/monitoring")
async def get_monitoring(
    start: str = Query("-1h"),
    stop: str = Query("now()"),
    limit: int = Query(100, ge=1, le=1000),
    service: Optional[str] = None,
    severity: Optional[str] = None,
#    current_user: dict = Depends(verify_admin)
):
    try:
        filters = []
        if service:
            filters.append(f'|> filter(fn: (r) => r["service"] == "{service}")')
        if severity:
            filters.append(f'|> filter(fn: (r) => r["severity"] == "{severity}")')

        filter_str = "\n  ".join(filters)

        query = f'''
        from(bucket: "factory_monitoring")
          |> range(start: {start}, stop: {stop})
          |> filter(fn: (r) => r["_measurement"] == "logs")
          {filter_str}
          |> limit(n: {limit})
          |> sort(columns: ["_time"], desc: true)
        '''

        result = query_api.query(query)

        data = []
        for table in result:
            for record in table.records:
                data.append({
                    "time": record.get_time().isoformat(),
                    "service": record.values.get("service"),
                    "severity": record.values.get("severity"),
                    "field": record.get_field(),
                    "value": record.get_value()
                })

        return {
            "bucket": "factory_monitoring",
            "count": len(data),
            "filters": {"service": service, "severity": severity},
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {str(e)}")


@router.get("/debug")
async def get_debug(
    start: str = Query("-1h"),
    stop: str = Query("now()"),
    limit: int = Query(100, ge=1, le=1000),
    service: Optional[str] = None,
#    current_user: dict = Depends(verify_admin)
):
    try:
        service_filter = f'|> filter(fn: (r) => r["service"] == "{service}")' if service else ""

        query = f'''
        from(bucket: "factory_debug")
          |> range(start: {start}, stop: {stop})
          |> filter(fn: (r) => r["_measurement"] == "logs")
          {service_filter}
          |> limit(n: {limit})
          |> sort(columns: ["_time"], desc: true)
        '''

        result = query_api.query(query)

        data = []
        for table in result:
            for record in table.records:
                data.append({
                    "time": record.get_time().isoformat(),
                    "service": record.values.get("service"),
                    "severity": record.values.get("severity"),
                    "field": record.get_field(),
                    "value": record.get_value()
                })

        return {
            "bucket": "factory_debug",
            "count": len(data),
            "filters": {"service": service},
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {str(e)}")
