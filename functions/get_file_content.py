import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Writes out the contents of the given file with a maximum of 10000 character, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we want to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(file_name):
    working_directory="calculator"
    try:
        work_dir_path = os.path.abspath(working_directory)
        if file_name is None:
            return f'No file path'
        else:
            file_path = os.path.abspath(os.path.join(working_directory, file_name))
        # Check if the resolved path is outside the working directory
        if not file_path.startswith(work_dir_path):
            return f'Error: Cannot read "{file_name}" as it is outside the permitted working directory'
        if os.path.isdir(file_path):
            return f'Error: File not found or is not a regular file: "{file_name}"'
        
        MAX_CHARS = 10000

        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f" ...File {file_name} truncated at 10000 characters"
            return file_content_string
    
    except Exception as e:
        return f'Error: {e}'