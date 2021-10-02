from scrapy.http.response.html import HtmlResponse
from fanza.fanza_exception import ExtractException
from re import search
from fanza.prestige_actress_constants import *

def prestige_actress_ground_extract(response: HtmlResponse):
    hrefs = response.xpath('//ul[@id="actress"]/li/a/@href').getall()
    if len(hrefs) == 0:
        raise ExtractException('prestige actress page ground extract error', response.url)
    for path in hrefs:
        yield PRESTIGE_DOMAIN + path

def prestige_actress_detail_extract_id(url: str):
    id_m = search(PRESTIGE_ACTRESS_ID_REGEX, url)
    if id_m is None:
        raise ExtractException('illegal prestige actress detail page url', url)
    return id_m.group()

def prestige_actress_detail_extract_name(response: HtmlResponse):
    name = response.xpath('//div[@id="actress_name"]/h1/text()').get()
    en_name = response.xpath('//div[@id="actress_name"]/h2/text()').get()
    if name is None or en_name is None:
        raise ExtractException("extract prestige actress name error", response.url)
    return name, en_name

def prestige_actress_detail_extract_profile(response: HtmlResponse, meta_text: str):
    xpath_str = '//dl[@class="prof_text"]/dt[contains(., "{}")]/text()'.format(meta_text)
    extract_regex = r'(?<={}：).*'.format(meta_text)
    return response.xpath(xpath_str).re_first(extract_regex)

def prestige_actress_detail_extract_sns(response: HtmlResponse, meta_text: str):
    return response.xpath('//img[@alt="{}"]/parent::a/@href'.format(meta_text)).get()

def prestige_actress_detail_extract_profile_image(response: HtmlResponse):
    img_url_path = response.xpath('//div[@id="actress_img"]/img/@src').get()
    if img_url_path is None:
        raise ExtractException('extract prestige actress profile img error', response.url)
    return PRESTIGE_DOMAIN + img_url_path
    