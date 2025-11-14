import os
from os.path import abspath
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Show the content of the file up to the first {MAX_CHARS} characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file for which the content is being shown.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    normalized_working_dir = os.path.abspath(working_directory)

    if not absolute_path.startswith(normalized_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # MAX_CHARS = 10000

        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            return (
                file_content_string
                + f"[...File {file_path} truncated at {MAX_CHARS} characters]"
            )
        return file_content_string

    except Exception as e:
        return f"Error: {e}"
