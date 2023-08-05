

class BaseWorker:

    def __init__(self, **kwargs):
        self.next = None
        self.verbose = kwargs.get('verbose', True)

    def printDescription(self):
        if self.verbose:
            print(self.executeDescription())

    def prepareWork(self, **kwargs):
        '''Override this to retrieve arguments before work starts'''

    def executeDescription(self):
        '''Override this to print a description of the job'''

    def preExecute(self):
        '''Gets called before the actual work is done'''

    def execute(self, **kwargs):
        '''Override this to do the deed'''

    def postExecute(self):
        '''Gets called after self and next are done'''
