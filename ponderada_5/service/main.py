import paho.mqtt.client as paho
from paho import mqtt
from mqtt.broker.publisher import Publisher
from mqtt.broker.subscriber import Subscriber
from mqtt.generator.fake_data import SensorDataGenerator
import json
from decouple import config
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
        yield conn
    except Exception as e:
        print(e)
    finally:
        conn.close()

def consumer(typo: json):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO metabase (id, name, latitude, longitude, date, humidity, pressure) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, 
                (typo.name, typo.valor, typo.latitude, typo.longitude, typo.date, typo.humidity, typo.pressure))
            conn.commit()
            cursor.close()
    return {"status": "ok"}

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

publisher = Publisher(client, QOS)

def on_message(client, userdata, message):
    message = message.payload.decode('utf-8')
    consumer(json.loads(message))
    print(f"Message consumed: {message}")

client.on_message = on_message

client.loop_forever()