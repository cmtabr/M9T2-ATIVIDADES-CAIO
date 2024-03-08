import paho.mqtt.client as mqtt
import time
from typing import Any
from faker import Faker
import json

class BrokerConnection:
    def __init__(self, client_id) -> None:
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self.client.connect("localhost", 1891, 60)

    def publish(self, topic: str, message: Any, qos: int) -> None:
        self.client.publish(topic, payload=message, qos=qos, retain=False)

    def __del__(self):
        self.client.disconnect()

# class PayloadGenerator: 
#     def __init__(self) -> None: 
#         self.fake = Faker()

#     def generate_id():
#         for i in range(1, 10, 1):
#             for j in range(i - 2):
#                 for k in range(j - 1):
#                     l = ('f' if k % 2 == 0 else 'g')
#                     yield f'lj0{i}{l}0{j}'
#                 time.sleep(1)

#     def fake_sensor_data(self) -> json:
#         for i in self.generate_id:
#             id = i 
#             type = ('geladeira' if id[4] == 'g' else 'freezer')
#             date = time.strftime('%Y-%m-%d %H:%M:%S')
#             temperature = self.fake.pyint(min_value=-30, max_value=-5)
#             sensor = {
#                 "id":id,
#                 "type":type,
#                 "date": date,
#                 "temperature": temperature
#             }
#         return json.dumps(sensor)

def generate_id():
        for i in range(1, 10, 1):
            for j in range(i - 2):
                for k in range(j - 1):
                    l = ('f' if k % 2 == 0 else 'g')
                    yield f'lj0{i}{l}0{j}'
                    time.sleep(1)

if __name__ == '__main__':
    fake = Faker()
    broker = BrokerConnection("R2-D2")
    for i in generate_id():
        id = i 
        tipo = 'geladeira' if id[4] == 'g' else 'freezer'
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        temperatura = fake.pyint(min_value=-30, max_value=-5)
        sensor = {
            "id":id,
            "tipo":tipo,
            "date": date,
            "temperatura": temperatura
        }
        print(sensor)
        broker.publish("data/mics6814", str(sensor), 0)
