from scrapy.http.response.html import HtmlResponse
from fanza.exceptions.fanza_exception import ExtractException
from re import search
from fanza.actress.s1_actress_constants import *

def s1_actress_ground_extract(response: HtmlResponse):
    hrefs = response.xpath('//p[text()="{}"]/following::div[@class="c-card main"]/descendant::a/@href'.format(S1_ACTRESS_TITLE)).getall()
    if len(hrefs) == 0:
        raise ExtractException("s1 actress page ground extract error", response.url)
    for url in hrefs:
        yield url

def s1_actress_detail_extract_name(response: HtmlResponse):
    name = response.xpath('//h2[@class="top anime__show__item -bottom c-main-font c-main-bg-after"]/text()').get()
    en_name = response.xpath('//p[@class="bottom anime__show__item -bottom delay"]/text()').get()
    if name is None or en_name is None:
        raise ExtractException("extract s1 actress name error", response.url)
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
        raise ExtractException('illegal s1 actress detail page url', url)
    return id_m.group()

def s1_actress_extract_profile_img(response: HtmlResponse):
    img_url = response.xpath('//img[@class="u-hidden--sp lazyload"]/@data-src').get()
    if img_url is None:
        raise ExtractException("extract s1 actress profile img error", response.url)
    return img_url

def s1_actress_extract_gallery(response: HtmlResponse):
    gallery_img_urls = response.xpath('//div[@class="p-profile__sign"]/div/img/@data-src').getall()
    if gallery_img_urls is None:
        raise ExtractException("extract s1 actress gallery img error", response.url)
    return gallery_img_urls
