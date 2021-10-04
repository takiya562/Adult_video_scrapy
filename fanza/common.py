from os.path import isfile
from urllib.request import OpenerDirector, Request, urlopen

def save_crawled_to_file(record: str, file: str):
    with open(file, 'a', encoding='utf-8') as f:
        f.write(record + '\n')

def save_to_file(record: str, file: str):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(record + '\n')

def get_crawled(file: str):
    l = set()
    if not isfile(file):
        raise FileNotFoundError
    with open(file, 'r') as f:
        for line in f.readlines():
            l.add(line.replace('\n', ''))
    return l

def get_target(file: str):
    if not isfile(file):
        raise FileNotFoundError
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            yield line

def download_image(opener: OpenerDirector, url: str, des: str):
    CHUNK = 1024 * 1024
    resp = opener.open(url, timeout=30)
    with open(des, 'wb') as f:
        while True:
            chunk = resp.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
    resp.close()