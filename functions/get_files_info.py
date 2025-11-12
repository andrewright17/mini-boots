import os
from os.path import abspath


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
