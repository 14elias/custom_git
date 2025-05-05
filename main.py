from pathlib import Path

class Ella:
    def __init__(self):
        self.repopath = Path.cwd()/'.ella'
        self.objectpath = self.repopath/'objects'
        self.indexpath = self.repopath/'index'
        self.headpath = self.repopath/'head'
    def init(self):
        self.repopath.mkdir(exist_ok = True)
        self.objectpath.mkdir(parents = True)
        self.indexpath.write_text('')
        self.headpath.write_text('')
        print('repository initialized')


obj = Ella()
obj.init()