from fanza.movie.movie_constants import *
from fanza.exceptions.fanza_exception import ExtractException, EmptyGenreException, FormatException
from fanza.image.img_url_factory import mgs_low_res_cover_url_factory

from scrapy.http.response.html import HtmlResponse

from os.path import splitext, isfile, join
from os import listdir
from re import search

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

def fanza_format_video_len(video_len: str):
    # regex '\d+(?=\b)' can not match correctly, don't know why
    m = search(r'\d+(?=\B)', video_len)
    if m:
        return int(m.group())
    else:
        raise ExtractException('format video len failed')


def fanza_extract_multi_info(response: HtmlResponse, meta_info: str):
    ids = response.xpath(f'//a[@data-i3pst="{meta_info}"]/@href').re(r'(?<=id=)\d*')
    if len(ids) == 0:
        return {}
    texts = response.xpath(f'//a[@data-i3pst="{meta_info}"]/text()').getall()
    if len(ids) != len(texts):
        raise ExtractException('{} meta count mismatch, id: {} name: {}', meta_info, len(ids), len(texts))
    res = dict()
    for i in range(0, len(ids)):
        if not ids[i].isdigit():
            continue
        res[ids[i]] = texts[i]
    return res

def fanza_extract_video_info(response: HtmlResponse, info_x: str):
    id = response.xpath(f'//a[@data-i3pst="{info_x}"]/@href').re_first(r'(?<=id=)\d*')
    if id is None:
        return None, None
    name = response.xpath(f'//a[@data-i3pst="{info_x}"]/text()').get()
    return int(id), name

def fanza_extract_meta_info(response: HtmlResponse, tag_text: str):
    text = response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{tag_text}")]/following-sibling::td/text()').get()
    if text is None:
        raise ExtractException('extract {} failed', tag_text)
    return text.replace('\n', '')

def fanza_extract_preview_image(response: HtmlResponse, censored_id: str):
    img_src = response.xpath('//div[@id="sample-image-block"]/a/img/@src').getall()
    if len(img_src) == 0:
       raise ExtractException('can not find any preview image of {}', censored_id)
    return img_src

def fanza_extract_cover_image(response: HtmlResponse, censored_id: str):
    high_res_img_href = response.xpath('//div[@class="center"]/a[@name="package-image"]/@href').get()
    low_res_img_src = response.xpath('//a[@name="package-image"]/img/@src').get()
    if high_res_img_href is None or low_res_img_src is None:
        raise ExtractException('can not find cover image of {}', censored_id)
    return low_res_img_src, high_res_img_href

def fanza_amateur_extract_cover_image(response: HtmlResponse, censored_id: str):
    img_src = response.xpath('//div[@id="sample-video"]/img/@src').get()
    if img_src is None:
        raise ExtractException('can not find cover image of {}', censored_id)
    return img_src

def mgs_clean_text(text: str):
    if text is None:
        return text
    return MGS_FORMAT_REGEX.sub(MGS_SUB_STR, text)

def mgs_clean_title(title: str):
    return MGS_TITLE_SUB_REGEX.sub(MGS_SUB_STR, mgs_clean_text(title))

def mgs_extract_title(response: HtmlResponse):
    title = response.xpath('//h1[@class="tag"]/text()').re_first(r'\n\s*(.*)\n\s*')
    if title is None:
        raise ExtractException('extract title failed')
    return title

def msg_extract_multi_info(response: HtmlResponse, meta_text: str):
    return response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/a/text()').re(r'\n\s*(.*)\n\s*')

def mgs_extract_video_info(response: HtmlResponse, meta_text: str):
    return response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/a/text()').re_first(r'\n\s*(.*)\n\s*')

def mgs_extract_meta_info(response: HtmlResponse, meta_text: str):
    return response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/text()').get()

def msg_extract_video_len(response: HtmlResponse):
    video_len = response.xpath('//th[contains(., "収録時間")]/following-sibling::td/text()').re_first(r'\d+(?=min)')
    if video_len is None:
        raise ExtractException('extract video len of failed')
    return int(video_len)

def mgs_extract_preview_image(response: HtmlResponse):
    high_res_href = response.xpath('//a[@class="sample_image"]/@href').getall()
    low_res_href = response.xpath('//a[@class="sample_image"]/img/@src').getall()
    if len(low_res_href) != len(high_res_href):
        raise ExtractException('count of low-res and hi-res preview image mismatch')
    for i in range(0, len(low_res_href)):
        yield {MSG_HIGH_RES_IMG_URL_KEY: high_res_href[i], MGS_LOW_RES_IMG_URL_KEY: low_res_href[i]}

def mgs_extract_cover_image(response: HtmlResponse, censored_id: str):
    low_res_src = response.xpath('//img[@class="enlarge_image"]/@src').get()
    if low_res_src is None:
        raise ExtractException('can not find cover image')
    high_res_scr = MGS_COVER_URL_SUB_REGEX.sub(MGS_COVER_URL_SUB_STR, low_res_src)
    return high_res_scr, mgs_low_res_cover_url_factory.get_url(low_res_src, censored_id)

def mgs_extract_preview_num(url: str, low_res: int):
    preview_name_m = search(r'(?<=\/)[^\/]*(?=\.jpg)', url)
    if preview_name_m is None:
        raise ExtractException('preview image name is illegal, url: {}', url)
    preview_name = preview_name_m.group()
    if low_res:
        num_m = search(MGS_LOW_RES_PREVIEW_REGEX, preview_name)
    else:
        num_m = search(MGS_HIGH_RES_PREVIEW_REGEX, preview_name)
    if num_m is None:
        raise ExtractException('preview image num is illegal, url: {}', url)
    return num_m.group()
