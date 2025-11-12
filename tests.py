from os import write
from functions.get_files_info import get_file_content, write_file
import sys


print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

sys.exit(0)
