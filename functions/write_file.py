import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content into the given file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we want to write into, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content we want to write into the file.",
            ),
        },
    ),
)

def write_file(file_name, content):
    working_directory="calculator"
    try:
        if file_name is None:
            return f'No file path'
        else:
            file_path = os.path.abspath(os.path.join(working_directory, file_name))
        # Check if the resolved path is outside the working directory
        work_dir_path = os.path.abspath(working_directory)
        if not file_path.startswith(work_dir_path):
            return f'Error: Cannot write to "{file_name}" as it is outside the permitted working directory'

        directory = os.path.dirname(file_path)
        if directory:  
            os.makedirs(directory, exist_ok=True)
            
        with open(file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_name}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: {e}'