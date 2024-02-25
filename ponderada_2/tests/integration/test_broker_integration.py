import pytest
import paho.mqtt.client as mqtt
from mypkg.broker.publisher import Publisher
from mypkg.broker.subscriber import Subscriber
import time


BROKER = 'localhost'
PORT = 1891
QOS = 1


@pytest.fixture
def client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "R2-D2")
    client.connect(BROKER, PORT, 60)
    return client


def test_pub_sub_integration(client):
    subscriber = Subscriber(client, QOS)
    publisher = Publisher(client, QOS)

    test_topic = "test/integration"
    test_payload = "Hello MQTT"

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
    assert message.topic == test_topic
    assert message.payload.decode() == test_payload
    assert message.qos == QOS
