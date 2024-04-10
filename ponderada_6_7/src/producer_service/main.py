import json
import time

from contextlib import asynccontextmanager
from decouple import Config, RepositoryEnv
from fastapi import FastAPI
import paho.mqtt.client as paho
from paho import mqtt

from generator.data_generator import Generator as _producer

env = './hivemq.env'

config = Config(RepositoryEnv(env))

BROKER = config("BROKER", cast=str)
PORT = config("PORT", cast=int)
QOS = config("QOS", cast=int)
USER = config("PROFILE", cast=str)
CLIENT_ID = config("CLIENT_ID", cast=str)
PASSWORD = config("PASSWORD", cast=str)
TOPIC = config("TOPIC", cast=str)


client = paho.Client(
    callback_api_version=paho.CallbackAPIVersion.VERSION2,
    client_id=CLIENT_ID
    )

client.connect(BROKER, PORT, 60)

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set(USER, PASSWORD)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with status code {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Published message with mid {mid}")

def message_producer():
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(BROKER, PORT)

    while True:
        message = json.dumps(_producer().data_generator())
        client.publish(TOPIC, message, QOS)
        time.sleep(1)


@asynccontextmanager
async def data_posting(app: FastAPI):
    task = message_producer()
    yield
    await task()

app = FastAPI(lifespan=data_posting)

