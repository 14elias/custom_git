from pathlib import Path
import hashlib

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

    @staticmethod
    def hash_object(file):
        return hashlib.sha1(file).hexdigest()

    def add(self,file):
        with open(file,'rb') as f:
            content = f.read()
        header = f"blob{len(content)}/0".encode()
        hash1_object = self.hash_object(header + content)
        newfilepath = self.objectpath/hash1_object
        newfilepath.write_text(content.decode())
        print(f'{file} added')

obj = Ella()
obj.add('text1.txt')