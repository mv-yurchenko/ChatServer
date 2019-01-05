from queue import Queue, Empty
from threading import Thread


class LogWriter:
    def __init__(self, *args):
        self.filewriter = open(*args)
        self.queue = Queue()
        self.finished = False
        Thread(name="LogWriter", target=self.internal_writer).start()

    def write(self, data):
        # print(data)
        self.queue.put(data)
        print("Data written")

    def internal_writer(self):
        while not self.finished:
            try:
                data = self.queue.get(True, 1)
                print(data)
            except Empty:
                continue
            self.queue.task_done()
            self.filewriter.write(data)
            print(data)

    def close(self):
        self.queue.join()
        self.finished = True
        self.filewriter.close()
