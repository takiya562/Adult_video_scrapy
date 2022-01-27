from typing import Dict
from scrapy import Spider
from scrapy.http import HtmlResponse
from fanza.movie.impl.fanza_amateur_extractor import FanzaAmateurExtractor
from fanza.movie.impl.fanza_extractor import FanzaExtractor
from fanza.movie.impl.mgs_extractor import MgstageExtractor
from fanza.movie.impl.sod_extractor import SodExtractor
from fanza.movie.movie_extractor import MovieExtractor
from fanza.items import MovieImageItem
from scrapy.exporters import JsonLinesItemExporter
from fanza.movie.factory.request_factory import request_generate_chain
from fanza.common import get_crawled, save_crawled_to_file, scan_movie_dir

from re import search


class MovieDetailSpider(Spider):
    name = 'movie_detail'
    allowed_domains = ['dmm.co.jp', 'mgstage.com', 'ec.sod.co.jp']
    extractors: Dict[str, MovieExtractor] = {
        'fanza': FanzaExtractor(),
        'fanza_amateur': FanzaAmateurExtractor(),
        'mgstage': MgstageExtractor(),
        'sod': SodExtractor()
    }
    append_json_exporter = JsonLinesItemExporter(open('v-item.txt', 'ab'), ensure_ascii=False, encoding='utf-8')
    new_json_exporter = JsonLinesItemExporter(open('new-item.txt', 'wb'), ensure_ascii=False, encoding='utf-8')
    processed = set()
    successed = set()

    def start_requests(self):
        movie_dir = self.settings['MOVIE_DIR']
        ext_white_list = self.settings['EXT_WHITE_LIST']
        crawled = get_crawled(self.settings['CRAWLED_FILE'])
        for censored_id in scan_movie_dir(movie_dir, ext_white_list):
            id_m = search(r'^[A-Z]{2,6}-\d{3,5}', censored_id)
            if id_m is None:
                self.logger.info('%s is not a valid movie id', censored_id)
                continue
            censored_id = id_m.group()
            if censored_id in crawled:
                self.logger.debug('%s has been crawled', censored_id)
                continue
            self.processed.add(censored_id)
            for req in request_generate_chain.generate_request(self.parse, censored_id):
                yield req

        

    def parse(self, response: HtmlResponse, censored_id, store):
        """ This function parse fanza movie page.

        @url https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=cawd00186/
        @cb_kwargs {"censored_id": "CAWD-186", "store": "fanza"}
        @cookies {"age_check_done": "1"}
        """
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
        # """ This function parse sod movie page.
        
        # @url https://ec.sod.co.jp/prime/videos/?id=STARS-449
        # @cb_kwargs {"censored_id": "STARS-449", "store": "sod"}
        # @meta {"store": "sod"}
        # """
        if response.status != 200:
            self.logger.debug('%s is not a valid movie page', response.url)
            return
        if censored_id in self.successed:
            self.logger.debug('%s is duplicated', censored_id)
            return
        self.logger.info('%s is a valid movie page', response.url)
        extractor = self.extractors.get(store, None)
        if extractor is None:
            return
        res = extractor.extract(response, censored_id)
        self.append_json_exporter.export_item(res)
        self.new_json_exporter.export_item(res)
        save_crawled_to_file(censored_id, self.settings['CRAWLED_FILE'])
        self.successed.add(censored_id)
        self.logger.info('%s has been crawled', censored_id)
        self.logger.debug("movie info: %s", res)
        high_res_cover, low_res_cover = extractor.extract_cover()
        # self.logger.info("high_res_cover: %s", high_res_cover)
        # self.logger.info("low_res_cover: %s", low_res_cover)
        yield MovieImageItem(url=high_res_cover, subDir=censored_id, imageName=censored_id + "pl", isCover=1)
        yield MovieImageItem(url=low_res_cover, subDir=censored_id, imageName=censored_id + "ps", isCover=1)
        for low_res_url, high_res_url, num in extractor.extract_preview():
            # self.logger.info("low_res_preview: %s", low_res_url)
            # self.logger.info("high_res_preview: %s", high_res_url)
            low_res_preview_name = f'{censored_id}-{num:02d}'
            high_res_preview_name = f'{censored_id}jp-{num:02d}'
            yield MovieImageItem(url=low_res_url, subDir=censored_id, imageName=low_res_preview_name, isCover=0)
            yield MovieImageItem(url=high_res_url, subDir=censored_id, imageName=high_res_preview_name, isCover=0)
