from pathlib import Path
import hashlib
import json
from datetime import datetime
import difflib

class Ella:
    def __init__(self):
        self.repopath = Path.cwd()/'.ella'
        self.objectpath = self.repopath/'objects'
        self.indexpath = self.repopath/'index'
        self.headpath = self.repopath/'HEAD'

    def init(self):
        if not self.repopath.is_dir():
            self.repopath.mkdir(exist_ok = True)
            self.objectpath.mkdir(parents = True,exist_ok=True)
            self.indexpath.write_text("[]")
            self.headpath.write_text('')
            print('repository initialized')
        else:
            print('repository reintialized')

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
        index = json.loads(index)
        parent_commit = self.get_current_head()

        commit_data ={
            'date': str(datetime.now()),
            'message': message,
            'files': index,
            'parent': parent_commit
        }
        commit_data_encoded = json.dumps(commit_data).encode()

        commit_hash = self.hash_object(commit_data_encoded)

        commit_folder_path=self.objectpath/commit_hash[:2]
        commit_folder_path.mkdir(parents=True, exist_ok=True)

        commit_file_path = commit_folder_path/commit_hash[2:]
        commit_file_path.write_text(commit_data_encoded.decode())

        self.headpath.write_text(commit_hash)
        self.indexpath.write_text('[]')


    def get_current_head(self):
        with open(self.headpath) as f:
            parent = f.read()
        return parent 
    
    def log(self):
        current_commit_hash = self.get_current_head()
        while(current_commit_hash):
            with open(self.objectpath / current_commit_hash[:2] / current_commit_hash[2:]) as f:
                commit_data = json.load(f)
            # commit_data = json.load(self.objectpath/current_commit_hash[:2]/current_commit_hash[2:])
            print(f'commit : {current_commit_hash}\n Date:{commit_data.get('date')}\n\n {commit_data.get('message')}')

            current_commit_hash = commit_data.get('parent')

    def show_diff(self,commit_hash):
        commit_data = self.get_commit_data(commit_hash)
        
        if not commit_data:
            print('commit not found ')
            return
        print('changes in the last commit')

        files = commit_data.get('files', [])
        if not isinstance(files, list):  # Ensure `files` is a list
            print(f"Invalid files structure in commit: {files}")
            return

        for file in files:
            if not isinstance(file, dict):  # Ensure each file is a dictionary
                print(f"Invalid file entry: {file}")
                continue
            print(f'file:{file}')
            file_content = self.get_file_content(file.get('file_hash'),file.get('folder_hash'))
            print(file_content)

            if commit_data.get('parent'):
                parent_commit_data = self.get_commit_data(commit_data.get('parent'))
                if parent_commit_data:
                    parent_file = self.get_parent_file_content(parent_commit_data, file.get('file_path'))
                    if parent_file is None:
                        print(f"No matching parent file found for file_hash: {file.get('file_hash')} and folder_hash: {file.get('folder_hash')}")
                    else:
                        self.print_git_style_diff(parent_file, file_content)

            else: print(file_content)
                


    
    def get_parent_file_content(self,parent_commit_data,file_path):
        parent_file = parent_commit_data.get('files')
        for file in parent_file:
            if file_path == file.get('file_path'):
                return self.get_file_content(file.get('file_hash'),file.get('folder_hash'))
            

    def get_file_content(self, file_hash, folder_hash):
        file_path = self.objectpath / folder_hash / file_hash
        with open(file_path, 'r') as f:
            try:
                file_content = json.load(f)  # Try to load as JSON
            except json.JSONDecodeError:
                f.seek(0)  # Reset file pointer
                file_content = f.read()  # Read as plain text
        return file_content

    
    def get_commit_data(self,commit_hash):
        try:
            with open(self.objectpath / commit_hash[:2] / commit_hash[2:], 'r') as f:
                commit_data = json.load(f)
            if 'files' in commit_data and isinstance(commit_data['files'],str):
                commit_data['files'] = json.loads(commit_data['files'])
            return commit_data
        except FileNotFoundError:
            return None
        
    @staticmethod
    def print_git_style_diff(old_text, new_text, filename="file.txt"):
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm=''
        )

        for line in diff:
            print(line)

if __name__ == '__main__':
    obj = Ella()
    obj.init()
    obj.add('text1.txt')
    obj.commit('first commit')
    obj.add('text2.txt')
    obj.commit('second commit')
    obj.log()
    obj.show_diff("a2bce7c0a680245f3e69711bbe742afc6d8a5ef8")