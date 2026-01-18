# Colección Bruno - PBL Grupo2 (microservicios)

Esta colección está preparada para probar el *docker-compose* del proyecto.

## Cómo usarla

1. Abre **Bruno** → **Import** → selecciona la carpeta de esta colección.
2. Elige un entorno en **Environments**:
   - **Docker Compose (Gateway HTTPS)** (recomendado):
     - Usa el **API Gateway (HAProxy)** para **todos** los microservicios (`auth`, `order`, `machine`, `delivery`, `payment`, `warehouse`).
     - El gateway expone `https://localhost` (puerto 443). El puerto 80 redirige a 443.
   - **Direct Ports (sin Gateway)**:
     - Llama a cada microservicio por su puerto publicado en host.
     - Machine: A en 5001 y B en 5006 (en tu docker-compose actual).
     - Importante: en tu compose, **Auth no está publicado en host** (no tiene `ports:`). Si quieres usar este entorno para Auth, tendrás que exponerlo.

3. Certificados TLS locales (CA propia):
   - En Bruno: **Settings → General → desactiva “SSL/TLS Certificate Verification”**.
   - Si ejecutas por CLI: usa `bru run --insecure`.

   Si prefieres hacerlo “bien”, importa tu `ca.pem` como CA de confianza en tu sistema o configura Bruno para confiar en esa CA.

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
5. **04 Warehouse**:
   - `Set stock` / `Add stock`.
   - `Ingest order` y luego `Get fabrication order status`.
   - `Simulate piece built` para marcar piezas como fabricadas.

## Variables importantes

En el entorno recomendado puedes cambiar:
- `adminUsername`, `adminPassword` (por defecto `admin` / `adminpass`).
- `userUsername`, `userPassword` (usuario de pruebas a crear).
- `orderPieces`, `orderAddress`, `orderDescription`.
- `topUpAmount`.
- Variables de Warehouse (cantidades/stock) en los bodies de las requests.

## Notas técnicas

- Todos los microservicios están en **HTTPS-only**. Si llamas a puertos directos, usa `https://`.
- El API Gateway (HAProxy) también está en HTTPS y valida certificados de los backends con tu CA.
- Si el Gateway te da errores de certificado en Bruno: desactiva la verificación SSL/TLS o importa la CA.
