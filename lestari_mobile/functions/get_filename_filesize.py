import os

def execute(fullpath):
    return os.stat(fullpath).st_size