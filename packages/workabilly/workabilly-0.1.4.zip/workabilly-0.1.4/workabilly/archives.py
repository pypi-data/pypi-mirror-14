from .base.workers import BaseWorker

import os
import zipfile


class Unzipper(BaseWorker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target = kwargs.get('target')

    def executeDescription(self):
        return 'Extracting ' + self.source + ' to ' + self.target

    def prepareWork(self, **kwargs):
        self.source = kwargs.get('archive')

    def preExecute(self):
        if not os.path.exists(self.target):
            os.makedirs(self.target)

    def execute(self, **kwargs):
        with zipfile.ZipFile(self.source, "r") as z:
            z.extractall(self.target)

    def postExecute(self):
        os.remove(self.source)
