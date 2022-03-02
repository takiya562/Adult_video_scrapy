from typing import Dict
from scrapy import Spider
from scrapy.http import HtmlResponse
from fanza.common import get_crawled, scan_movie_dir
from fanza.items import MovieImageItem
from fanza.movie.factory.request_factory import request_generate_chain
from fanza.movie.impl.fanza_amateur_extractor import FanzaAmateurExtractor
from fanza.movie.impl.fanza_extractor import FanzaExtractor
from fanza.movie.impl.mgs_extractor import MgstageExtractor
from fanza.movie.impl.sod_extractor import SodExtractor
from fanza.movie.movie_extractor import MovieExtractor

from re import search


class MoiveImageSpider(Spider):
    name = 'movie_image'
    allowed_domains = ['dmm.co.jp', 'mgstage.com', 'ec.sod.co.jp']
    start_urls = ['http://dmm.co.jp/']
    extractors: Dict[str, MovieExtractor] = {
        'fanza': FanzaExtractor(),
        'fanza_amateur': FanzaAmateurExtractor(),
        'mgstage': MgstageExtractor(),
        'sod': SodExtractor()
    }
    processed = set()
    successed = set()

    def __init__(self, censored_id=None, **kwargs):
        super().__init__(**kwargs)
        self.censored_id = censored_id

    def start_requests(self):
        movie_dir = self.settings['MOVIE_DIR']
        ext_white_list = self.settings['EXT_WHITE_LIST']
        crawled = get_crawled(self.settings['CRAWLED_FILE'])
        for censored_id in scan_movie_dir(movie_dir, ext_white_list):
            id_m = search(r'^[A-Z]{1,6}-\d{3,7}', censored_id)
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
        if response.status != 200:
            self.logger.debug('%s is not a valid movie page', response.url)
            return
        extractor = self.extractors.get(store, None)
        if extractor is None:
            return
        extractor.response = response
        high_res_cover, low_res_cover = extractor.extract_cover()
        yield MovieImageItem(url=high_res_cover, subDir=censored_id, imageName=censored_id + "pl", isCover=1)
        yield MovieImageItem(url=low_res_cover, subDir=censored_id, imageName=censored_id + "ps", isCover=1)
        for low_res_url, high_res_url, num in extractor.extract_preview():
            low_res_preview_name = f'{censored_id}-{num:02d}'
            high_res_preview_name = f'{censored_id}jp-{num:02d}'
            yield MovieImageItem(url=low_res_url, subDir=censored_id, imageName=low_res_preview_name, isCover=0)
            yield MovieImageItem(url=high_res_url, subDir=censored_id, imageName=high_res_preview_name, isCover=0)
        self.successed.add(censored_id)
