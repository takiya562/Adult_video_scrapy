from scrapy.http import HtmlResponse
from fanza.exceptions.fanza_exception import ExtractException
from fanza.actress.faleno_actress_constants import FALENO_ACTRESS_EN_NAME_REGEX
from re import search

def faleno_actress_ground_extract(response: HtmlResponse):
    hrefs = response.xpath('//ul[@class="clearfix"]/li/div/a/@href').getall()
    if len(hrefs) == 0:
        raise ExtractException("faleno actress page ground extract error", response.url)
    for url in hrefs:
        yield url

def faleno_actress_detail_extract_en_name(url: str):
    en_name_m = search(FALENO_ACTRESS_EN_NAME_REGEX, url)
    if en_name_m is None:
        raise ExtractException('illegal faleno actress detail page url', url)
    return en_name_m.group()

def faleno_actress_detail_extract_name(response: HtmlResponse):
    name = response.xpath('//div[@class="bar02"]/h1/text()').get()
    en_name = response.xpath('//div[@class="bar02"]/h1/span/text()').get()
    if name is None or en_name is None:
        raise ExtractException("extract faleno actress name error", response.url)
    return name, en_name

def faleno_actress_detail_extract_profile(response: HtmlResponse, meta_text: str):
    query = '//li[@class="clearfix"]/span[text()="{}"]/following-sibling::p/text()'.format(meta_text)
    return response.xpath(query).get()

def faleno_actress_extract_profile_img(response: HtmlResponse):
    img_url = response.xpath('//div[@class="box_actress02_left"]/img/@src').get()
    if img_url is None:
        raise ExtractException("extract faleno actress profile img error", response.url)
    return img_url