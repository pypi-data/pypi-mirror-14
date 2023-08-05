from collections import deque


class WorkingQueue:

    def __init__(self):
        self.queue = []
        self.done = deque()

    def add(self, worker):
        self.queue.append(worker)

    def execute(self, current, **kwargs):

        current.preExecute()

        res = {}
        if kwargs:
            current.prepareWork(**kwargs)
            current.printDescription()
            res = current.execute(**kwargs)
        else:
            current.printDescription()
            res = current.execute()

        self.done.append(current)
        return res

    def start(self, **kwargs):
        res = {}
        while len(self.queue) > 0:
            current = self.queue.pop(0)
            if current is None:
                continue
            res = self.execute(current, **res)

        while len(self.done) > 0:
            current = self.done.pop()
            current.postExecute()
