class Subscriber:
    def __init__(self, client, qos=0):
        self.client = client
        self.qos = qos

    def subscribe(self, topic: str):
        self.client.subscribe(topic, self.qos)
        print(f"Subscribed to {topic} with QoS {self.qos}")

    def on_message(self, client, message: str):
        return print(message)
