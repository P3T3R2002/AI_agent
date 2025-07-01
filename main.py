import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
import functions.get_files_info 
import functions.get_file_content
import functions.write_file
import functions.run_python

available_functions = types.Tool(
    function_declarations=[
        functions.get_files_info.schema_get_files_info,
        functions.get_file_content.schema_get_file_content,
        functions.write_file.schema_write_file,
        functions.run_python.schema_run_python,
    ]
)
available_functions_map = {
    "get_files_info": functions.get_files_info.get_files_info,
    "get_file_content": functions.get_file_content.get_file_content,
    "run_python_file": functions.run_python.run_python_file,
    "write_file": functions.write_file.write_file
}

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    flag = False
    if len(sys.argv) == 1:
        print("Prompt not provided!")
        exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--verbose":
            print("Prompt not provided!")
            exit(1)
    elif len(sys.argv) == 3:
        if sys.argv[2] != "--verbose":
            print("Wrong second argument.")
            exit(1)
        else:
            flag = True
    
    prompt = sys.argv[1]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [ types.Content(role="user", parts=[types.Part(text=prompt)]) ]
    
    for _ in range(1, 20):
        response = generate_content(client, messages)

        for candidate in response.candidates:
            messages.append(candidate.content)

        if not response.function_calls:
            print(response.text)
            break   

        for call in response.function_calls:
            result = call_function(call, flag)
            if not result.parts[0].function_response.response:
                raise SystemError 
            elif flag:
                print(f"-> {result.parts[0].function_response.response['result']}")
            messages.append(result)

#--------------------------------------------------------------------------

def generate_content(client, messages):
    return client.models.generate_content(  model='gemini-2.0-flash-001', 
                                                contents=messages,
                                                config=types.GenerateContentConfig(
                                                    tools=[available_functions], system_instruction=system_prompt
                                                )
                                            )
    
#--------------------------------------------------------------------------

def call_function(function_call_part, verbose=False):
    if function_call_part.name not in available_functions_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": available_functions_map[function_call_part.name](**function_call_part.args)},
                )
            ],
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": available_functions_map[function_call_part.name](**function_call_part.args)},
                )
            ],
        )

if __name__ == "__main__":
    main()
