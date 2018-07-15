# Worker for ThreadPool

from threading import Thread


class Worker(Thread):
    def __init__(self, task):
        Thread.__init__(self)
        self.task = task
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, arg, karg = self.task.get()

            try:
                func(arg, karg)
            except Exception as e:
                print(e)

            self.task.task_done()
