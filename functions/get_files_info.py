import os 
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(directory=None):
    working_directory="calculator"
    try:
        work_dir_path = os.path.abspath(working_directory)
        if directory is None:
            dir_path = work_dir_path
        else:
            dir_path = os.path.abspath(os.path.join(working_directory, directory))
        # Check if the resolved path is outside the working directory
        if not dir_path.startswith(work_dir_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(dir_path):
            return f'Error: "{directory}" is not a directory'
    
        dir = os.listdir(dir_path)
        ret_str = ""
        for file in dir:
            file_path = os.path.join(dir_path, file)
            ret_str = f"{ret_str}- {file}: file_size={get_size(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"
        return ret_str
    except Exception as e:
        return f'Error: {e}'


def get_size(dir):
    if not os.path.isdir(dir):
        return os.path.getsize(dir)
    size = 0
    list = os.listdir(dir)
    for file in list:
        size += get_size(os.path.join(dir, file))
    return size
