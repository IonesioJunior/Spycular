import os
import signal
import sys

from spycular.consumer.websocket import WebSocketConsumer
from spycular.store.virtual import VirtualStore


def websocket_server(module):
    with open("server.pid", "w") as pid_file:
        pid_file.write(str(os.getpid()))
    ws_consumer = WebSocketConsumer(VirtualStore(), "localhost", 8765)
    ws_consumer.set_module(module=module)
    ws_consumer.listen()


def start_server():
    if len(sys.argv) <= 2:
        print(
            "You should provide at least\
              two arguments <numpy|torch> <ws|http|webrtc>",
        )
        return
    module = None
    if sys.argv[1] == "numpy":
        import numpy as np

        module = np
    elif sys.argv[1] == "torch":
        import torch as th

        module = th
    else:
        print("First argument should be either numpy or torch")
        return
    if sys.argv[2] == "ws":
        websocket_server(module)
    elif sys.argv[2] == "http":
        print("Not implemented yet")
    elif sys.argv[2] == "webrtc":
        print("Not implemented yet")
    else:
        print("Second argument should be either ws, http or webrtc")
        return


def stop():
    with open("server.pid", "r") as pid_file:
        pid = int(pid_file.read())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Server with PID {pid} has been terminated.")
    except ProcessLookupError:
        print(f"No process with PID {pid} found.")
