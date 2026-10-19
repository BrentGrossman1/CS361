
from urllib.parse import urlsplit 

def get_url_path(url):
    return urlsplit(url).path

urlStrings = [
    "https://example.com/",
    "https://example.com/foo",
    "https://example.com/bar.txt",
    "https://example.com/baz/foo/bar.git",
]

for url in urlStrings:
    print(f"Input:  {url}\nOutput: {get_url_path(url)}\n")