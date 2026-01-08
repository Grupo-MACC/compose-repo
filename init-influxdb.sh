#!/bin/bash
set -e

echo "Esperando a que InfluxDB esté listo..."
sleep 15

echo "Creando buckets adicionales..."
influx bucket create --host "$INFLUX_HOST" -n factory_errors -o "$INFLUX_ORG" -t "$INFLUX_TOKEN" 2>/dev/null || echo "Bucket factory_errors ya existe"
influx bucket create --host "$INFLUX_HOST" -n factory_monitoring -o "$INFLUX_ORG" -t "$INFLUX_TOKEN" 2>/dev/null || echo "Bucket factory_monitoring ya existe"
influx bucket create --host "$INFLUX_HOST" -n factory_debug -o "$INFLUX_ORG" -t "$INFLUX_TOKEN" 2>/dev/null || echo "Bucket factory_debug ya existe"
influx bucket create --host "$INFLUX_HOST" -n factory_infra -o "$INFLUX_ORG" -t "$INFLUX_TOKEN" 2>/dev/null || echo "Bucket factory_infra ya existe"

echo "Buckets creados correctamente"
