class Publisher:
    def __init__(self, client, qos=0):
        self.client = client
        self.qos = qos

    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload, qos=self.qos)
        print(
            f"""Message published\n
            Topic: '{topic}'\n
            Payload: '{payload}'\n
            QoS: {self.qos}
            """
        )
