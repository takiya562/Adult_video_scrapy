from fanza.common import get_crawled, get_target
from fanza.items import ActressImageItem, PrestigeActressItem
from fanza.exceptions.error_msg_constants import *
from fanza.exceptions.fanza_exception import ExtractException
from fanza.actress.prestige_actress_constants import *
from fanza.actress.prestige_actress_extract_helper import *
from fanza.actress.actress_common import build_flag, isUpdate, isGround, isTarget, isImage
from fanza.actress.actress_constants import *

from scrapy import Spider
from scrapy_splash import SplashRequest
from scrapy.http.response.html import HtmlResponse

class PrestigeActressSpider(Spider):
    name = 'prestige_actress'
    allowed_domains = ['prestige-av.com']
    

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.crawled = []
        self.flag = ACTRESS_AGGR_MODE
        self.request_callback = self.parse_detail
        self.lua_script = """
        function main(splash, args)
        splash:add_cookie{"age_auth", "1", "/", domain=".prestige-av.com"}
        splash.images_enabled = false
        splash.js_enabled = true
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return {
          html = splash:html()
        }
        end
        """

    def start_requests(self):
        mode = self.settings['PRESTIGE_ACTRESS_MODE']
        self.flag = build_flag(mode)
        self.crawled = get_crawled(self.settings['PRESTIGE_ACTRESS_COMMITTED'])
        if isImage(self.flag):
            self.request_callback = self.parse_image
        if isGround(self.flag):
            yield SplashRequest(
                url=PRESTIGE_ACTRESS_TOP,
                endpoint='execute',
                args={'lua_source': self.lua_script},
                callback=self.parse
            )
        if isTarget(self.flag):
            prestige_atress_target = self.settings['PRESIIGE_ACTRESS_TARGET']
            for id in get_target(prestige_atress_target):
                if not isUpdate(self.flag) and id in self.crawled:
                    self.logger.info('prestige actress is already crawled -> id: %s', id)
                    continue
                yield SplashRequest(
                    url=PRESTIGE_ACTRESS_TARGET_FORMATTER.format(id),
                    endpoint='execute',
                    args={'lua_source': self.lua_script},
                    meta={PRESTIGE_ACTRESSID_META_KEY: id},
                    callback=self.parse_detail
                )

    def parse(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", response.url)
        try:
            for url in prestige_actress_ground_extract(response):
                id = prestige_actress_detail_extract_id(url)
                if not isUpdate(self.flag) and id in self.crawled:
                    self.logger.info('actress is already crawled -> id: %s', id)
                    continue
                yield SplashRequest(
                    url=PRESTIGE_ACTRESS_TARGET_FORMATTER.format(id),
                    endpoint='execute',
                    args={'lua_source': self.lua_script},
                    meta={PRESTIGE_ACTRESSID_META_KEY: id},
                    callback=self.parse_detail
                )
        except ExtractException as err:
            self.logger.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return

    def parse_detail(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        id = response.meta[PRESTIGE_ACTRESSID_META_KEY]
        try:
            name, en_name = prestige_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        birth_place = prestige_actress_detail_extract_profile(response, PRESTIGE_ACTRESS_DETAIL_PLACE_TEXT)
        birth = prestige_actress_detail_extract_profile(response, PRESTIGE_ACTRESS_DETAIL_BIRTH_TEXT)
        blood_type = prestige_actress_detail_extract_profile(response, PRESTIGE_ACTRESS_DETAIL_BLOOD_TYPE_TEXT)
        height = prestige_actress_detail_extract_profile(response, PRESTIGE_ACTRESS_DETAIL_HEIGHT_TEXT)
        three_size = prestige_actress_detail_extract_profile(response, PRESTIGE_ACTRESS_DETAIL_SIZE_TEXT)
        hobby_trick = prestige_actress_detail_extract_profile(response, PRESTIGE_ACTRESS_DETAIL_HOBBY_TRICK_TEXT)
        twitter = prestige_actress_detail_extract_sns(response, PRESTIGE_ACTRESS_DETAIL_TWITTER_TEXT)
        ins = prestige_actress_detail_extract_sns(response, PRESTIGE_ACTRESS_DETAIL_INS_TEXT)
        self.logger.info('id\t%s', id)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_PLACE_TEXT, birth_place)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_BIRTH_TEXT, birth)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_BLOOD_TYPE_TEXT, blood_type)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_HEIGHT_TEXT, height)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_SIZE_TEXT, three_size)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_HOBBY_TRICK_TEXT, hobby_trick)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_TWITTER_TEXT, twitter)
        self.logger.info('%s\t%s', PRESTIGE_ACTRESS_DETAIL_INS_TEXT, ins)
        yield PrestigeActressItem(
            id=id, actressName=name, actressNameEn=en_name,
            birth=birth, height=height,
            birthPlace=birth_place, threeSize=three_size,
            bloodType=blood_type, hobbyTrick=hobby_trick,
            twitter=twitter, ins=ins
        )
        try:
            img_url = prestige_actress_detail_extract_profile_image(response)
        except ExtractException as err:
            self.logger.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        yield ActressImageItem(
            url=img_url, subDir=PRESTIGE_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(id),
            imageName=S1_ACTRESS_PROFILE_IMGNAME, isUpdate=isUpdate(self.flag), actress=name
        )


    def parse_image(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_DETAIL_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        id = response.meta[PRESTIGE_ACTRESSID_META_KEY]
        try:
            name, en_name = prestige_actress_detail_extract_name(response)
        except ExtractException as err:
            self.logger.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract actress %s(%s) information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', name, en_name)
        try:
            img_url = prestige_actress_detail_extract_profile_image(response)
        except ExtractException as err:
            self.logger.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        yield ActressImageItem(
            url=img_url, subDir=PRESTIGE_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER.format(id),
            imageName=S1_ACTRESS_PROFILE_IMGNAME, isUpdate=isUpdate(self.flag), actress=name
        )

