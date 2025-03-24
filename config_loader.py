import os
import json

def load_config(file_name: str):
    path = os.path.join(os.path.dirname(__file__), 'config', file_name)
    with open(path, 'r') as f:
        return json.load(f)
