from threading import Thread
from queue import Queue


class Mission:
    def __init__(self, max_thread):
        self.queue = Queue()
        self.max_thread = max_thread

    def __enter__(self):
        for x in range(self.max_thread):
            thread = Thread(target=self._threader)
            thread.daemon = True
            thread.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.queue.join()

    def send_task(self, func, *args):
        self.queue.put((func, args))

    def _threader(self):
        while True:
            try:
                func, args = self.queue.get()
                func(*args)
                self.queue.task_done()
            except e:
                pass
