import paho.mqtt.client as paho
from paho import mqtt
from mqtt.broker.publisher import Publisher
from mqtt.broker.subscriber import Subscriber
from mqtt.generator.fake_data import SensorDataGenerator
import json
import time
from decouple import config


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

generator = SensorDataGenerator()

publisher = Publisher(client, QOS)

subscriber = Subscriber(client, QOS)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with status code {reason_code}")

def on_message(client, userdata, message):
    print(
            f"""On Message:\n
            Received message '{message.payload.decode('utf-8')}'\n
            From topic: '{message.topic}'\n
            QoS level: {message.qos}
            """
        )

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Published message with mid {mid}")


client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(BROKER, PORT)

subscriber.subscribe(TOPIC)

client.loop_start()

i = 0

while i < 9:
    publisher.publish(TOPIC, json.dumps(generator.fake_sensor_data()))
    time.sleep(1)
    i += 1

client.loop_stop()
