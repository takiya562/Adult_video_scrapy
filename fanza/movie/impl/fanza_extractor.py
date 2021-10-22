from fanza.movie.movie_extractor import MovieExtractor
from fanza.movie.movie_constants import DATE_REGEX
from fanza.enums import Actress, DeliveryDate, Genre, Label, Maker, ReleaseDate, Series, Director, VideoLen
from fanza.annotations import checkdate, checkvideolen, collect, notnull

class FanzaExtractor(MovieExtractor):
    @notnull
    def extract_title(self):
        return self.response.xpath('//h1[@id="title"]/text()').get()

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self):
        return self.fanza_extract_meta_info(ReleaseDate.FANZA.value)

    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self):
        return self.fanza_extract_meta_info(DeliveryDate.FANZA.value)

    @checkvideolen
    @notnull
    def extract_video_len(self):
        return self.response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{VideoLen.FANZA.value}")]/following-sibling::td/text()').re_first(r'\d+(?=分)')

    @collect
    def extract_actress(self):
        return self.fanza_extract_multi_info(Actress.FANZA.value)

    @collect
    def extract_director(self):
        return self.fanza_extract_multi_info(Director.FANZA.value)

    @collect
    def extract_maker(self):
        return self.fanza_extract_multi_info(Maker.FANZA.value)

    @collect
    def extract_label(self):
        return self.fanza_extract_multi_info(Label.FANZa.value)

    @collect
    def extract_series(self):
        return self.fanza_extract_multi_info(Series.FANZA.value)

    @collect
    def extract_genre(self):
        return self.fanza_extract_multi_info(Genre.FANZA.value)

    def fanza_extract_multi_info(self, meta_info):
        ids = self.response.xpath(f'//a[@data-i3pst="{meta_info}"]/@href').re(r'(?<=id=)\d*')
        names = self.response.xpath(f'//a[@data-i3pst="{meta_info}"]/text()').getall()
        return ids, names

    def fanza_extract_meta_info(self, meta_info):
        return self.response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/text()').re_first(r'(?<=\n).*')
    