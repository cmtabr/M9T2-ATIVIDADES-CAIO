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

    def on_message(client, userdata, message):
        incoming_data = message.payload.decode('utf-8')
        if incoming_data["tipo"] == "freezer" and incoming_data["temperatura"] > -15:
            print(f'[Alerta] : Temperatura elevada - Setor Congelados | {incoming_data["temperatura"]}ºC')
        elif incoming_data["tipo"] == "freezer" and incoming_data["temperatura"] < -25:
            print(f'[Alerta] : Temperatura baixa - Setor Congelados | {incoming_data["temperatura"]}ºC')
        elif incoming_data["tipo"] == "geladeira" and incoming_data["temperatura"] > 10:
            print(f'[Alerta] : Temperatura elevada - Setor Refrigerados | {incoming_data["temperatura"]}ºC')
        elif incoming_data["tipo"] == "geladeira" and incoming_data["temperatura"] < 2:
            print(f'[Alerta] : Temperatura baixa - Setor Refrigerados | {incoming_data["temperatura"]}ºC')
        else:
            print(f'Nenhuma ação necessária')

    def __del__(self):
        self.client.disconnect()

def generate_id():
        for i in range(1, 10, 1):
            for j in range(i - 2):
                for k in range(j - 1):
                    l = ('f' if k % 2 == 0 else 'g')
                    yield f'lj0{i}{l}0{j}'
                    time.sleep(1)

if __name__ == '__main__':
    fake = Faker()
    broker = BrokerConnection('R2-D2')
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
        broker.publish("prova/m9-p1", json.dumps(sensor), 1)
    broker.on_message