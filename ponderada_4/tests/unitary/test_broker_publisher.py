import pytest
from unittest.mock import MagicMock
from mqtt.broker.publisher import Publisher
import json


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def config():
    with open('simulator_config.json', 'r') as f:
        return json.load(f)


@pytest.fixture
def mock_qos(config):
    return config['mqtt']['qos']


@pytest.fixture
def publisher(mock_client, mock_qos):
    return Publisher(mock_client, mock_qos)


def test_publish(publisher, mock_client, mock_qos):
    topic = "test/topic"
    payload = "test message"
    publisher.publish(topic, payload)
    mock_client.publish.assert_called_once_with(topic, payload, qos=mock_qos)
