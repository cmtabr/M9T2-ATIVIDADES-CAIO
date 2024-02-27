import pytest
from unittest.mock import MagicMock
from mqtt.broker.subscriber import Subscriber
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
def subscriber(mock_client, mock_qos):
    return Subscriber(mock_client, mock_qos)


def test_subscribe(subscriber, mock_client, mock_qos):
    topic = "test/topic"
    subscriber.subscribe(topic)
    mock_client.subscribe.assert_called_once_with(topic, mock_qos)
