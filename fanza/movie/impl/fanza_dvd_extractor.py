from fanza.movie.impl.fanza_extractor import FanzaExtractor
from fanza.enums import Label, ReleaseDate, Actress, Director, Maker, Series, Genre
from fanza.movie.movie_constants import DATE_REGEX
from fanza.annotations import checkdate, notnull
from scrapy.http import HtmlResponse

class FanzaDvdExtractor(FanzaExtractor):
    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self, response: HtmlResponse):
        return self.fanza_dvd_extract_meta_info(ReleaseDate.FANZA_DVD.value, response)

    def extract_actress(self, response: HtmlResponse):
        return response.xpath(f'//span[@id="{Actress.FANZA_DVD.value}"]/a/text()').getall()

    def extract_director(self, response: HtmlResponse):
        return self.fanza_dvd_extract_multi_info(Director.FANZA_DVD.value, response)
    
    def extract_maker(self, response: HtmlResponse):
        return self.fanza_dvd_extract_multi_info(Maker.FANZA_DVD.value, response)

    def extract_label(self, response: HtmlResponse):
        return self.fanza_dvd_extract_multi_info(Label.FANZA_DVD.value, response)

    def extract_series(self, response: HtmlResponse):
        return self.fanza_dvd_extract_multi_info(Series.FANZA_DVD.value, response)

    def extract_genre(self, response: HtmlResponse):
        return self.fanza_dvd_extract_multi_info(Genre.FANZA_DVD.value, response)
    
    def extract_store(self):
        return "fanza-dvd"

    @notnull
    def extract_high_res_cover(self, response: HtmlResponse):
        return response.xpath('//div[@class="center"]/div/a[@name="package-image"]/@href').get()

    def fanza_dvd_extract_multi_info(self, meta_info, response: HtmlResponse):
        return response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/a/text()').getall()

    def fanza_dvd_extract_meta_info(self, meta_info, response: HtmlResponse):
        return response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/text()').get()