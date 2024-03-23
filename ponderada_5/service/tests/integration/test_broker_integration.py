import pytest
from paho import mqtt
import paho.mqtt.client as paho
from mqtt.broker.publisher import Publisher
from mqtt.broker.subscriber import Subscriber
from mqtt.generator.fake_data import SensorDataGenerator
from decouple import config
import json
import time


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


@pytest.fixture
def mock_generator():
    generator = SensorDataGenerator()
    payload = generator.fake_sensor_data()
    return payload


def test_pub_sub_integration(client, mock_generator):
    publisher = Publisher(client, QOS)
    subscriber = Subscriber(client, QOS)
    test_payload = json.dumps(mock_generator)
    received_messages = []
    log = {
        "id": "Id não correspondente",
        "name": "Nome não correspondente",
        "latitude": "Parâmetro 'latitude' não correspondente",
        "longitude": "Parâmetro 'longitude' não correspondente",
        "date": "Parâmetro 'date' não correspondente",
        "sensor_data": "Os dados do sensor não foram recebidos."
    }

    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")

    def on_publish(client, userdata, mid, reason_code, properties):
        print(f"Published message with mid {mid}")

    def on_message(client, userdata, message):
        print(
                f"""
                Received message '{message.payload.decode('utf-8')}'\n
                From topic: '{message.topic}'\n
                QoS level: {message.qos}
                """
            )
        received_messages.append(json.loads(message.payload.decode('utf-8')))

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect(BROKER, PORT)

    publisher.publish(TOPIC, test_payload)

    client.loop_start()
    subscriber.subscribe(TOPIC)
    publisher.publish(TOPIC, test_payload)
    time.sleep(5)
    client.loop_stop()

    assert len(received_messages) > 0, "A mensagem não foi recebida."
    assert received_messages[0]['id'] is not None, log.id
    assert received_messages[0]['name'] is not None, log.name
    assert received_messages[0]['latitude'] is not None, log.latitude
    assert received_messages[0]['longitude'] is not None, log.longitude
    assert received_messages[0]['date'] is not None, log.date
    assert received_messages[0]['sensor_data'] is not None, log.sensor_data
    assert all(
            key in received_messages[0]['sensor_data']
            for key in [
                        'carbon_monoxide_ppm', 'nitrogen_dioxide_ppm',
                        'hydrogen_ppm', 'methane_ppm'
                    ]
        ), "Os parâmetros do sensor não correspondem."
