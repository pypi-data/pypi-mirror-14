from collections import deque


class WorkingQueue:

    def __init__(self):
        self.queue = []
        self.done = deque()

    def add(self, worker):
        self.queue.append(worker)

    def execute(self, current, **kwargs):
        current._printPreExecute()
        current.preExecute()

        res = {}
        if kwargs:
            current.prepareWork(**kwargs)
            current._printExecute()
            res = current.execute(**kwargs)
        else:
            res = current.execute()
            current._printExecute()

        self.done.append(current)

        return res

    def start(self, **kwargs):

        res = {}
        print("Starting workers...")
        while len(self.queue) > 0:
            current = self.queue.pop(0)
            if current is None:
                continue
            res = self.execute(current, **res)

        print("Cleaning...")

        while len(self.done) > 0:
            current = self.done.pop()
            current._printPostExecute()
            current.postExecute()

        print("Done...")
