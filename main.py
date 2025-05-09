from pathlib import Path
import hashlib
import json
from datetime import datetime

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

    def commit(self,message):
        with open(self.indexpath) as f:
            index = f.read()
        parent_commit = self.get_current_head()

        commit_data =str( {
            'date': str(datetime.now()),
            'message': message,
            'files': index,
            'parent': parent_commit
        }).encode()

        commit_hash = self.hash_object(commit_data)

        commit_folder_path=self.objectpath/commit_hash[:2]
        commit_folder_path.mkdir(parents=True, exist_ok=True)

        commit_file_path = commit_folder_path/commit_hash[2:]
        commit_file_path.write_text(commit_data.decode())

        self.headpath.write_text(commit_hash)
        self.indexpath.write_text('[]')


    def get_current_head(self):
        with open(self.headpath) as f:
            parent = f.read()
        return parent

obj = Ella()
obj.init()
obj.add('text1.txt')
obj.add('text2.txt')
obj.commit('first commit')