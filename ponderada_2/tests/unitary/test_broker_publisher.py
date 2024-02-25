import pytest
from unittest.mock import MagicMock
from mypkg.broker.publisher import Publisher


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def mock_qos():
    return 1


@pytest.fixture
def publisher(mock_client, mock_qos):
    return Publisher(mock_client, mock_qos)


def test_publish(publisher, mock_client, mock_qos):
    topic = "test/topic"
    payload = "test message"
    publisher.publish(topic, payload)
    mock_client.publish.assert_called_once_with(topic, payload, qos=mock_qos)
