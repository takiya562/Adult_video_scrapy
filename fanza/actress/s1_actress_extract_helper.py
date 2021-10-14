from fanza.exceptions.fanza_exception import ExtractException
from fanza.actress.s1_actress_constants import *
from fanza.actress.actress_error_msg_constants import *

from scrapy.http import HtmlResponse

from re import search

MAKER = 's1'

def s1_actress_ground_extract(response: HtmlResponse):
    hrefs = response.xpath('//p[text()="{}"]/following::div[@class="c-card main"]/descendant::a/@href'.format(S1_ACTRESS_TITLE)).getall()
    if len(hrefs) == 0:
        raise ExtractException(GROUND_EXTRACT_ERROR, MAKER)
    return hrefs

def s1_actress_detail_extract_name(response: HtmlResponse):
    name = response.xpath('//h2[@class="top anime__show__item -bottom c-main-font c-main-bg-after"]/text()').get()
    en_name = response.xpath('//p[@class="bottom anime__show__item -bottom delay"]/text()').get()
    if name is None or en_name is None:
        raise ExtractException(EXTRACT_ACTRESS_NAME_ERROR, MAKER)
    return name, en_name

def s1_actress_detail_extract_profile(response: HtmlResponse, info: str):
    info_text = response.xpath('//div[@class="p-profile__info"]//p[text()="{}"]/following-sibling::p/text()'.format(info)).get()
    if info_text is not None:
        info_text = S1_ACTRESS_PROFILE_CLEAN_REGEX.sub(S1_ACTRESS_PROFILE_CLEAN_STR, info_text)
    return info_text

def s1_actress_detail_extract_sns(response: HtmlResponse, sns_index: int):
    sns = response.xpath('//div[@class="sns"]/div/a[{}]/@href'.format(sns_index)).get()
    return sns

def s1_actress_detail_extract_id(url: str):
    id_m = search(S1_ACTRESS_ID_REGEX, url)
    if id_m is None:
        raise ExtractException(ILLEGAL_ACTRESS_DETAIL_PAGE_URL.format(maker=MAKER), url)
    return id_m.group()

def s1_actress_extract_profile_img(response: HtmlResponse):
    img_url = response.xpath('//img[@class="u-hidden--sp lazyload"]/@data-src').get()
    if img_url is None:
        raise ExtractException(EXTRACT_ACTRESS_PROFILE_IMG_ERROR, MAKER)
    return img_url

def s1_actress_extract_gallery(response: HtmlResponse):
    gallery_img_urls = response.xpath('//div[@class="p-profile__sign"]/div/img/@data-src').getall()
    if gallery_img_urls is None:
        raise ExtractException("extract s1 actress gallery img error")
    return gallery_img_urls
