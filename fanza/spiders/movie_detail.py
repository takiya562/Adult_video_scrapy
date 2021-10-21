from scrapy import Spider
from scrapy.http import HtmlResponse
from fanza.movie.impl.fanza_amateur_extractor import FanzaAmateurExtractor
from fanza.movie.impl.fanza_extractor import FanzaExtractor
from fanza.movie.impl.mgs_extractor import MgstageExtractor

class MovieDetailSpider(Spider):
    name = 'movie_detail'
    allowed_domains = ['dmm.co.jp']
    extractors = {
        'fanza': FanzaExtractor(),
        'fanza_amateur': FanzaAmateurExtractor(),
        'mgstage': MgstageExtractor()
    }

    def parse(self, response: HtmlResponse, censored_id, store):
        """ This function parse fanza movie page.

        @url https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=cawd00186/
        @cb_kwargs {"censored_id": "CAWD-186", "store": "fanza"}
        @cookies {"age_check_done": "1"}
        """
        """ This function parse fanza amateur movie page.

        @url https://www.dmm.co.jp/digital/videoc/-/detail/=/cid=yaho012/
        @cb_kwargs {"censored_id": "YAHO-012", "store": "fanza_amateur"}
        @cookies {"age_check_done": "1"}
        """
        """ This function parse mgstage movie page.

        @url https://www.mgstage.com/product/product_detail/ABW-013/
        @cb_kwargs {"censored_id": "ABW-013", "store": "mgstage"}
        @cookies {"adc": "1"}
        """
        extractor = self.extractors.get(store, None)
        if extractor is None:
            return
        res = extractor.extract(response)
        self.logger.info("movie id: %s", censored_id)
        self.logger.info("movie title: %s", res.get('title', None))
        self.logger.info("release_date: %s", res.get('releaseDate', None))
        self.logger.info("delivery_date: %s", res.get('deliveryDate', None))
        self.logger.info("amateur: %s", res.get('amateur', None))
        self.logger.info("three_size: %s", res.get('threeSize', None))
        for id, name in res.get('actress', dict()).items():
            self.logger.info("actress info -> id: %s \t name: %s", id, name)
        for id, name in res.get('director', dict()).items():
            self.logger.info("director info -> id: %s \t name: %s", id, name)
        for id, name in res.get('maker', dict()).items():
            self.logger.info("maker info -> id: %s \t name: %s", id, name)
        for id, name in res.get('label', dict()).items():
            self.logger.info("label info -> id: %s \t name: %s", id, name)
        for id, name in res.get('series', dict()).items():
            self.logger.info("series info -> id: %s \t name: %s", id, name)
        for id, name in res.get('genre', dict()).items():
            self.logger.info("genre info -> id: %s \t name: %s", id, name)

        
