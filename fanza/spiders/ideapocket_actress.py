from fanza.common import get_crawled, get_target
from fanza.items import ActressImageItem, IdeapocketActressItem, RequestStatusItem
from fanza.actress.ideapocket_actress_constants import *
from fanza.actress.ideapocket_actress_extract_helper import *
from fanza.actress.actress_common import build_flag, isUpdate, isGround, isTarget, isImage
from fanza.actress.actress_constants import *
from fanza.exceptions.fanza_exception import ExtractException
from fanza.exceptions.error_msg_constants import *

from scrapy import Spider, Request
from scrapy.http.response.html import HtmlResponse

class IdeapocketActressSpider(Spider):
    name = 'ideapocket_actress'
    allowed_domains = ['ideapocket.com']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.crawled = []
        self.flag = ACTRESS_AGGR_MODE
        self.request_callback = self.parse_detail

    def start_requests(self):
        mode = self.settings['IDEAPOCKET_ACTRESS_MODE']
        self.crawled = get_crawled(self.settings['IDEAPOCKET_ACTRESS_COMMITTED'])
        self.flag = build_flag(mode)
        if isImage(self.flag):
            self.request_callback = self.parse_image
        if isGround(self.flag):
            yield Request(IDEAPOCKET_ACTRESS_TOP, callback=self.parse)
        if isTarget(self.flag):
            ideapocket_actress_target = self.settings['IDEAPOCKET_ACTRESS_TARGET']
            for id in get_target(ideapocket_actress_target):
                if not isUpdate(self.flag) and id in self.crawled:
                    self.logger.info('ideapocket actress is already crawled -> id: %s', id)
                    continue
                url = IDEAPOCKET_ACTRESS_TARGET_FORMATTER.format(id)
                yield Request(
                    url,
                    callback=self.request_callback,
                    cb_kwargs=dict(id=id)
                )

    def parse(self, response: HtmlResponse):
        """ This function parse ideapocket actress top page.

        @url https://www.ideapocket.com/actress/
        @returns requests 12 24
        """
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", response.url)
        try:
            for url in ideapocket_actress_ground_extract(response):
                id = ideapcoket_actress_detail_extract_id(url)
                if not isUpdate(self.flag) and id in self.crawled:
                    self.logger.info('ideapocket actress is already crawled -> id: %s', id)
                    continue
                yield Request(url, callback=self.request_callback, cb_kwargs=dict(id=id))
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return

    def parse_detail(self, response: HtmlResponse, id):
        """ This function parse s1 actress detail page.

        @url https://www.ideapocket.com/actress/detail/1031805/
        @cb_kwargs {"id": "1031805"}
        @avbookreturns actressItem 1 imageItem 1
        @avbookscrapes actressItem {"id": 1031805, "actressName": "桃乃木かな"}
        """
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        try:
            name, en_name = ideapocket_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        birth = ideapocket_actress_detail_extract_profile(response, IDEAPOCKET_ACTRESS_DETAIL_BIRTH_TEXT)
        height = ideapocket_actress_detail_extract_profile(response, IDEAPOCKET_ACTRESS_DETAIL_HEIGHT_TEXT)
        three_size = ideapocket_actress_detail_extract_profile(response, IDEAPOCKET_ACTRESS_DETAIL_SIZE_TEXT),
        birth_place = ideapocket_actress_detail_extract_profile(response, IDEAPOCKET_ACTRESS_DETAIL_PLACE_TEXT)
        blood_type = ideapocket_actress_detail_extract_profile(response, IDEAPOCKET_ACTRESS_DETAIL_BLOOD_TEXT)
        hobby_trick = ideapocket_actress_detail_extract_profile(response, IDEAPOCKET_ACTRESS_DETAIL_HOBBYTRICK_TEXT)
        twitter = ideapocket_actress_detail_extract_sns(response, IDEAPOCKET_ACTRESS_DETAIL_TWITTER_TEXT)
        ins = ideapocket_actress_detail_extract_sns(response, IDEAPOCKET_ACTRESS_DETAIL_INS_TEXT)

        self.logger.info('id\t%s', id)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_BIRTH_TEXT, birth)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_HEIGHT_TEXT, height)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_SIZE_TEXT, three_size)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_PLACE_TEXT, birth_place)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_BLOOD_TEXT, blood_type)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_HOBBYTRICK_TEXT, hobby_trick)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_TWITTER_TEXT, twitter)
        self.logger.info('%s\t%s', IDEAPOCKET_ACTRESS_DETAIL_INS_TEXT, ins)

        yield IdeapocketActressItem(
            id=int(id),
            actressName=name, actressNameEn=en_name,
            birth=birth,
            height=height,
            threeSize=three_size,
            birthPlace=birth_place,
            bloodType=blood_type,
            hobbyTrick=hobby_trick,
            twitter=twitter,
            ins=ins
        )

        try:
            img_url = ideapocket_actress_extract_profile_img(response)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        
        yield ActressImageItem(
            url=img_url,
            subDir=IDEAPOCKET_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(id),
            imageName=IDEAPOCKET_ACTRESS_PROFILE_IMGNAME,
            actress=name,
            isUpdate=isUpdate(self.flag)
        )

    def parse_image(self, response: HtmlResponse):
        pass