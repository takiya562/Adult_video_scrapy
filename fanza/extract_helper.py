from fanza.constants import *
from fanza.fanza_exception import ExtractException, EmptyGenreException, FormatException
from os.path import splitext, isfile, join
from os import listdir
from re import search

def save_crawled_to_file(censored_id: str, file: str):
    if not isfile(file):
        raise FileNotFoundError
    with open(file, 'a') as f:
        f.write(censored_id + '\n')

def scan_video_dir(dir: str, ext_list: list):
    for item in listdir(dir):
        if isfile(join(dir, item)):
            filename, file_extension = splitext(item)
            if file_extension in ext_list:
                yield filename

def black_list_filter(genre: str, black_list: list):
    for g in black_list:
        if search(g, genre):
            return False
    return True

def get_crawled(file: str):
    l = []
    if not isfile(file):
        raise FileNotFoundError
    with open(file, 'r') as f:
        for line in f.readlines():
            l.append(line.replace('\n', ''))
    return l

def format_censored_id(censored_id: str):
    if censored_id is None:
        raise FormatException('censored id is none!')
    return censored_id.replace('-', '00').lower()


def format_image_name(img_name: str):
    return FANZA_IMAGE_NAME_SUB_REGEX.sub(FANZA_IMAGE_NAME_SUB_STR, img_name).upper()


def fanza_format_video_len(video_len: str):
    # regex '\d+(?=\b)' can not match correctly, don't know why
    m = search(r'\d+(?=\B)', video_len)
    if m:
        return int(m.group())
    else:
        raise FormatException('video len format error!')


def fanza_extract_actress_info(response):
    tag_a = response.xpath('//a[@data-i3pst="{}"]/@href'.format(FANZA_ACTRESS_INFO))
    if len(tag_a) == 0:
        return {}
    a_hrefs = tag_a.getall()
    tag_a_textes = response.xpath('//a[@data-i3pst="{}"]/text()'.format(FANZA_ACTRESS_INFO))
    if len(tag_a_textes) != len(tag_a):
        raise ExtractException("count of actress name and actress id do not match", response.url)
    a_textes = tag_a_textes.getall()
    actress = {}
    for i in range(0, len(tag_a)):
        a_href = a_hrefs[i]
        a_text = a_textes[i]
        m = search(r'(?<=id=)\d*', a_href)
        if m is None:
            raise ExtractException("match id info of `%s` failed" % FANZA_ACTRESS_INFO, response.url)
        actress[m.group()] = a_text
    return actress


def fanza_extract_video_info(response, info_x: str):
    tag_a = response.xpath('//a[@data-i3pst="{}"]/@href'.format(info_x))
    if len(tag_a) == 0:
        return None, None
    if tag_a is None or len(tag_a) != 1:
        raise ExtractException('encounter multiple %s or %s is null' % (info_x, info_x), response.url)
    a_href = tag_a.get()
    m = search(r'(?<=id=)\d*', a_href)
    if m is None:
        raise ExtractException("match id info of `%s` failed" % info_x, response.url)
    id_info = m.group()
    tag_a_text = response.xpath('//a[@data-i3pst="{}"]/text()'.format(info_x))
    if tag_a_text is None or len(tag_a_text) != 1:
        raise ExtractException('encounter multiple %s or %s is null' % (info_x, info_x), response.url)
    name_info = tag_a_text.get()
    return int(id_info), name_info


def fanza_extract_meta_info(response, tag_text: str):
    tag_td_text = response.xpath('//table[@class="mg-b20"]//tr[contains(., "{}")]/td[2]/text()'.format(tag_text))
    if tag_td_text is None or len(tag_td_text) != 1:
        raise ExtractException('encounter multiple %s tag or %s tag is null' % (tag_text, tag_text), response.url)
    return tag_td_text.get().replace('\n', '')


def fanza_extract_genre_info(response):
    genre_a_textes = response.xpath('//table[@class="mg-b20"]//tr[contains(., "{}")]/td/a/text()'.format(GENRE_INFO))
    if len(genre_a_textes) == 0:
        raise EmptyGenreException('genre list is empty', response.url)
    a_textes = genre_a_textes.getall()
    genre_a_hrefs = response.xpath('//table[@class="mg-b20"]//tr[contains(., "{}")]/td/a/@href'.format(GENRE_INFO))
    if len(a_textes) != len(genre_a_hrefs):
        raise ExtractException("coun of genre id and genre name do not match", response.url)
    a_hrefs = genre_a_hrefs.getall()
    genre = {}
    for i in range(0, len(a_textes)):
        a_href = a_hrefs[i]
        genre_name = a_textes[i]
        m = search(r'(?<=id=)\d*', a_href)
        if m and black_list_filter(genre_name, FANZA_BLACK_GENRE_LIST):
            genre[m.group()] = genre_name
    return genre

def mgs_format_text(text: str):
    if text is None:
        raise FormatException('None text cannot be formatted!')
    return MGS_FORMAT_REGEX.sub(MGS_SUB_STR, text)

def mgs_clean_title(title: str):
    return MGS_TITLE_SUB_REGEX.sub(MGS_SUB_STR, mgs_format_text(title))

def mgs_extract_video_info(response, th_text: str):
    tag_a = response.xpath('//tr/th[contains(., "{}")]/following-sibling::td/a/text()'.format(th_text))
    if len(tag_a) == 0:
        return None
    if len(tag_a) != 1:
        raise ExtractException('encounter multiple %s or %s is null' % (th_text, th_text), response.url)
    tag_a_text = tag_a.get()
    try:
        tag_a_text = mgs_format_text(tag_a_text)
    except FormatException as err:
        raise err
    return tag_a_text

def mgs_extract_meta_info(response, th_text: str):
    tag_td = response.xpath('//tr/th[contains(., "{}")]/following-sibling::td/text()'.format(th_text))
    if len(tag_td) == 0:
        return None
    if len(tag_td) != 1:
        raise ExtractException('encounter multiple %s or %s is null' % (th_text, th_text), response.url)
    return tag_td.get()

def mgs_format_video_len(video_len: str):
    m = search(r'\d+(?=min)', video_len)
    if m:
        return m.group()
    else:
        raise FormatException('video len format error!')
