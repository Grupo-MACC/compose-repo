from microservice_chassis_grupo2.core.rabbitmq_core import get_channel, declare_exchange, declare_exchange_logs, PUBLIC_KEY_PATH
import asyncio
import httpx
import json
from aio_pika import Message
from microservice_chassis_grupo2.core.router_utils import AUTH_SERVICE_URL


async def consume_auth_events():
    _, channel = await get_channel()
    
    exchange = await declare_exchange(channel)
    
    logs_queue = await channel.declare_queue('logs_queue', durable=True)
    await logs_queue.bind(exchange, routing_key="auth.running")
    await logs_queue.bind(exchange, routing_key="auth.not_running")
    
    await logs_queue.consume(handle_auth_events)

async def handle_auth_events(message):
    async with message.process():
        data = json.loads(message.body)
        if data["status"] == "running":
            try:
                async with httpx.AsyncClient(
                    verify="/certs/ca.pem",
                    cert=("/certs/logs/logs-cert.pem", "/certs/logs/logs-key.pem"),
                ) as client:
                    response = await client.get(
                        f"{AUTH_SERVICE_URL}/auth/public-key"
                    )
                    response.raise_for_status()
                    public_key = response.text
                    
                    with open(PUBLIC_KEY_PATH, "w", encoding="utf-8") as f:
                        f.write(public_key)
                    
                    await publish_to_logger(message={"message":"Clave publica guardada"},topic="logs.info")

            except Exception as exc:
                print(exc)
async def publish_to_logger(message, topic):
    connection = None
    try:
        connection, channel = await get_channel()
        
        exchange = await declare_exchange_logs(channel)
        
        # Asegúrate de que el mensaje tenga estos campos
        log_data = {
            "measurement": "logs",
            "service": topic.split('.')[0],
            "severity": topic.split('.')[1],
            **message
        }

        msg = Message(
            body=json.dumps(log_data).encode(), 
            content_type="application/json", 
            delivery_mode=2
        )
        await exchange.publish(message=msg, routing_key=topic)
        
    except Exception as e:
        print(f"Error publishing to logger: {e}")
    finally:
        if connection:
            await connection.close()