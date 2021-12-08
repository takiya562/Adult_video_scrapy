from fanza.annotations import notnull
from fanza.movie.impl.fanza_extractor import FanzaExtractor
from fanza.movie.movie_constants import AMATEUR_NAME_TEXT

class FanzaAmateurExtractor(FanzaExtractor):
    def extract(self, response) -> dict:
        res = super().extract(response)
        amateur = self.extract_amateur()
        three_size = self.extract_three_size()
        res['amateur'] = amateur
        res['threeSize'] = three_size
        return res
    
    def extract_director(self):
        return dict()

    @notnull
    def extract_low_res_cover(self):
        return self.response.xpath('//div[@id="sample-video"]/img/@src').get()

    def extract_cover(self):
        low_res_cover = self.extract_low_res_cover()
        return low_res_cover, low_res_cover

    def extract_amateur(self):
        return self.fanza_extract_meta_info(AMATEUR_NAME_TEXT)

    def extract_three_size(self):
        return self.response.xpath('//table[@class="mg-b20"]/tr/td[contains(., "サイズ")]/following-sibling::td/text()').get()
    