from fanza.exceptions.fanza_exception import ExtractException
from fanza.actress.ideapocket_actress_constants import *
from fanza.actress.actress_error_msg_constants import *

from scrapy.http import HtmlResponse

from re import search

MAKER = 'ideapocket'

def ideapocket_actress_ground_extract(response: HtmlResponse):
    hrefs = response.xpath('//ul[@class="c-person-list"][2]/li/a/@href').getall()
    if len(hrefs) == 0:
        raise ExtractException(GROUND_EXTRACT_ERROR.format(maker=MAKER), response.url)
    for url_path in hrefs:
        yield IDEAPOCKET_ACTRESS_BASE_URL + url_path

def ideapocket_actress_detail_extract_name(response: HtmlResponse):
    name = response.xpath('//p[@class="actress-detail-name"]/text()').re_first(r'[^\s\n]+')
    en_name = response.xpath('//p[@class="actress-detail-name"]/span/text()').get()
    if name is None or en_name is None:
        raise ExtractException(EXTRACT_ACTRESS_NAME_ERROR.format(maker=MAKER), response.url)
    return name, en_name

def ideapocket_actress_detail_extract_profile(response: HtmlResponse, meta_text: str):
    query = f'//dt[contains(., "{meta_text}")]/following-sibling::dd/text()'
    profile_text = response.xpath(query).get()
    if profile_text is not None:
        profile_text = profile_text.strip()
        profile_text = IDEAPOCKET_ACTRESS_CLEAN_REGEX.sub(' ', profile_text)
    return profile_text

def ideapocket_actress_detail_extract_sns(response: HtmlResponse, sns: str):
    query = f'//li[@class="actress-detail-sns-item actress-detail-sns-item--{sns}"]/a/@href'
    sns_href = response.xpath(query).get()
    return sns_href

def ideapcoket_actress_detail_extract_id(url: str):
    id_m = search(IDEAPOCKET_ACTRESS_ID_REGEX, url)
    if id_m is None:
        raise ExtractException(ILLEGAL_ACTRESS_DETAIL_PAGE_URL.format(maker=MAKER), url)
    return id_m.group()

def ideapocket_actress_extract_profile_img(response: HtmlResponse):
    img_url_path = response.xpath('//div[@class="actress-detail-image"]/img/@src').get()
    if img_url_path is None:
        raise ExtractException(EXTRACT_ACTRESS_PROFILE_IMG_ERROR.format(maker=MAKER), response.url)
    return IDEAPOCKET_ACTRESS_BASE_URL + img_url_path
