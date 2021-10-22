from fanza.movie.movie_extractor import MovieExtractor
from fanza.enums import Actress, Director, Genre, Label, Maker, ReleaseDate, Series, VideoLen
from fanza.exceptions.fanza_exception import ExtractException
from fanza.movie.movie_constants import DATE_REGEX
from fanza.annotations import checkdate, checkvideolen, collect, notnull
from re import search

class SodExtractor(MovieExtractor):
    @notnull
    def extract_title(self):
        return self.response.xpath('//div[@id="videos_head"]/h1[@style="display:none;"]/following-sibling::h1/text()').get()

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self):
        date_text = self.response.xpath(f'//td[text()="{ReleaseDate.SOD.value}"]/following-sibling::td/text()').get()
        date_m = search(r'(\d{4})年\s(\d{2})月\s(\d{2})日', date_text)
        if date_m is None:
            raise ExtractException('illegal date value')
        return f'{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}'

    @checkvideolen
    @notnull
    def extract_video_len(self):
        return self.response.xpath(f'//td[text()="{VideoLen.SOD.value}"]/following-sibling::td/text()').re_first(r'\d+(?=分)')
    
    @collect
    def extract_actress(self):
        return self.sod_extract_multi_info(Actress.SOD.value)

    @collect
    def extract_director(self):
        return self.sod_extract_multi_info(Director.SOD.value)

    @collect
    def extract_maker(self):
        return self.sod_extract_multi_info(Maker.SOD.value)

    def extract_label(self):
        return self.response.xpath(f'//td[text()="{Label.SOD.value}"]/following-sibling::td/text()').get()

    @collect
    def extract_series(self):
        return self.sod_extract_multi_info(Series.SOD.value)
    
    @collect
    def extract_genre(self):
        return self.sod_extract_multi_info(Genre.SOD.value)

    def sod_extract_multi_info(self, meta_info):
        ids = self.response.xpath(f'//td[text()="{meta_info}"]/following-sibling::td/a/@href').re(r'(?<==)\d+$')
        names = self.response.xpath(f'//td[text()="{meta_info}"]/following-sibling::td/a/text()').getall()
        return ids, names
        
    