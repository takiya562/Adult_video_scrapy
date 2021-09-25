from fanza.extract_helper import get_crawled
from fanza.items import ActressImageItem, S1ActressItem
from fanza.s1_actress_constants import *
from fanza.error_msg_constants import S1_ACTRESS_RESPONSE_STATUS_ERROR_MSG, EXTRACT_GLOBAL_ERROR_MSG
from scrapy import Spider, Request
from scrapy.http.response.html import HtmlResponse
from fanza.s1_actress_extract_helper import *

class S1ActressSpider(Spider):
    name = 's1_actress'
    allowed_domains = ['s1s1s1.com']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.crawled = None

    def start_requests(self):
        mode = self.settings['S1_ACTRESS_MODE']
        self.crawled = get_crawled(self.settings['S1_ACTRESS_COMMITTED'])
        if mode == S1_ACTRESS_TOP_GROUND_MODE or mode == S1_ACTRESS_AGGR_MODE:
            yield Request(S1_ACTRESS_TOP, callback=self.parse)
        if mode == S1_ACTRESS_TARGET_MODE or mode == S1_ACTRESS_AGGR_MODE:
            s1_actress_target = self.settings['S1_ACTRESS_TARGET']
            with open(s1_actress_target, 'r') as f:
                for id in f.readlines():
                    id = id.replace('\n', '')
                    if id in self.crawled:
                        self.logger.info('actress is already crawled -> id: %s', id)
                        continue
                    url = S1_ACTRESS_TARGET_FORMATTER.format(id)
                    yield Request(url, callback=self.parse_detail, meta={S1_ACTRESSID_META_KEY: id})

    def parse(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(S1_ACTRESS_RESPONSE_STATUS_ERROR_MSG, response.url)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", response.url)
        try:
            for url in s1_actress_ground_extract(response):
                id = s1_actress_detail_extract_id(url)
                if id in self.crawled:
                    self.logger.info('actress is already crawled -> id: %s', id)
                    continue
                yield Request(url, callback=self.parse_detail, meta={S1_ACTRESSID_META_KEY: id})
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return

    def parse_detail(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.exception(S1_ACTRESS_RESPONSE_STATUS_ERROR_MSG, response.url)
            return
        id = response.meta[S1_ACTRESSID_META_KEY]
        try:
            name, en_name = s1_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        try:
            birth = s1_actress_detail_extract_profile(response, S1_ACTRESS_DETAIL_BIRTH_TEXT)
            height = s1_actress_detail_extract_profile(response, S1_ACTRESS_DETAIL_HEIGHT_TEXT)
            three_size = s1_actress_detail_extract_profile(response, S1_ACTRESS_DETAIL_SIZE_TEXT)
            birth_palce = s1_actress_detail_extract_profile(response, S1_ACTRESS_DETAIL_PLACE_TEXT)
            blood_type = s1_actress_detail_extract_profile(response, S1_ACTRESS_DETAIL_BLOOD_TYPE_TEXT)
            hobby = s1_actress_detail_extract_profile(response, S1_ACTRESS_DETAIL_HOBBY_TEXT)
            trick = s1_actress_detail_extract_profile(response, S1_ACTRESS_DETAIL_TRICK_TEXT)
            twitter = s1_actress_detail_extract_sns(response, S1_ACTRESS_TWITTER_INDEX)
            ins = s1_actress_detail_extract_sns(response, S1_ACTRESS_INS_INDEX)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('id\t%s', id)
        self.logger.info('%s\t%s', S1_ACTRESS_DETAIL_BIRTH_TEXT, birth)
        self.logger.info('%s\t%s', S1_ACTRESS_DETAIL_HEIGHT_TEXT, height)
        self.logger.info('%s\t%s', S1_ACTRESS_DETAIL_SIZE_TEXT, three_size)
        self.logger.info('%s\t%s', S1_ACTRESS_DETAIL_PLACE_TEXT, birth_palce)
        self.logger.info('%s\t%s', S1_ACTRESS_DETAIL_BLOOD_TYPE_TEXT, blood_type)
        self.logger.info('%s\t%s', S1_ACTRESS_DETAIL_HOBBY_TEXT, hobby)
        self.logger.info('%s\t%s', S1_ACTRESS_DETAIL_TRICK_TEXT, trick)
        self.logger.info('twitter\t%s', twitter)
        self.logger.info('ins\t%s', ins)
        yield S1ActressItem(
            id, name, en_name,
            birth, height, three_size,
            birth_palce, blood_type, hobby, trick,
            twitter, ins
        )
        try:
            img_url = s1_actress_extract_profile_img(response)
            yield ActressImageItem(img_url, id, S1_ACTRESS_PROFILE_IMGNAME, name)
            gallery_img_urls = s1_actress_extract_gallery(response)
            for i in range(0, len(gallery_img_urls)):
                yield ActressImageItem(gallery_img_urls[i], id, S1_ACTRESS_GALLERY_IMGNAME_FORMATTER.format(i + 1), name, 1)   
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
