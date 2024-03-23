import pytest
import paho.mqtt.client as paho
from paho import mqtt
from mqtt.broker.publisher import Publisher
from mqtt.generator.fake_data import SensorDataGenerator
import json
from decouple import config


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
def mock_generator():
    generator = SensorDataGenerator()
    payload = generator.fake_sensor_data()
    return payload


@pytest.fixture
def mock_qos():
    return QOS


@pytest.fixture
def publisher(mock_client, mock_qos):
    return Publisher(mock_client, mock_qos)


def test_publish(publisher, mock_client, mock_qos, mock_generator):
    topic = TOPIC
    payload = mock_generator
    json_payload = json.dumps(payload)
    publisher.publish(topic, json_payload)
    mock_client.publish(topic, json_payload, qos=mock_qos)
