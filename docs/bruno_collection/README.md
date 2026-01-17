# [PBL] Grupo2 - Microservicios (TLS + Gateway)

## Importar y seleccionar entorno

1) En Bruno (app) -> **Import** -> selecciona el `.zip`.
2) Arriba a la derecha, en el desplegable **Environment**, selecciona uno de estos:

- **tls-gateway** (recomendado): usa el **API Gateway (HAProxy)** para todos los micros, incluido Warehouse.
- **tls-direct-ports**: llama a cada microservicio por su puerto (`https://localhost:500x`).

(Se mantienen entornos legacy `*-http*` por compatibilidad, pero para TLS usa los `tls-*`).

## Variables cómodas (sin tocar los .bru)

Cambia desde el Environment:
- `orderPiecesA`, `orderPiecesB`, `orderAddress`, `orderDescription`
- `topUpAmount`
- credenciales (`adminUsername`, `adminPassword`, `userUsername`, ...)

La request **Create order (A+B)** usa esas variables directamente.

## TLS / Certificados (Bruno)

Si Bruno muestra error de certificado (CA propia / self-signed), lo correcto es instalar tu `ca.pem` en el almacén de CAs del sistema y reiniciar Bruno.

En Debian/Ubuntu:

```bash
sudo cp ./certs/ca.pem /usr/local/share/ca-certificates/pbl-grupo2-ca.crt
sudo update-ca-certificates
```
