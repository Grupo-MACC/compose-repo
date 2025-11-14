#!/bin/bash
set -e

echo "Esperando a que InfluxDB esté listo..."
sleep 15

echo "Creando buckets adicionales..."
influx bucket create -n factory_errors -o my-org -t MY_CUSTOM_TOKEN_123456 2>/dev/null || echo "Bucket factory_errors ya existe"
influx bucket create -n factory_monitoring -o my-org -t MY_CUSTOM_TOKEN_123456 2>/dev/null || echo "Bucket factory_monitoring ya existe"
influx bucket create -n factory_debug -o my-org -t MY_CUSTOM_TOKEN_123456 2>/dev/null || echo "Bucket factory_debug ya existe"

echo "Buckets creados correctamente"