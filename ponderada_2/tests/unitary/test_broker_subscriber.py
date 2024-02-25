import pytest
from unittest.mock import MagicMock
from mypkg.broker.subscriber import Subscriber


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def mock_qos():
    return 1


@pytest.fixture
def subscriber(mock_client, mock_qos):
    return Subscriber(mock_client, mock_qos)


def test_subscribe(subscriber, mock_client, mock_qos):
    topic = "test/topic"
    subscriber.subscribe(topic)
    mock_client.subscribe.assert_called_once_with(topic, mock_qos)
