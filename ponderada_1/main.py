import paho.mqtt.client as mqtt
import time
from typing import Any

from sensor import SensorDataGenerator

# region Broker Connection
class BrokerConnection:
    def __init__(self) -> None:
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "R2-D2")
        self.client.connect("localhost", 1891, 60)

    def publish(self, topic: str, message: Any, qos: int) -> None:
        self.client.publish(topic, payload=message, qos=qos, retain=True)

    def __del__(self):
        self.client.disconnect()
# endregion

if __name__ == "__main__":
    broker = BrokerConnection()
    message = SensorDataGenerator()
    try:
        while True:
            broker.publish("data/mics6814", message.fake_sensor_data(), 0)
            print(f"Publicado: {message}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Publicação encerrada")
        del broker