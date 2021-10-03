from re import I
from scrapy import Spider, Request
from scrapy.http import HtmlResponse
from fanza.actress_constants import *
from fanza.actress_common import build_flag, isUpdate, isImage, isGround, isTarget
from fanza.common import get_crawled, get_target
from fanza.faleno_actress_constants import *
from fanza.error_msg_constants import *
from fanza.faleno_actress_extract_helper import *
from fanza.items import FalenoActressItem, ActressImageItem


class FalenoActressSpider(Spider):
    name = 'faleno_actress'
    allowed_domains = ['faleno.jp']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.crawled = []
        self.flag = ACTRESS_AGGR_MODE
        self.request_callback = self.parse_detail

    def start_requests(self):
        mode = self.settings['PRESTIGE_ACTRESS_MODE']
        self.crawled = get_crawled(self.settings['PRESTIGE_ACTRESS_COMMITTED'])
        self.flag = build_flag(mode)
        if isImage(self.flag):
            self.request_callback = self.parse_image
        if isGround(self.flag):
            yield Request(FALENO_ACTRESS_TOP, callback=self.parse)
        if isTarget(self.flag):
            faleno_actress_target = self.settings['FALENO_ACTRESS_TARGET']
            for en_name in get_target(faleno_actress_target):
                if not isUpdate(self.flag) and en_name in self.crawled:
                    self.logger.info('faleno actress is already crawled')
                    continue
                url = FALENO_ACTRESS_TARGET_FORMATTER.format(en_name)
                yield Request(url, callback=self.request_callback, meta={FALENO_ACTRESS_NAME_ID_META_KEY: en_name})
                
        
    def parse(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", response.url)
        try:
            for url in faleno_actress_ground_extract(response):
                en_name = faleno_actress_detail_extract_en_name(url)
                if not isUpdate(self.flag) and en_name in self.crawled:
                    self.logger.info('actress is already crawled -> en_name: %s', en_name)
                    continue
                yield Request(url, callback=self.request_callback, meta={FALENO_ACTRESS_NAME_ID_META_KEY: en_name})
        except ExtractException as err:
            self.logger.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return

    def parse_detail(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        name_id = response.meta[FALENO_ACTRESS_NAME_ID_META_KEY]
        try:
            name, en_name = faleno_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        birth = faleno_actress_detail_extract_profile(response, FALENO_ACTRESS_DETAIL_BIRTH_TEXT)
        birth_place = faleno_actress_detail_extract_profile(response, FALENO_ACTRESS_DETAIL_PLACE_TEXT)
        height = faleno_actress_detail_extract_profile(response, FALENO_ACTRESS_DETAIL_HEIGHT_TEXT)
        three_size = faleno_actress_detail_extract_profile(response, FALENO_ACTRESS_DETAIL_SIZE_TEXT)
        hobby = faleno_actress_detail_extract_profile(response, FALENO_ACTRESS_DETAIL_HOBBY_TEXT)
        trick = faleno_actress_detail_extract_profile(response, FALENO_ACTRESS_DETAIL_TRICK_TEXT)
        self.logger.info("%s\t%s", FALENO_ACTRESS_DETAIL_BIRTH_TEXT, birth)
        self.logger.info("%s\t%s", FALENO_ACTRESS_DETAIL_PLACE_TEXT, birth_place)
        self.logger.info("%s\t%s", FALENO_ACTRESS_DETAIL_HEIGHT_TEXT, height)
        self.logger.info("%s\%s", FALENO_ACTRESS_DETAIL_SIZE_TEXT, three_size)
        self.logger.info("%s\t%s", FALENO_ACTRESS_DETAIL_HOBBY_TEXT, hobby)
        self.logger.info("%s\t%s", FALENO_ACTRESS_DETAIL_TRICK_TEXT, trick)
        yield FalenoActressItem(
            id=name_id,
            actressName=name, actressNameEn=en_name,
            birth=birth, birthPlace=birth_place,
            height=height, threeSize=three_size,
            hobby=hobby, trick=trick
        )
        try:
            img_url = faleno_actress_extract_profile_img(response)
            yield ActressImageItem(
                url=img_url, subDir=FALENO_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(name_id),
                imageName=FALENO_ACTRESS_PROFILE_IMGNAME, actress=name,
                isUpdate=isUpdate(self.flag)
            )
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return

    def parse_image(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        name_id = response.meta[FALENO_ACTRESS_NAME_ID_META_KEY]
        try:
            name, en_name = faleno_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        try:
            img_url = faleno_actress_extract_profile_img(response)
            yield ActressImageItem(
                url=img_url, subDir=FALENO_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(name_id),
                imageName=FALENO_ACTRESS_PROFILE_IMGNAME, actress=name,
                isUpdate=isUpdate(self.flag)
            )
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
