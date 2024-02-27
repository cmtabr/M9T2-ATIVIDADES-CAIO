# import time


class Publisher:
    def __init__(self, client, qos=0):
        self.client = client
        self.qos = qos

    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload, qos=self.qos)
        # Uncomment the next lines to see the published message information
        # print(
        #     f"""Message published:\n
        #     Topic: '{topic}'\n
        #     Payload: {payload}\n
        #     QoS: {self.qos}
        #     Time: {time.strftime("%H:%M:%S")}
        #     """
        # )
