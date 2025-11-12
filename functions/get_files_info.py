import os
from os.path import abspath
from config import MAX_CHARS


def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))
    normalized_working_dir = os.path.abspath(working_directory)

    if not absolute_path.startswith(normalized_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'

    contents = os.listdir(absolute_path)
    file_sizes = [
        os.path.getsize(os.path.join(absolute_path, file)) for file in contents
    ]
    file_types = [os.path.isdir(os.path.join(absolute_path, file)) for file in contents]

    return "\n".join(
        f"- {content}: {size} bytes, is_dir={file_type}"
        for content, size, file_type in zip(contents, file_sizes, file_types)
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
