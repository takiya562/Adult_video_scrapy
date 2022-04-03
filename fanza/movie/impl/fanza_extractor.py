from re import search, compile
from fanza.movie.movie_extractor import MovieExtractor
from fanza.movie.movie_constants import DATE_REGEX
from fanza.enums import Actress, DeliveryDate, Genre, Label, Maker, ReleaseDate, Series, Director, VideoLen
from fanza.annotations import checkdate, checkvideolen, notempty, notnull
from scrapy.http import HtmlResponse

class FanzaExtractor(MovieExtractor):
    @notnull
    def extract_title(self, response: HtmlResponse):
        return response.xpath('//h1[@id="title"]/text()').get()

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self, response: HtmlResponse):
        return self.fanza_extract_meta_info(ReleaseDate.FANZA.value, response)

    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self, response: HtmlResponse):
        return self.fanza_extract_meta_info(DeliveryDate.FANZA.value, response)

    @checkvideolen
    @notnull
    def extract_video_len(self, response: HtmlResponse):
        return response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{VideoLen.FANZA.value}")]/following-sibling::td/text()').re_first(r'\d+(?=分)')

    def extract_actress(self, response: HtmlResponse):
        return self.fanza_extract_multi_info(Actress.FANZA.value, response)

    def extract_director(self, response: HtmlResponse):
        return self.fanza_extract_multi_info(Director.FANZA.value, response)

    def extract_maker(self, response: HtmlResponse):
        return self.fanza_extract_multi_info(Maker.FANZA.value, response)

    def extract_label(self, response: HtmlResponse):
        return self.fanza_extract_multi_info(Label.FANZA.value, response)

    def extract_series(self, response: HtmlResponse):
        return self.fanza_extract_multi_info(Series.FANZA.value, response)

    def extract_genre(self, response: HtmlResponse):
        return self.fanza_extract_multi_info(Genre.FANZA.value, response)

    def extract_store(self):
        return "fanza"

    @notnull
    def extract_high_res_cover(self, response: HtmlResponse):
        return response.xpath('//div[@class="center"]/a[@name="package-image"]/@href').get()

    @notnull
    def extract_low_res_cover(self, response: HtmlResponse):
        return response.xpath('//a[@name="package-image"]/img/@src').get()

    def extract_cover(self, response: HtmlResponse):
        return self.extract_high_res_cover(response), self.extract_low_res_cover(response)

    def extract_preview(self, response: HtmlResponse):
        low_res_previews = self.extract_low_res_preview(response)
        for low_res_preview in low_res_previews:
            num_m = search(r'(?<=-)\d+(?=\.jpg)', low_res_preview)
            if num_m:
                num = num_m.group()
                high_res_url = compile(r'-(?=\d{1,2}(\.jpg)*$)').sub('jp-', low_res_preview)
                yield low_res_preview, high_res_url, int(num)

    @notempty
    def extract_low_res_preview(self, response: HtmlResponse):
        return response.xpath('//div[@id="sample-image-block"]/a/img/@src').getall()

    def fanza_extract_multi_info(self, meta_info, response: HtmlResponse):
        return response.xpath(f'//a[@data-i3pst="{meta_info}"]/text()').getall()

    def fanza_extract_meta_info(self, meta_info, response: HtmlResponse):
        return response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/text()').re_first(r'(?<=\n).*')
    