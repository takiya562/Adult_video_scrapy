from fanza.items import FalenoActressItem, ActressImageItem
from fanza.common import get_crawled, get_target
from fanza.actress.faleno_actress_constants import *
from fanza.actress.actress_constants import ACTRESS_AGGR_MODE
from fanza.actress.actress_common import build_flag, isUpdate, isImage, isGround, isTarget
from fanza.actress.faleno_actress_extract_helper import *
from fanza.exceptions.error_msg_constants import ACTRESS_RESPONSE_STATUS_ERROR_MSG, ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG

from scrapy import Spider, Request
from scrapy.http import HtmlResponse

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
                yield Request(
                    url,
                    callback=self.request_callback,
                    cb_kwargs=dict(name_id=en_name)
                )
                
        
    def parse(self, response: HtmlResponse):
        """ This function parse s1 actress top page.

        @url https://faleno.jp/top/actress/
        @returns requests 24 40
        """
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", response.url)
        for url in faleno_actress_ground_extract(response):
            en_name = faleno_actress_detail_extract_en_name(url)
            if not isUpdate(self.flag) and en_name in self.crawled:
                self.logger.info('faleno actress is already crawled -> en_name: %s', en_name)
                continue
            yield Request(
                url,
                callback=self.request_callback,
                cb_kwargs=dict(name_id=en_name)
            )

    def parse_detail(self, response: HtmlResponse, name_id):
        """ This function parse faleno actress detail page.

        @url https://faleno.jp/top/actress/arina_hashimoto/
        @cb_kwargs {"name_id": "arina_hashimoto"}
        @avbookreturns actressItem 1 imageItem 1
        @avbookscrapes actressItem {"id": "arina_hashimoto", "actressName": "橋本ありな"}
        """
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        name, en_name = faleno_actress_detail_extract_name(response)
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
        img_url = faleno_actress_extract_profile_img(response)
        yield ActressImageItem(
            url=img_url, subDir=FALENO_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(name_id),
            imageName=FALENO_ACTRESS_PROFILE_IMGNAME, actress=name,
            isUpdate=isUpdate(self.flag)
        )

    def parse_image(self, response: HtmlResponse, name_id):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        name, en_name = faleno_actress_detail_extract_name(response)
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        img_url = faleno_actress_extract_profile_img(response)
        yield ActressImageItem(
            url=img_url, subDir=FALENO_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(name_id),
            imageName=FALENO_ACTRESS_PROFILE_IMGNAME, actress=name,
            isUpdate=isUpdate(self.flag)
        )
