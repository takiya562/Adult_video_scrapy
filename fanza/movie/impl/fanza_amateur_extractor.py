from fanza.annotations import notnull
from fanza.movie.impl.fanza_extractor import FanzaExtractor
from re import search, compile
from scrapy.http import HtmlResponse

class FanzaAmateurExtractor(FanzaExtractor):
    def extract(self, response, censored_id) -> dict:
        res = super().extract(response, censored_id)
        amateur = self.extract_amateur(response)
        three_size = self.extract_three_size(response)
        res['amateur'] = amateur
        res['threeSize'] = three_size
        return res
    
    def extract_director(self, response):
        return []

    def extract_store(self):
        return "fanza-amateur"

    def extract_preview(self, response: HtmlResponse):
        low_res_previews = self.extract_low_res_preview(response)
        for low_res_preview in low_res_previews:
            num_m = search(r'(?<=-)\d+(?=\.jpg)', low_res_preview)
            if num_m:
                num = num_m.group()
                high_res_url = compile(r'js-(?=\d{3}(\.jpg)*$)').sub('jp-', low_res_preview)
                yield low_res_preview, high_res_url, int(num)

    @notnull
    def extract_low_res_cover(self, response: HtmlResponse):
        return response.xpath('//div[@id="sample-video"]/img/@src').get()

    def extract_cover(self, response: HtmlResponse):
        low_res_cover = self.extract_low_res_cover(response)
        return low_res_cover, low_res_cover

    def extract_amateur(self, response: HtmlResponse):
        return self.fanza_extract_meta_info('名前', response)

    def extract_three_size(self, response: HtmlResponse):
        return response.xpath('//table[@class="mg-b20"]/tr/td[contains(., "サイズ")]/following-sibling::td/text()').get()
    