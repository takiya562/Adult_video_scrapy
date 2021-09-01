from logging import info
from fanza.constants import *
from fanza.fanza_exception import ExtractException, EmptyGenreException, FormatException
from os.path import splitext, isfile, join
from os import listdir
from re import search
from scrapy.http.response.html import HtmlResponse

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


def fanza_extract_multi_info(response: HtmlResponse, info_x: str):
    tag_a = response.xpath('//a[@data-i3pst="{}"]/@href'.format(info_x))
    if len(tag_a) == 0:
        return {}
    a_hrefs = tag_a.getall()
    tag_a_textes = response.xpath('//a[@data-i3pst="{}"]/text()'.format(info_x))
    if len(tag_a_textes) != len(tag_a):
        raise ExtractException("count of %s name and %s id do not match", info_x, info_x, response.url)
    a_textes = tag_a_textes.getall()
    multi_info = {}
    for i in range(0, len(tag_a)):
        a_href = a_hrefs[i]
        a_text = a_textes[i]
        m = search(r'(?<=id=)\d*', a_href)
        if m is None:
            raise ExtractException("match id info of `%s` failed" % info_x, response.url)
        multi_info[m.group()] = a_text
    return multi_info


def fanza_extract_video_info(response: HtmlResponse, info_x: str):
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


def fanza_extract_meta_info(response: HtmlResponse, tag_text: str):
    tag_td_text = response.xpath('//table[@class="mg-b20"]//tr[contains(., "{}")]/td[2]/text()'.format(tag_text))
    if tag_td_text is None or len(tag_td_text) != 1:
        raise ExtractException('encounter multiple %s tag or %s tag is null' % (tag_text, tag_text), response.url)
    return tag_td_text.get().replace('\n', '')


def fanza_extract_genre_info(response: HtmlResponse):
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

def fanza_extract_preview_image(response: HtmlResponse, censored_id: str):
    img_src = response.xpath('//a[@name="sample-image"]/img/@src').getall()
    if len(img_src) == 0:
       raise ExtractException('can not find any preview image of %s!' % censored_id, response.url)
    for url in img_src:
        yield url

def fanza_extract_cover_image(response: HtmlResponse, censored_id: str):
    low_res_img_href = response.xpath('//div[@class="center"]/a[@name="package-image"]/@href').get()
    high_res_img_src = response.xpath('//a[@name="package-image"]/img/@src').get()
    if low_res_img_href is None or high_res_img_src is None:
        raise ExtractException('can not find cover image of %s!' % censored_id, response.url)
    return high_res_img_src, low_res_img_href

def mgs_clean_text(text: str):
    if text is None:
        return text
    return MGS_FORMAT_REGEX.sub(MGS_SUB_STR, text)

def mgs_clean_title(title: str):
    return MGS_TITLE_SUB_REGEX.sub(MGS_SUB_STR, mgs_clean_text(title))

def mgs_extract_video_info(response: HtmlResponse, th_text: str):
    tag_a = response.xpath('//tr/th[contains(., "{}")]/following-sibling::td/a/text()'.format(th_text))
    if len(tag_a) == 0:
        return None
    if len(tag_a) != 1:
        raise ExtractException('encounter multiple %s or %s is null' % (th_text, th_text), response.url)
    tag_a_text = tag_a.get()
    try:
        tag_a_text = mgs_clean_text(tag_a_text)
    except FormatException as err:
        raise err
    return tag_a_text

def mgs_extract_meta_info(response: HtmlResponse, th_text: str):
    tag_td = response.xpath('//tr/th[contains(., "{}")]/following-sibling::td/text()'.format(th_text))
    if len(tag_td) == 0:
        return None
    if len(tag_td) != 1:
        raise ExtractException('encounter multiple %s or %s is null' % (th_text, th_text), response.url)
    return tag_td.get()

def mgs_format_video_len(video_len: str):
    if video_len is None:
        return video_len
    m = search(r'\d+(?=min)', video_len)
    if m:
        return m.group()
    else:
        raise FormatException('video len format error!')

def mgs_extract_genre_info(response: HtmlResponse):
    tag_a = response.xpath('//tr/th[contains(., "{}")]/following-sibling::td/a/text()'.format(GENRE_INFO))
    if len(tag_a) == 0:
        return []
    genre = []
    a_textes = tag_a.getall()
    for text in a_textes:
        text = mgs_clean_text(text)
        if black_list_filter(text, MGS_BLACK_GENRE_LIST):
            genre.append(text)
    return genre

def mgs_extract_preview_image(response: HtmlResponse, censored_id: str):
    high_res_href = response.xpath('//a[@class="sample_image"]/@href').getall()
    low_res_href = response.xpath('//a[@class="sample_image"]/img/@src').getall()
    if len(low_res_href) != len(high_res_href):
        raise ExtractException('low-res and hi-res preview image count of %s does not match!' % censored_id, response.url)
    for i in range(0, len(low_res_href)):
        yield {'high_res_url': high_res_href[i], 'low_res_url': low_res_href[i]}

def mgs_extract_cover_image(response: HtmlResponse, censored_id: str):
    low_res_src = response.xpath('//img[@class="enlarge_image"]/@src').get()
    if low_res_src is None:
        raise ExtractException('can not find cover image of %s' % censored_id, response.url)
    high_res_scr = MGS_COVER_URL_SUB_REGEX.sub(MGS_COVER_URL_SUB_STR, low_res_src)
    return high_res_scr, low_res_src

def mgs_extract_preview_num(url: str, censored_id: str, low_res: int):
    preview_name_m = search(r'(?<=\/)[^\/]*(?=\.jpg)', url)
    if preview_name_m is None:
        raise ExtractException('preview image name of %s is illegal' % censored_id, url)
    preview_name = preview_name_m.group()
    if low_res:
        num_m = search(MGS_LOW_RES_PREVIEW_REGEX, preview_name)
    else:
        num_m = search(MGS_HIGH_RES_PREVIEW_REGEX, preview_name)
    if num_m is None:
        raise ExtractException('preview image num of %s is illegal' % censored_id, url)
    return num_m.group()
