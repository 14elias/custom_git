from pathlib import Path
import hashlib
import json

class Ella:
    def __init__(self):
        self.repopath = Path.cwd()/'.ella'
        self.objectpath = self.repopath/'objects'
        self.indexpath = self.repopath/'index'
        self.headpath = self.repopath/'HEAD'

    def init(self):
        self.repopath.mkdir(exist_ok = True)
        self.objectpath.mkdir(parents = True,exist_ok=True)
        self.indexpath.write_text("[]")
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

        new_folder_path = self.objectpath/hash1_object[:2]
        new_folder_path.mkdir(parents=True,exist_ok=True)

        new_file_path = new_folder_path/hash1_object[2:]
        new_file_path.write_text(content.decode())

        self.update_staging_area(file,hash1_object[:2],hash1_object[2:])
        print(f'{file} added')
    
    def update_staging_area(self, file_path,folder_hash, file_hash):
        with open(self.indexpath, 'r') as f:
            content = f.read()
        index = json.loads(content)
        index.append({"file_path":file_path,"folder_hash":folder_hash, "file_hash":file_hash})
        self.indexpath.write_text(json.dumps(index))

obj = Ella()
obj.add('text1.txt')