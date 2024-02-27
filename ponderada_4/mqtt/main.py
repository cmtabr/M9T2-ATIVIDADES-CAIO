import paho.mqtt.client as paho
from paho import mqtt
from mqtt.broker.publisher import Publisher
from mqtt.broker.subscriber import Subscriber
from mqtt.generator.fake_data import SensorDataGenerator
from decouple import config
import time

frequency = time.sleep(5)
BROKER = config("BROKER")
PORT = config("PORT", cast=int)
QOS = config("QOS")
USER = config("PROFILE")
CLIENT_ID = config("CLIENT_ID")
PASSWORD = config("PASSWORD")
TOPIC = config("TOPIC")


print(f"""
        BROKER: {BROKER}\n
        PORT: {PORT}\n
        QOS: {QOS}\n
        USER: {USER}\n
        CLIENT_ID: {CLIENT_ID}\n
        PASSWORD: {PASSWORD}\n
        TOPIC: {TOPIC}
        """
    )


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"CONNACK received with code {reason_code}")
    client.subscribe(TOPIC, qos=1)

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(f"{msg.topic} (QoS: {msg.qos}) - {msg.payload.decode('utf-8')}")

# Instanciação do cliente
client = paho.Client(paho.CallbackAPIVersion.VERSION2, "Subscriber",
                     protocol=paho.MQTTv5)
client.on_connect = on_connect

# Configurações de TLS
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(USER, PASSWORD)  # Configuração da autenticação

client.on_message = on_message

# Conexão ao broker
client.connect(BROKER, port=PORT)

# Loop de espera por mensagens
client.loop_forever()