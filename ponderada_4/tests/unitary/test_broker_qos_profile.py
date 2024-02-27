import pytest
import paho.mqtt.client as paho
from paho import mqtt
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
def mock_client():
    client = paho.Client(
        callback_api_version=paho.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID
        )
    client.connect(BROKER, PORT, 60)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(USER, PASSWORD)
    return client


@pytest.fixture
def mock_qos():
    return QOS


@pytest.fixture
def publisher(mock_client, mock_qos):
    return Publisher(mock_client, mock_qos)


@pytest.fixture
def subscriber(mock_client, mock_qos):
    return Subscriber(mock_client, mock_qos)


@pytest.fixture
def mock_generator():
    generator = SensorDataGenerator()
    payload = generator.fake_sensor_data()
    return payload


def test_subscriber_qos(subscriber, mock_client, mock_qos, mock_generator):
    def on_message(client, userdata, message):
        assert message.topic == TOPIC
        received_payload = message.payload
        expected_payload = json.loads(mock_generator)
        assert received_payload == expected_payload

    mock_client.on_message = on_message

    mock_client.loop_start()

    subscriber.subscribe(TOPIC)
    mock_client.subscribe(TOPIC, qos=mock_qos)

    mock_client.publish(TOPIC, json.dumps(mock_generator), qos=mock_qos)

    time.sleep(1)

    mock_client.loop_stop()


def test_publisher_qos(publisher, mock_client, mock_qos, mock_generator):
    serialized_payload = json.dumps(mock_generator)

    def on_message(client, userdata, message):
        assert message.topic == TOPIC
        received_payload = message.payload
        expected_payload = json.loads(serialized_payload)
        assert received_payload == expected_payload

    mock_client.on_message = on_message

    mock_client.loop_start()

    mock_client.subscribe(TOPIC, qos=mock_qos)

    publisher.publish(topic=TOPIC, payload=serialized_payload)

    time.sleep(1)

    mock_client.loop_stop()
