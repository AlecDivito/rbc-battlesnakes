import threading
import subprocess


class Trainer(threading.Thread):

    def __init__(self, name, cmd, counter, max_iterations, console=False):
        threading.Thread.__init__(self)
        self.name = name
        self.cmd = cmd.split()
        self.counter = counter
        self.max_iterations = max_iterations
        self.console = console

    def run(self):
        if self.console is True:
            self.run_with_console()
        else:
            self.run_without_console()

    def run_without_console(self):
        """
        Execute the command without capturing console output
        """
        next_count = self.counter.increment()
        while next_count < self.max_iterations:
            # print("Thread {}: Running iteration {}".format(self.name, next_count))
            subprocess.run(self.cmd, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, capture_output=False, text=False)
            next_count = self.counter.increment()

    def run_with_console(self):
        """
        Execute the command with capturing console output
        """
        next_count = self.counter.increment()
        while next_count < self.max_iterations:
            print("Running iteration {}".format(next_count))
            result = subprocess.run(self.cmd, capture_output=True, text=True)
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            next_count = self.counter.increment()


class AtomicCounter:

    def __init__(self, initial=0):
        self.value = initial
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.value += 1
            return self.value

    def get(self):
        with self._lock:
            return self.value
