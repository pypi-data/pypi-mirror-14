import signal
import time


class ABC(object):
    def setup(self):
        signal.signal(signal.SIGUSR1, self.catch)
        signal.siginterrupt(signal.SIGUSR1, False)

    def catch(self, signum, frame):
        print("xxxx", self, signum, frame)


abc = ABC()
abc.setup()
time.sleep(20)
