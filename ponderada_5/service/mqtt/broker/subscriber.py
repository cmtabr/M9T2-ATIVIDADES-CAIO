# import time


class Subscriber:
    def __init__(self, client, qos=0):
        self.client = client
        self.qos = qos

    def subscribe(self, topic: str):
        self.client.subscribe(topic, self.qos)
        # Uncomment the next lines to see the subscription information
        # print(
        #     f"""Subscription Information:\n
        #     Topic: {topic}\n
        #     QoS: {self.qos}\n
        #     Time: {time.strftime("%H:%M:%S")}
        #     """
        # )
