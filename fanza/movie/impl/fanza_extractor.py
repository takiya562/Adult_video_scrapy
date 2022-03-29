from re import search, compile
from fanza.movie.movie_extractor import MovieExtractor
from fanza.movie.movie_constants import DATE_REGEX
from fanza.enums import Actress, DeliveryDate, Genre, Label, Maker, ReleaseDate, Series, Director, VideoLen
from fanza.annotations import checkdate, checkvideolen, notempty, notnull

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

    def extract_actress(self):
        return self.fanza_extract_multi_info(Actress.FANZA.value)

    def extract_director(self):
        return self.fanza_extract_multi_info(Director.FANZA.value)

    def extract_maker(self):
        return self.fanza_extract_multi_info(Maker.FANZA.value)

    def extract_label(self):
        return self.fanza_extract_multi_info(Label.FANZA.value)

    def extract_series(self):
        return self.fanza_extract_multi_info(Series.FANZA.value)

    def extract_genre(self):
        return self.fanza_extract_multi_info(Genre.FANZA.value)

    def extract_store(self):
        return "fanza"

    @notnull
    def extract_high_res_cover(self):
        return self.response.xpath('//div[@class="center"]/a[@name="package-image"]/@href').get()

    @notnull
    def extract_low_res_cover(self):
        return self.response.xpath('//a[@name="package-image"]/img/@src').get()

    def extract_cover(self):
        return self.extract_high_res_cover(), self.extract_low_res_cover()

    def extract_preview(self):
        low_res_previews = self.extract_low_res_preview()
        for low_res_preview in low_res_previews:
            num_m = search(r'(?<=-)\d+(?=\.jpg)', low_res_preview)
            if num_m:
                num = num_m.group()
                high_res_url = compile(r'-(?=\d{1,2}(\.jpg)*$)').sub('jp-', low_res_preview)
                yield low_res_preview, high_res_url, int(num)

    @notempty
    def extract_low_res_preview(self):
        return self.response.xpath('//div[@id="sample-image-block"]/a/img/@src').getall()

    def fanza_extract_multi_info(self, meta_info):
        names = self.response.xpath(f'//a[@data-i3pst="{meta_info}"]/text()').getall()
        return names

    def fanza_extract_meta_info(self, meta_info):
        return self.response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/text()').re_first(r'(?<=\n).*')
    