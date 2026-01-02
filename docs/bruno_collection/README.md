# Colección Bruno - PBL Grupo2 (microservicios)

Esta colección está preparada para probar el *compose* del repositorio que me has pasado.

## Cómo usarla

1. Abre **Bruno** → **Import** → selecciona la carpeta de esta colección.
2. Elige un entorno en **Environments**:
   - **Docker Compose (Gateway + Warehouse direct)** (recomendado):
     - Usa el **API Gateway (HAProxy)** para `auth`, `order`, `machine`, `delivery`, `payment`.
     - Usa **puerto directo** para `warehouse` (porque en tu `haproxy.cfg` no existe ruta `/warehouse`).
   - **Direct Ports (sin Gateway)**: útil si algún día expones `auth` en host (por defecto en tu compose NO está expuesto).
3. Si vas a usar el Gateway por HTTPS con certificados locales:
   - En Bruno: **Settings → General → desactiva “SSL/TLS Certificate Verification”**.
   - Si ejecutas por CLI: usa `bru run --insecure`.

## Flujo recomendado (para simular acciones de usuario)

1. **00 Healthchecks**: comprueba que todo responde.
2. **01 Auth**:
   - `Admin login` (tokens admin se guardan en variables `admin_access_token` / `admin_refresh_token`).
   - `Create user (role user)` (crea un usuario normal con `role_id=2`).
   - `User login` (tokens del usuario se guardan en `access_token` / `refresh_token`).
3. **02 Payment**:
   - `Top up wallet` para meter saldo al usuario.
   - `View wallet` para comprobarlo.
4. **03 Orders**:
   - `Create order` crea un pedido y guarda `order_id`.
   - `View order by id` / `List orders` para inspeccionar.
5. **04 Warehouse** (pruebas del microservicio aislado):
   - `Set stock` / `Add stock`.
   - `Ingest order` y luego `Get manufacturing order status`.
   - `Simulate piece built` para marcar piezas como fabricadas.

## Variables importantes

En el entorno recomendado puedes cambiar:
- `adminUsername`, `adminPassword` (por defecto `admin` / `adminpass`, según tu `auth/app_auth/core/config.py`).
- `userUsername`, `userPassword` (usuario de pruebas a crear).
- `orderPieces`, `orderAddress`, `orderDescription`.
- `topUpAmount`.
- `whOrderId` y cantidades para Warehouse (en los bodies de las requests).

## Notas técnicas (para que no te explote nada “porque sí”)

- **Auth no está publicado en host** en tu `docker-compose.yaml` (no tiene `ports:`), así que **desde Bruno solo lo puedes llamar vía Gateway**.
- **Warehouse** sí está publicado en `5005:5005`, pero **no está enrutado por HAProxy**, por eso aquí lo llamo directo.
- Si el Gateway te da errores de certificado: desactiva la verificación SSL/TLS en Bruno (o añade tu CA/cert en Bruno si prefieres hacerlo “bien”).
