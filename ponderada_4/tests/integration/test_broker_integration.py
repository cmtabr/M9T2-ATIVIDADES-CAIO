import pytest
from paho import mqtt
import paho.mqtt.client as paho
from mqtt.broker.publisher import Publisher
from mqtt.broker.subscriber import Subscriber
from mqtt.generator.fake_data import SensorDataGenerator
from decouple import config
import time
import json

BROKER = config("BROKER", cast=str)
PORT = config("PORT", cast=int)
QOS = config("QOS", cast=int)
USER = config("PROFILE", cast=str)
CLIENT_ID = config("CLIENT_ID", cast=str)
PASSWORD = config("PASSWORD", cast=str)
TOPIC = config("TOPIC", cast=str)


@pytest.fixture
def client():
    client = paho.Client(
        callback_api_version=paho.CallbackAPIVersion.VERSION2, 
        client_id=CLIENT_ID
        )
    client.connect(BROKER, PORT, 60)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(USER, PASSWORD)
    return client

def test_pub_sub_integration(client):
    subscriber = Subscriber(client, QOS)
    publisher = Publisher(client, QOS)
    generator = SensorDataGenerator()

    test_topic = TOPIC
    test_payload = generator.fake_sensor_data()

    received_messages = []

    def on_message(client, userdata, message):
        received_messages.append(message)

    client.on_message = on_message
    subscriber.subscribe(test_topic)

    client.loop_start()
    time.sleep(5)

    publisher.publish(test_topic, test_payload)
    time.sleep(5)

    client.loop_stop()

    assert len(received_messages) > 0
    message = received_messages[0]
    expected_payload = json.loads(test_payload)
    receiced_payload = json.loads(message.payload.decode())
    assert message.topic == test_topic
    assert receiced_payload == expected_payload
    assert message.qos == QOS
