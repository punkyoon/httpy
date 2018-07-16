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
            karg = None
            task_args = self.task.get()

            func = task_args[0]
            arg = task_args[1]

            if len(task_args) > 2:
                karg = task_args[2]

            try:
                if karg is None:
                    func(arg)
                else:
                    func(arg, karg)
            except Exception as e:
                print(e)

            self.task.task_done()
