from re import compile
from fanza.movie.movie_extractor import MovieExtractor
from fanza.movie.movie_constants import DATE_REGEX
from fanza.enums import Actress, DeliveryDate, Label, Maker, Genre, ReleaseDate, Series, VideoLen
from fanza.annotations import checkvideolen, checkdate, notempty, notnull
from scrapy.http import HtmlResponse

class MgstageExtractor(MovieExtractor):
    @notnull
    def extract_title(self, response: HtmlResponse):
        return response.xpath('//h1[@class="tag"]/text()').re_first(r'\n\s*(.*)\n\s*')

    def extract_actress(self, response: HtmlResponse):
        return self.mgs_extract_multi_info(Actress.MGSTAGE.value, response)

    @checkvideolen
    @notnull
    def extract_video_len(self, response: HtmlResponse):
        return response.xpath(f'//th[contains(., "{VideoLen.MGSTAGE.value}")]/following-sibling::td/text()').re_first(r'\d+(?=min)')

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self, response: HtmlResponse):
        return self.mgs_extract_meta_info(ReleaseDate.MGSTAGE.value, response)

    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self, response: HtmlResponse):
        return self.mgs_extract_meta_info(DeliveryDate.MGSTAGE.value, response)

    def extract_director(self, response: HtmlResponse):
        return []

    def extract_label(self, response: HtmlResponse):
        return self.mgs_extract_multi_info(Label.MGSTAGE.value, response)

    def extract_maker(self, response: HtmlResponse):
        return self.mgs_extract_multi_info(Maker.MGSTAGE.value, response)

    def extract_series(self, response: HtmlResponse):
        return self.mgs_extract_multi_info(Series.MGSTAGE.value, response)

    def extract_genre(self, response: HtmlResponse):
        return self.mgs_extract_multi_info(Genre.MGSTAGE.value, response)

    def extract_store(self):
        return "mgstage"

    @notnull
    def extract_low_res_cover(self, response: HtmlResponse):
        return response.xpath('//img[@class="enlarge_image"]/@src').get()
    
    def extract_cover(self, response: HtmlResponse):
        low_res_cover = self.extract_low_res_cover(response)
        high_res_cover = compile(r'(?<=\/)pf_o1(?=_)').sub('pb_e', low_res_cover)
        return high_res_cover, low_res_cover

    def extract_preview(self, response: HtmlResponse):
        high_res_previews = self.extract_high_res_preview(response)
        low_res_previews = self.extract_low_res_preview(response)
        n = len(high_res_previews) if len(high_res_previews) > len(low_res_previews) else len(low_res_previews)
        for i in range(0, n):
            yield low_res_previews[i], high_res_previews[i], i

    @notempty
    def extract_low_res_preview(self, response: HtmlResponse):
        return response.xpath('//a[@class="sample_image"]/img/@src').getall()

    @notempty
    def extract_high_res_preview(self, response: HtmlResponse):
        return response.xpath('//a[@class="sample_image"]/@href').getall()

    def mgs_extract_multi_info(self, meta_text, response: HtmlResponse):
        names = response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/a/text()').re(r'\n\s*(.*)\n\s*')
        return names

    def mgs_extract_meta_info(self, meta_text, response: HtmlResponse):
        return response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/text()').get()
