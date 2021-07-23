from time import sleep
import signal

items = []

def run_operation():
    items.append("a")
    print(items)

def exit_print(*args, **kwargs):
    print('exiting. running one last operation')
    run_operation()
    exit(0)

signal.signal(signal.SIGTERM, exit_print)

while True:
    run_operation()
    sleep(2)
