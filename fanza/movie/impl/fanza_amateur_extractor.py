from fanza.annotations import notnull
from fanza.movie.impl.fanza_extractor import FanzaExtractor

class FanzaAmateurExtractor(FanzaExtractor):
    def extract(self, response, censored_id) -> dict:
        res = super().extract(response, censored_id)
        amateur = self.extract_amateur()
        three_size = self.extract_three_size()
        res['amateur'] = amateur
        res['threeSize'] = three_size
        return res
    
    def extract_director(self):
        return []

    def extract_store(self):
        return "fanza-amateur"

    @notnull
    def extract_low_res_cover(self):
        return self.response.xpath('//div[@id="sample-video"]/img/@src').get()

    def extract_cover(self):
        low_res_cover = self.extract_low_res_cover()
        return low_res_cover, low_res_cover

    def extract_amateur(self):
        return self.fanza_extract_meta_info('名前')

    def extract_three_size(self):
        return self.response.xpath('//table[@class="mg-b20"]/tr/td[contains(., "サイズ")]/following-sibling::td/text()').get()
    