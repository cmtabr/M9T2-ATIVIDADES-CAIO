import paho.mqtt.client as paho
from paho import mqtt
from mqtt.broker.publisher import Publisher
from mqtt.broker.subscriber import Subscriber
from mqtt.generator.fake_data import SensorDataGenerator
import json
import time
from decouple import config


BROKER = config("BROKER", cast=str)
PORT = config("PORT", cast=int)
QOS = config("QOS", cast=int)
USER = config("PROFILE", cast=str)
CLIENT_ID = config("CLIENT_ID", cast=str)
PASSWORD = config("PASSWORD", cast=str)
TOPIC = config("TOPIC", cast=str)


client = paho.Client(
    callback_api_version=paho.CallbackAPIVersion.VERSION2,
    client_id=CLIENT_ID
    )

client.connect(BROKER, PORT, 60)

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set(USER, PASSWORD)

generator = SensorDataGenerator()

publisher = Publisher(client, QOS)

subscriber = Subscriber(client, QOS)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with status code {reason_code}")

def on_message(client, userdata, message):
    print(type(message.payload.decode('utf-8')))
    # print(
    #         f"""On Message:\n
    #         Received message '{message.payload.decode('utf-8')}'\n
    #         From topic: '{message.topic}'\n
    #         QoS level: {message.qos}
    #         """
    #     )
    message = json.loads(message.payload.decode('utf-8'))
    consumer(message)

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Published message with mid {mid}")


from psycopg2 import connect

def get_db():
    conn = connect(
        dbname="metabase",
        user="metabase",
        password="metabase",
        host="localhost",
        port = "5432"
    )
    try: 
        return conn
    except Exception as e:
        print(e)

conn = get_db()

def consumer(typo: json):
    id = typo.get("id")
    name = typo.get("name")
    latitude = typo.get("latitude")
    longitude = typo.get("longitude")
    date = typo.get("date")
    temperature = typo.get("temperature")
    humidity = typo.get("humidity")
    pressure = typo.get("pressure")
    with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO metabase (id, name, latitude, longitude, date, temperature, humidity, pressure) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, 
                (id, name, latitude, longitude, date, temperature, humidity, pressure))
            conn.commit()
            print(f"Inserted data into database")
    return {"status": "ok"}


client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(BROKER, PORT)

subscriber.subscribe(TOPIC)

client.loop_start()

i = 0

while i < 9:
    publisher.publish(TOPIC, json.dumps(generator.fake_sensor_data()))
    i += 1
    time.sleep(2)
