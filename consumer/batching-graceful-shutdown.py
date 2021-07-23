import signal
from time import sleep
from kafka import KafkaConsumer
import threading
from queue import Queue, Empty

items = Queue()


class GracefulKiller:
    def __init__(self, consumer):
        self.consumer = consumer
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        print("received kill signal")
        consumer.stop()
        persist_messages()
        exit(0)


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        print("stopping consumer thread")
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(
            "twitch_chat",
            bootstrap_servers=["localhost:9092"],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="my-group",
        )

        while not self.stop_event.is_set():
            for message in consumer:
                self.process_message(message.value)
                if self.stop_event.is_set():
                    break

        consumer.close()

    def process_message(self, message):
        items.put(message)


def persist_messages():
    print("PERSISTING MESSAGES")
    n = -1

    with open("output.txt", "a+") as f:
        try:
            while True:
                n += 1
                i = items.get_nowait()
                f.write(f"{i}\n")

        except Empty:
            pass

    print(n)


if __name__ == "__main__":
    print("Starting batching worker")

    consumer = Consumer()
    consumer.daemon = True
    consumer.start()

    killer = GracefulKiller(consumer)

    while True:
        persist_messages()
        sleep(1)
