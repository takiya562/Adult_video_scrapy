from fanza.common import get_crawled, get_target
from fanza.items import ActressImageItem, KawaiiActressItem
from fanza.exceptions.error_msg_constants import *
from fanza.exceptions.fanza_exception import ExtractException
from fanza.actress.actress_common import build_flag, isUpdate, isGround, isTarget, isImage
from fanza.actress.actress_constants import *
from fanza.actress.kawaii_actress_constants import *
from fanza.actress.kawaii_actress_extract_helper import *

from scrapy import Spider
from scrapy.http import HtmlResponse, Request


class KawaiiActressSpider(Spider):
    name = 'kawaii_actress'
    allowed_domains = ['kawaiikawaii.jp']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.crawled = []
        self.flag = ACTRESS_AGGR_MODE
        self.request_callback = self.parse_detail
    
    def start_requests(self):
        mode = self.settings['KAWAII_ACTRESS_MODE']
        self.crawled = get_crawled(self.settings['KAWAII_ACTRESS_COMMITTED'])
        self.flag = build_flag(mode)
        if isImage(self.flag):
            self.request_callback = self.parse_image
        if isGround(self.flag):
            yield Request(KAWAII_ACTRESS_TOP, callback=self.parse)
        if isTarget(self.flag):
            kawaii_actress_target = self.settings['KAWAII_ACTRESS_TARGET']
            for id in get_target(kawaii_actress_target):
                if not isUpdate(self.flag) and id in self.crawled:
                    self.logger.info('kawaii actress is already crawled -> id: %s', id)
                    continue
                yield Request(
                    KAWAII_ACTRESS_TARGET_FORMATTER.format(id),
                    callback=self.request_callback,
                    cb_kwargs=dict(id=id)
                )

    def parse(self, response: HtmlResponse):
        """ This function parse kawaii actress top page.

        @url https://www.kawaiikawaii.jp/actress/
        @returns requests 15 30
        """
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", response.url)
        for url in kawaii_actress_ground_extract(response):
            id = kawaii_actress_detail_extract_id(url)
            if not isUpdate(self.flag) and id in self.crawled:
                self.logger.info('kawaii actress is already crawled -> id: %s', id)
                continue
            yield Request(
                url,
                callback=self.request_callback,
                cb_kwargs=dict(id=id)
            )

    def parse_detail(self, response: HtmlResponse, id):
        """ This function parse kawaii actress detail page.

        @url https://www.kawaiikawaii.jp/actress/detail/1042907/
        @cb_kwargs {"id": "1042907"}
        @avbookreturns actressItem 1 ImageItem 1
        @avbookscrapes actressItem {"id": 1042907, "actressName": "伊藤舞雪"}
        """
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        try:
            name, en_name = kawaii_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        birth = kawaii_actress_detail_extract_profile(response, KAWAII_ACTRESS_DETAIL_BIRTH_TEXT)
        height = kawaii_actress_detail_extract_profile(response, KAWAII_ACTRESS_DETAIL_HEIGHT_TEXT)
        three_size = kawaii_actress_detail_extract_profile(response, KAWAII_ACTRESS_DETAIL_SIZE_TEXT)
        trick = kawaii_actress_detail_extract_profile(response, KAWAII_ACTRESS_DETAIL_TRICK_TEXT)
        hobby = kawaii_actress_detail_extract_profile(response, KAWAII_ACTRESS_DETAIL_HOBBY_TEXT)
        twitter = kawaii_actress_detail_extract_sns(response, KAWAII_ACTRESS_DETAIL_TWITTER_TEXT)
        ins = kawaii_actress_detail_extract_sns(response, KAWAII_ACTRESS_DETAIL_INS_TEXT)
        self.logger.info("id\t%s", id)
        self.logger.info("%s\t%s", KAWAII_ACTRESS_DETAIL_BIRTH_TEXT, birth)
        self.logger.info("%s\t%s", KAWAII_ACTRESS_DETAIL_HEIGHT_TEXT, height)
        self.logger.info("%s\t%s", KAWAII_ACTRESS_DETAIL_SIZE_TEXT, three_size)
        self.logger.info("%s\t%s", KAWAII_ACTRESS_DETAIL_TRICK_TEXT, trick)
        self.logger.info("%s\t%s", KAWAII_ACTRESS_DETAIL_HOBBY_TEXT, hobby)
        self.logger.info("%s\t%s", KAWAII_ACTRESS_DETAIL_TWITTER_TEXT, twitter)
        self.logger.info("%s\t%s", KAWAII_ACTRESS_DETAIL_INS_TEXT, ins)
        yield KawaiiActressItem(
            id=int(id),
            actressName=name, actressNameEn=en_name,
            birth=birth,
            height=height,
            threeSize=three_size,
            trick=trick,
            hobby=hobby,
            twitter=twitter,
            ins=ins
        )
        try:
            img_url = kawaii_actress_detail_extract_profile_img(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        yield ActressImageItem(
            url=img_url,
            subDir=KAWAII_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(id),
            imageName=KAWAII_ACTRESS_PROFILE_IMGNAME,
            isUpdate=isUpdate(self.flag),
            actress=name,
        )

    def parse_image(self, response: HtmlResponse, id):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        try:
            name, en_name = kawaii_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        try:
            img_url = kawaii_actress_detail_extract_profile_img(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        yield ActressImageItem(
            url=img_url,
            subDir=KAWAII_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(id),
            imageName=KAWAII_ACTRESS_PROFILE_IMGNAME,
            isUpdate=isUpdate(self.flag),
            actress=name,
        )
