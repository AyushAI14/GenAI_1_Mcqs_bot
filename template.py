import os
from pathlib import Path

file_dir = 'src'

 
file_list = [
    f"{file_dir}/__init__.py",
    f"{file_dir}/Prompt/__init__.py",
    f"{file_dir}/utils/__init__.py",
    f"{file_dir}/utils/common.py",
    f"{file_dir}/logging/__init__.py",
    f"{file_dir}/pipeline/__init__.py",
    f"{file_dir}/llm/__init__.py",
    "data/mcq_store.csv",
    "config/config.yaml",
    "response.json",
    "app.py",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/"
]
try:
    for filepath in file_list:
        filepath = Path(filepath)
        filedir , filename = os.path.split(filepath)
        if filedir != '':
            os.makedirs(filedir,exist_ok=True)
        if (not os.path.exists(filepath) or (os.path.getsize==0)):
            with open(filepath,'w') as f:
                pass
except Exception as e:
    print('Error occured while creating files',e)
