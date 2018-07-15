# Thread pool

from queue import Queue
from thread_pool.worker import Worker


class ThreadPool:
    def __init__(self, num_thread):
        self.task = Queue(num_thread)

        for tmp in range(num_thread):
            Worker(self.task)

    def __str__(self):
        return 'Thread Pool task: {}'.format(self.task)

    def add_task(self, func, *args, **kwargs):
        self.task.put((func, args, kwargs))

    def wait_completion(self):
        self.task.join()
