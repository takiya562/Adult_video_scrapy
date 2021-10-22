from fanza.movie.movie_extractor import MovieExtractor
from fanza.movie.movie_constants import MGS_TITLE_SUB_REGEX, MGS_SUB_STR, DATE_REGEX
from fanza.enums import Actress, DeliveryDate, Label, Maker, Genre, ReleaseDate, Series, VideoLen
from fanza.annotations import collect, checkvideolen, checkdate, notnull

class MgstageExtractor(MovieExtractor):
    @notnull
    def extract_title(self):
        title = self.response.xpath('//h1[@class="tag"]/text()').re_first(r'\n\s*(.*)\n\s*')
        return MGS_TITLE_SUB_REGEX.sub(MGS_SUB_STR, title)

    @collect
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
        return dict()

    @collect
    def extract_label(self):
        return self.mgs_extract_multi_info(Label.MGSTAGE.value)

    @collect
    def extract_maker(self):
        return self.mgs_extract_multi_info(Maker.MGSTAGE.value)

    @collect
    def extract_series(self):
        return self.mgs_extract_multi_info(Series.MGSTAGE.value)

    @collect
    def extract_genre(self):
        return self.mgs_extract_multi_info(Genre.MGSTAGE.value)

    def mgs_extract_multi_info(self, meta_text):
        names = self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/a/text()').re(r'\n\s*(.*)\n\s*')
        return [n for n in range(0, len(names))], names

    def mgs_extract_meta_info(self, meta_text):
        return self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/text()').get()
