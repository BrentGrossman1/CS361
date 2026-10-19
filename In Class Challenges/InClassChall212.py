# PurePosixPath was a suggestion from Claud ai when i asked it:
# "how would you use python url parse to get just the extension off of a input path?"
from pathlib import PurePosixPath
import mimetypes

# get_extension returns the extension from a given path
def get_extension(path):
    return PurePosixPath(path).suffix

# get_mime_type returns the mime type from a given file extension
def get_mime_type(extension):
    mime_type, encoding = mimetypes.guess_type("file" + extension)
    return mime_type

paths = [
    "/",
    "/foo", 
    "/bar.txt", 
    "/baz/foo/bar.gif", 
    "/baz/foo/bar.foo.jpg",
]

extensions = [
    "",
    ".txt",
    ".html",
    ".gif",
    ".jpg",
]

print("Part 1: Get the File Extension")
for path in paths:
    print(f"Input:  {path}\nOutput: {get_extension(path)}\n")

print("Part 2: Get the MIME Type")
for extension in extensions:
    print(f"Input:  {extension}\nOutput: {get_mime_type(extension)}\n")






