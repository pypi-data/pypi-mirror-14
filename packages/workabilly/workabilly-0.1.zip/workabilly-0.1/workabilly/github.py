from .downloader import Downloader

import shutil


class GithubArchiveGrabber(Downloader):

    def _buildUrl(self):
        archive = self.tag
        if archive is None:
            archive = self.branch

        format_str = ("https://github.com/%s/%s/archive/%s.zip")
        return format_str % (self.user, self.project, archive)

    def __init__(self, **kwargs):
        self.user = kwargs.get('user')
        self.project = kwargs.get('project')
        self.tag = kwargs.get('tag')
        self.branch = kwargs.get('branch', 'master')
        self.target = kwargs.get('target', './')

        super().__init__(source=self._buildUrl(), target=self.target)

    def preExecuteDescription(self):
        return 'Creating Temporary Folder ' + self.target

    def postExecuteDescription(self):
        return 'Deleting Temporary Folder ' + self.target

    def executeDescription(self):
        return 'Downloading ' + self.project

    def execute(self, **kwargs):
        return {'archive': super().execute(**kwargs).get('downloaded')}

    def postExecute(self):
        shutil.rmtree(self.target)
