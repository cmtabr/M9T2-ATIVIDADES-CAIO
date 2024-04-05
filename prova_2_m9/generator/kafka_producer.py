from confluent_kafka import Producer
import json
import time
from faker import Faker
from faker.providers import DynamicProvider

# Configurações do produtor
producer_config = {
    'bootstrap.servers': 'localhost:29092,localhost:39092',
    'client.id': 'python-producer'
}

topic = 'qualidadeAr'

pollutant_provider = DynamicProvider(
                                provider_name="pollutant",
                                elements=[
                                        'CO2', 
                                        'CO', 
                                        'NO2', 
                                        'O3', 
                                        'PM2.5', 
                                        'PM10'
                                    ],
                                )

class KafkaSensorProducer:
    def __init__(self, producer_config):
        self.producer = Producer(**producer_config)
        self.faker = Faker()
        self.faker.add_provider(pollutant_provider)

    def fake_sensor_data(self) -> str:
        sensor = {
            'name': 'Sensor_' + self.faker.unique.bothify(text='???-###'),
            'air_quality': float(self.faker.pyfloat(
                            min_value=0.05,
                            max_value=10,
                            right_digits=2
                        )),
            'pollutant_type': self.faker.pollutant(),
            'ppm': self.faker.pyint(min_value=0, max_value=1000),
            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        sensor_data = json.dumps(sensor)
        return sensor_data

    def delivery_callback(self, err, msg):
        if err:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def produce_messages(self, topic):
        while True:
            message = self.fake_sensor_data()
            self.producer.produce(topic, message.encode('utf-8'), callback=self.delivery_callback)
            self.producer.flush()
            time.sleep(2)

ksp = KafkaSensorProducer(producer_config=producer_config)

ksp.produce_messages(topic=topic)