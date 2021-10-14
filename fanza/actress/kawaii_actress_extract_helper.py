from fanza.actress.actress_error_msg_constants import EXTRACT_ACTRESS_NAME_ERROR, EXTRACT_ACTRESS_PROFILE_IMG_ERROR, GROUND_EXTRACT_ERROR, ILLEGAL_ACTRESS_DETAIL_PAGE_URL
from fanza.exceptions.fanza_exception import ExtractException
from fanza.actress.kawaii_actress_constants import KAWAII_ACTRESS_ID_REGEX, KAWAII_BASE_URL

from scrapy.http import HtmlResponse

from re import search

MAKER = 'kawaii'

def kawaii_actress_ground_extract(response: HtmlResponse):
    hrefs = response.xpath('//div[@class="p-area-list"]/ul/li/a/@href').getall()
    if len(hrefs) == 0:
       raise ExtractException(GROUND_EXTRACT_ERROR, MAKER)
    for url_path in hrefs:
        yield KAWAII_BASE_URL + url_path

def kawaii_actress_detail_extract_id(url: str):
    id_m = search(KAWAII_ACTRESS_ID_REGEX, url)
    if id_m is None:
        raise ExtractException(ILLEGAL_ACTRESS_DETAIL_PAGE_URL, MAKER)
    return id_m.group()

def kawaii_actress_detail_extract_name(response: HtmlResponse):
    name = response.xpath('//h1[@class="tx-actress-name"]/text()').get()
    name_en = response.xpath('//p[@class="tx-actress"]/text()').get()
    if name is None or name_en is None:
        raise ExtractException(EXTRACT_ACTRESS_NAME_ERROR, MAKER)
    return name, name_en

def kawaii_actress_detail_extract_profile(response: HtmlResponse, meta_text: str):
    query = '//dt[text()="{}"]/following-sibling::dd[1]/text()'.format(meta_text)
    info_text = response.xpath(query).get()
    if info_text == '----':
        return None
    return info_text

def kawaii_actress_detail_extract_sns(response: HtmlResponse, meta_class: str):
    query = '//a[@class="{}"]/@href'.format(meta_class)
    return response.xpath(query).get()

def kawaii_actress_detail_extract_profile_img(response: HtmlResponse):
    img_url_path = response.xpath('//div[@class="area-image js-tile"]/img/@src').get()
    if img_url_path is None:
        raise ExtractException(EXTRACT_ACTRESS_PROFILE_IMG_ERROR, MAKER)
    return KAWAII_BASE_URL + img_url_path
