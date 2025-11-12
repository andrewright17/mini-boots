import os
from os.path import abspath
from config import MAX_CHARS
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    normalized_working_dir = os.path.abspath(working_directory)

    if not absolute_path.startswith(normalized_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(absolute_path):
        return f'Error: File "{file_path}" not found.'

    if not absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", absolute_path]
        if args:
            for arg in args:
                commands.append(arg)

        completed_process = subprocess.run(commands, capture_output=True, timeout=30)

        return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
