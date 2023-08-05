import signal


class timeout:
    def __init__(self, seconds=1):
        self.seconds = seconds

    def handle_timeout(self, signum, frame):
        raise Exception("Timeout")

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
