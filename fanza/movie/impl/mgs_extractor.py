from re import compile
from fanza.movie.movie_extractor import MovieExtractor
from fanza.movie.movie_constants import MGS_TITLE_SUB_REGEX, MGS_SUB_STR, DATE_REGEX
from fanza.enums import Actress, DeliveryDate, Label, Maker, Genre, ReleaseDate, Series, VideoLen
from fanza.annotations import collect, checkvideolen, checkdate, notempty, notnull

class MgstageExtractor(MovieExtractor):
    @notnull
    def extract_title(self):
        title = self.response.xpath('//h1[@class="tag"]/text()').re_first(r'\n\s*(.*)\n\s*')
        return MGS_TITLE_SUB_REGEX.sub(MGS_SUB_STR, title)

    def extract_actress(self):
        return self.mgs_extract_multi_info(Actress.MGSTAGE.value)

    @checkvideolen
    @notnull
    def extract_video_len(self):
        return self.response.xpath(f'//th[contains(., "{VideoLen.MGSTAGE.value}")]/following-sibling::td/text()').re_first(r'\d+(?=min)')

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self):
        return self.mgs_extract_meta_info(ReleaseDate.MGSTAGE.value)

    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self):
        return self.mgs_extract_meta_info(DeliveryDate.MGSTAGE.value)

    def extract_director(self):
        return []

    def extract_label(self):
        return self.mgs_extract_multi_info(Label.MGSTAGE.value)

    def extract_maker(self):
        return self.mgs_extract_multi_info(Maker.MGSTAGE.value)

    def extract_series(self):
        return self.mgs_extract_multi_info(Series.MGSTAGE.value)

    def extract_genre(self):
        return self.mgs_extract_multi_info(Genre.MGSTAGE.value)

    def extract_store(self):
        return "mgstage"

    @notnull
    def extract_low_res_cover(self):
        return self.response.xpath('//img[@class="enlarge_image"]/@src').get()
    
    def extract_cover(self):
        low_res_cover = self.extract_low_res_cover()
        high_res_cover = compile(r'(?<=\/)pf_o1(?=_)').sub('pb_e', low_res_cover)
        return high_res_cover, low_res_cover

    def extract_preview(self):
        high_res_previews = self.extract_high_res_preview()
        low_res_previews = self.extract_low_res_preview()
        n = len(high_res_previews) if len(high_res_previews) > len(low_res_previews) else len(low_res_previews)
        for i in range(0, n):
            yield low_res_previews[i], high_res_previews[i], i

    @notempty
    def extract_low_res_preview(self):
        return self.response.xpath('//a[@class="sample_image"]/img/@src').getall()

    @notempty
    def extract_high_res_preview(self):
        return self.response.xpath('//a[@class="sample_image"]/@href').getall()

    def mgs_extract_multi_info(self, meta_text):
        names = self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/a/text()').re(r'\n\s*(.*)\n\s*')
        return names

    def mgs_extract_meta_info(self, meta_text):
        return self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/text()').get()
