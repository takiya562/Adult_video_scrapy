from os.path import isfile
from urllib.request import OpenerDirector, Request
from os.path import splitext, isfile, join
from os import listdir
from re import search

def save_crawled_to_file(record: str, file: str):
    with open(file, 'a', encoding='utf-8') as f:
        f.write(record + '\n')

def save_to_file(record: str, file: str):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(record + '\n')

def get_crawled(file: str):
    l = set()
    with open(file, 'r') as f:
        for line in f.readlines():
            l.add(line.replace('\n', ''))
    return l

def get_image_fail(file: str):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            yield line.replace('\n', '')

def scan_movie_dir(dir: str, ext_list: list):
    for item in listdir(dir):
        if isfile(join(dir, item)):
            filename, file_extension = splitext(item)
            if file_extension in ext_list:
                yield filename

def get_target(file: str):
    if not isfile(file):
        raise FileNotFoundError
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            yield line

def download_image(opener: OpenerDirector, url: str, des: str):
    CHUNK = 1024 * 1024
    if search(r'cloudfront', url):
        req = Request(url, headers={'Referer': 'https://ec.sod.co.jp/'})
    else:
        req = Request(url)
    resp = opener.open(req, timeout=30)
    with open(des, 'wb') as f:
        while True:
            chunk = resp.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
    resp.close()

def normalize_space(s: str):
    return ' '.join(s.split()) if s else None