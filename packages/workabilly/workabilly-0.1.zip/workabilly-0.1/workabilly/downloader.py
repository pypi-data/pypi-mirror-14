from .base.workers import BaseWorker

import os
import wget


class Downloader(BaseWorker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source')
        self.target = kwargs.get('target', './')

    def preExecute(self):
        if not os.path.exists(self.target):
            os.makedirs(self.target)

    def execute(self, **kwargs):
        result = wget.download(self.source, out=self.target)
        return {'downloaded': result}
