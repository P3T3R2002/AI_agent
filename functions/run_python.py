import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we want to run, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(file_name):
    working_directory="calculator"
    try:
        work_dir_path = os.path.abspath(working_directory)
        if file_name is None:
            return f'No file path given'
        else:
            file_path = os.path.abspath(os.path.join(working_directory, file_name))
        # Check if the resolved path is outside the working directory
        if not file_path.startswith(work_dir_path):
            return f'Error: Cannot execute "{file_name}" as it is outside the permitted working directory'
        if not os.path.exists(file_path):
            return f'Error: File "{file_name}" not found.'
        if file_path[-3:] != ".py":
            return f'Error: "{file_name}" is not a Python file.'
        
    except Exception as e:
        return f'Error: {e}'
    
    try:
        sub_process = subprocess.run(["python3", file_path], timeout=30, capture_output=True)
        if sub_process.stdout.decode() == "" and sub_process.stderr.decode() == "":
            return "No output produced."
        ret_str = f"STDOUT: {sub_process.stdout.decode()}STDERR: {sub_process.stderr.decode()}\n"
        if sub_process.returncode != 0:
            ret_str += f"Process exited with code {sub_process.returncode}\n"

        return ret_str
        
    except Exception as e:
        return f"Error: executing Python file: {e}"