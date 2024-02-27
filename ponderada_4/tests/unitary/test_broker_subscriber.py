import pytest
import paho.mqtt.client as paho
from paho import mqtt
from mqtt.broker.subscriber import Subscriber
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
def mock_qos():
    return QOS


@pytest.fixture
def subscriber(mock_client, mock_qos):
    return Subscriber(mock_client, mock_qos)


def test_subscribe(subscriber, mock_client, mock_qos):
    topic = TOPIC
    subscriber.subscribe(topic)
    mock_client.subscribe(topic, mock_qos)
