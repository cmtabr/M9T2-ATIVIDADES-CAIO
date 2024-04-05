from confluent_kafka import Consumer, KafkaError
import json
import time

# Configurações do consumidor
consumer_config = {
    'bootstrap.servers': 'localhost:29092,localhost:39092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Tópico
topic = 'qualidadeAr'

class KafkaSensorConsumer:
    def __init__(self, consumer_config):
        self.consumer = Consumer(**consumer_config)

    def process_incoming_message(self, topic):
        self.consumer.subscribe([topic])
        try: 
            while True: 
                
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                file = open('../database.txt', 'a')
                print(f"""
                    Sensor: {json.loads(msg.value().decode('utf-8'))['name']}
                    Qualidade do Ar (0 à 10): {json.loads(msg.value().decode('utf-8'))['air_quality']}
                    Tipo de Poluente: {json.loads(msg.value().decode('utf-8'))['pollutant_type']}
                    Grandeza: {str(json.loads(msg.value().decode('utf-8'))['ppm']) + 'ppm'}
                    Data: {json.loads(msg.value().decode('utf-8'))['date']}
                    \n""",
                    file=file,
                )
        except KeyboardInterrupt: 
            pass
        finally:
            self.consumer.close()
            
ksc = KafkaSensorConsumer(consumer_config=consumer_config)

ksc.process_incoming_message(topic=topic)