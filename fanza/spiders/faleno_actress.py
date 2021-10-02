from scrapy import Spider, Request
from scrapy.http import HtmlResponse
from fanza.actress_constants import *
from fanza.actress_common import build_flag, isUpdate, isImage, isGround, isTarget
from fanza.common import get_crawled, get_target
from fanza.faleno_actress_constants import *
from fanza.error_msg_constants import *


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
                yield Request(url, callback=self.request_callback)
                
        
    def parse(self, response: HtmlResponse):
        if response.status == 404 or response.status == 302:
            self.logger.error(ACTRESS_RESPONSE_STATUS_ERROR_MSG, self.name, response.url)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", response.url)

    def parse_detail(self, response: HtmlResponse):
        pass

    def parse_image(self, response: HtmlResponse):
        pass
