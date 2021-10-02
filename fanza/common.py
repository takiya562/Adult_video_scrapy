from os.path import isfile

def save_crawled_to_file(record: str, file: str):
    if not isfile(file):
        raise FileNotFoundError
    with open(file, 'a', encoding='utf-8') as f:
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