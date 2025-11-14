import os
from os.path import abspath
from config import MAX_CHARS
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write data to a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path we are writing to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is going in the file.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    normalized_working_dir = os.path.abspath(working_directory)

    if not absolute_path.startswith(normalized_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(os.path.dirname(absolute_path)):
            os.makedirs(os.path.dirname(absolute_path))

        with open(absolute_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
