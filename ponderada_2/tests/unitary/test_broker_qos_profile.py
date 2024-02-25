import pytest
import json
from unittest.mock import MagicMock
from mypkg.broker.publisher import Publisher
from mypkg.broker.subscriber import Subscriber


@pytest.fixture
def config():
    with open('simulator_config.json', 'r') as f:
        return json.load(f)


@pytest.fixture
def mock_qos(config):
    return config['mqtt']['qos']


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def publisher(mock_client, mock_qos):
    return Publisher(mock_client, mock_qos)


@pytest.fixture
def subscriber(mock_client, mock_qos):
    return Subscriber(mock_client, mock_qos)


def test_publisher_qos(publisher, mock_client, mock_qos):
    publisher.publish("test/topic", "test message")
    mock_client.publish.assert_called_with(
                                        "test/topic",
                                        "test message",
                                        qos=mock_qos
                                    )


def test_subscriber_qos(subscriber, mock_client, mock_qos):
    subscriber.subscribe("test/topic")
    mock_client.subscribe.assert_called_with("test/topic", mock_qos)
