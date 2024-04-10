import json
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from confluent_kafka import Consumer, KafkaError
from decouple import Config, RepositoryEnv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

kafka_env = './confluent_kafka.env'

kafka_config = Config(RepositoryEnv(kafka_env))

mongo_env = './mongo.env'

mongo_config = Config(RepositoryEnv(mongo_env))

consumer_config = {
    'bootstrap.servers': kafka_config('KAFKA_BOOTSTRAP_SERVERS'),
    'client.id': kafka_config('KAFKA_CLIENT_ID'),
    'security.protocol': kafka_config('KAFKA_SECURITY_PROTOCOL'),
    'sasl.mechanism': kafka_config('KAFKA_MECHANISM'),
    'sasl.username': kafka_config('KAFKA_API_KEY'),
    'sasl.password': kafka_config('KAFKA_API_SECRET'),
    'client.id': kafka_config('KAFKA_CLIENT_ID'),
    'group.id': kafka_config('KAFKA_GROUP_ID')
}

URI_MONGO = f'mongodb+srv://{mongo_config("MONGO_USER")}:{mongo_config("MONGO_PASSWORD")}@atabase.wjkxbka.mongodb.net/?retryWrites=true&w=majority&appName=database'
USER_MONGO = mongo_config('MONGO_USER')
PASSWORD_MONGO = mongo_config('MONGO_PASSWORD')

@asynccontextmanager
async def data_consumer(app: FastAPI):
    consumer = Consumer(**consumer_config)
    consumer.subscribe([kafka_config('KAFKA_TOPIC')])
    client_mongo = MongoClient(URI_MONGO, server_api=ServerApi('1'))
    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {message.error()}")
                    continue
            
            document = json.loads(message.value().decode('utf-8'))
            client_mongo['database']['sensor'].insert_one(document)
            
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

    yield

app = FastAPI(lifespan=data_consumer)
