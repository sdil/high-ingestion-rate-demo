import signal
from time import sleep
from kafka import KafkaConsumer


class GracefulKiller:
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        print("received kill signal")
        self.kill_now = True


def process_message(message):
    print("received message: {}".format(message))
    # sleep(5)
    print("done processing")


if __name__ == "__main__":
    print("starting consumer app")
    killer = GracefulKiller()
    consumer = KafkaConsumer(
        "twitch_chat",
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-group",
    )
    n = 0

    for message in consumer:
        process_message(message.value)
        n += 1
        print(n)

        if killer.kill_now:
            print("End of the program. I was killed gracefully :)")
            consumer.close()
            exit()
