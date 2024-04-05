from confluent_kafka import Producer, Consumer, KafkaError
import json
import time

# Configurações do consumidor
consumer_config = {
    'bootstrap.servers': 'localhost:29092,localhost:39092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Topico
topic = 'qualidadeAr'

# Criar consumidor
consumer = Consumer(**consumer_config)

# Assinar tópico
consumer.subscribe([topic])

# Consumir mensagens
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print(f"""
            Sensor: {json.loads(msg.value().decode('utf-8'))['name']}
            Qualidade do Ar (0 à 10): {json.loads(msg.value().decode('utf-8'))['air_quality']}
            Tipo de Poluente: {json.loads(msg.value().decode('utf-8'))['pollutant_type']}
            Grandeza: {str(json.loads(msg.value().decode('utf-8'))['ppm']) + 'ppm'}
            Data: {json.loads(msg.value().decode('utf-8'))['date']}
            """
        )
except KeyboardInterrupt:
    pass
finally:
    consumer.close()