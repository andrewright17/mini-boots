import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
from config import SYSTEM_PROMPT, MODEL_NAME
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

functions_dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    kwargs = function_call_part.args if function_call_part.args is not None else {}
    kwargs["working_directory"] = "./calculator"

    function = functions_dict.get(function_call_part.name, 0)
    if function == 0:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    function(**kwargs)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function(**kwargs)},
            )
        ],
    )


if len(sys.argv) < 2:
    print("Error: No propmpt provided.")
    sys.exit(1)
user_prompt = sys.argv[1]

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

model_name = MODEL_NAME

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=SYSTEM_PROMPT
    ),
)

try:
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(
                function_call_part, verbose="--verbose" in sys.argv
            )
            if "--verbose" in sys.argv:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)
except Exception as e:
    raise Exception(f"Error: {e}")

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
