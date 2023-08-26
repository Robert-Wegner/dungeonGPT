
import os

file_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def read_file(file_path):
    file_path = os.path.join(file_dir, file_path)
    file_path = os.path.abspath(os.path.realpath(file_path))
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    
def write_file(filepath, content):
    file_path = os.path.join(file_dir, file_path)
    file_path = os.path.abspath(os.path.realpath(file_path))
    try:
        with open(filepath, 'a') as file:
            file.write(content)
        return "Content written to file."
    except Exception as error:
        raise Exception(f"Error writing to file: {error}")

def overwrite_file(filepath, content):
    file_path = os.path.join(file_dir, file_path)
    file_path = os.path.abspath(os.path.realpath(file_path))
    try:
        with open(filepath, 'w+') as file:
            file.write(content)
        return "Content written to file."
    except Exception as error:
        raise Exception(f"Error writing to file: {error}")