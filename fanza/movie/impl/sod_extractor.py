from fanza.movie.movie_extractor import MovieExtractor
from fanza.enums import Actress, Director, Genre, Label, Maker, ReleaseDate, Series, VideoLen
from fanza.exceptions.fanza_exception import ExtractException
from fanza.movie.movie_constants import DATE_REGEX
from fanza.annotations import checkdate, checkvideolen, notnull
from scrapy.http import HtmlResponse
from re import search

class SodExtractor(MovieExtractor):
    @notnull
    def extract_title(self, response: HtmlResponse):
        return response.xpath('//div[@id="videos_head"]/h1[@style="display:none;"]/following-sibling::h1/text()').get()

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self, response: HtmlResponse):
        date_text = response.xpath(f'//td[text()="{ReleaseDate.SOD.value}"]/following-sibling::td/text()').get()
        date_m = search(r'(\d{4})年\s(\d{2})月\s(\d{2})日', date_text)
        if date_m is None:
            raise ExtractException('illegal date value')
        return f'{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}'

    @checkvideolen
    @notnull
    def extract_video_len(self, response: HtmlResponse):
        return response.xpath(f'//td[text()="{VideoLen.SOD.value}"]/following-sibling::td/text()').re_first(r'\d+(?=分)')
    
    def extract_actress(self, response: HtmlResponse):
        return self.sod_extract_multi_info(Actress.SOD.value, response)

    def extract_director(self, response: HtmlResponse):
        return self.sod_extract_multi_info(Director.SOD.value, response)

    def extract_maker(self, response: HtmlResponse):
        return self.sod_extract_multi_info(Maker.SOD.value, response)

    def extract_label(self, response: HtmlResponse):
        return response.xpath(f'//td[text()="{Label.SOD.value}"]/following-sibling::td/text()').getall()

    def extract_series(self, response: HtmlResponse):
        return self.sod_extract_multi_info(Series.SOD.value, response)
    
    def extract_genre(self, response: HtmlResponse):
        return self.sod_extract_multi_info(Genre.SOD.value, response)

    def extract_store(self):
        return "sod"

    def extract_cover(self, response: HtmlResponse):
        return self.extract_high_res_cover(response), self.extract_low_res_cover(response)

    @notnull
    def extract_high_res_cover(self, response: HtmlResponse):
        return response.xpath('//div[@class="videos_samimg"]/a/@href').get()

    @notnull
    def extract_low_res_cover(self, response: HtmlResponse):
        return response.xpath('//div[@class="videos_samimg"]/a/img/@src').get()

    def extract_preview(self, response: HtmlResponse):
        high_res_previews = self.extract_high_res_preview(response)
        low_res_previews = self.extract_low_res_preview(response)
        n = len(high_res_previews) if len(high_res_previews) > len(low_res_previews) else len(low_res_previews)
        for i in range(0, n):
            yield low_res_previews[i], high_res_previews[i], i

    def extract_high_res_preview(self, response: HtmlResponse):
        return response.xpath('//div[@id="videos_samsbox"]/a/@href').getall()

    def extract_low_res_preview(self, response: HtmlResponse):
        return response.xpath('//div[@id="videos_samsbox"]/a/img/@src').getall()

    def sod_extract_multi_info(self, meta_info, response: HtmlResponse):
        names = response.xpath(f'//td[text()="{meta_info}"]/following-sibling::td/a/text()').getall()
        return names
        
    