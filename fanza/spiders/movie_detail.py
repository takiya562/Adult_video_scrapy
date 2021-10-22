from typing import Dict
from scrapy import Spider
from scrapy.http import HtmlResponse
from fanza.movie.impl.fanza_amateur_extractor import FanzaAmateurExtractor
from fanza.movie.impl.fanza_extractor import FanzaExtractor
from fanza.movie.impl.mgs_extractor import MgstageExtractor
from fanza.movie.impl.sod_extractor import SodExtractor
from fanza.movie.movie_extractor import MovieExtractor

class MovieDetailSpider(Spider):
    name = 'movie_detail'
    allowed_domains = ['dmm.co.jp', 'mgstage.com', 'ec.sod.co.jp']
    extractors: Dict[str, MovieExtractor] = {
        'fanza': FanzaExtractor(),
        'fanza_amateur': FanzaAmateurExtractor(),
        'mgstage': MgstageExtractor(),
        'sod': SodExtractor()
    }

    def start_requests(self):
        pass

    def parse(self, response: HtmlResponse, censored_id, store):
        # """ This function parse fanza movie page.

        # @url https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=cawd00186/
        # @cb_kwargs {"censored_id": "CAWD-186", "store": "fanza"}
        # @cookies {"age_check_done": "1"}
        # """
        # """ This function parse fanza amateur movie page.

        # @url https://www.dmm.co.jp/digital/videoc/-/detail/=/cid=yaho012/
        # @cb_kwargs {"censored_id": "YAHO-012", "store": "fanza_amateur"}
        # @cookies {"age_check_done": "1"}
        # """
        # """ This function parse mgstage movie page.

        # @url https://www.mgstage.com/product/product_detail/ABW-013/
        # @cb_kwargs {"censored_id": "ABW-013", "store": "mgstage"}
        # @cookies {"adc": "1"}
        # """
        """ This function parse sod movie page.
        
        @url https://ec.sod.co.jp/prime/videos/?id=STARS-449
        @cb_kwargs {"censored_id": "STARS-449", "store": "sod"}
        @meta {"store": "sod"}
        """
        extractor = self.extractors.get(store, None)
        if extractor is None:
            return
        res = extractor.extract(response)
        self.logger.info("id: %s", censored_id)
        self.logger.info("movie info: %s", res)
