from fanza.movie.impl.fanza_extractor import FanzaExtractor
from fanza.enums import Label, ReleaseDate, Actress, Director, Maker, Series, Genre
from fanza.movie.movie_constants import DATE_REGEX
from fanza.annotations import checkdate, notnull

class FanzaDvdExtractor(FanzaExtractor):
    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self):
        return self.fanza_dvd_extract_meta_info(ReleaseDate.FANZA_DVD.value)

    def extract_actress(self):
        return self.response.xpath(f'//span[@id="{Actress.FANZA_DVD.value}"]/a/text()').getall()

    def extract_director(self):
        return self.fanza_dvd_extract_multi_info(Director.FANZA_DVD.value)
    
    def extract_maker(self):
        return self.fanza_dvd_extract_multi_info(Maker.FANZA_DVD.value)

    def extract_label(self):
        return self.fanza_dvd_extract_multi_info(Label.FANZA_DVD.value)

    def extract_series(self):
        return self.fanza_dvd_extract_multi_info(Series.FANZA_DVD.value)

    def extract_genre(self):
        return self.fanza_dvd_extract_multi_info(Genre.FANZA_DVD.value)
    
    def extract_store(self):
        return "fanza-dvd"

    @notnull
    def extract_high_res_cover(self):
        return self.response.xpath('//div[@class="center"]/div/a[@name="package-image"]/@href').get()

    def fanza_dvd_extract_multi_info(self, meta_info):
        return self.response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/a/text()').getall()

    def fanza_dvd_extract_meta_info(self, meta_info):
        return self.response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/text()').get()