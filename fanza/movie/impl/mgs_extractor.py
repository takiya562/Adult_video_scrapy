from fanza.movie.movie_extractor import MovieExtractor
from typing import Iterator
from fanza.movie.movie_constants import MGS_TITLE_SUB_REGEX, MGS_SUB_STR, MGS_ACTRESS_INFO
from fanza.movie.movie_constants import DATE_REGEX, RELEASE_DATE_TEXT, DELIVERY_DATE_TEXT
from fanza.movie.movie_constants import MGS_LABEL_INFO, MGS_MAKER_INFO, MGS_SERIES_INFO, MGS_GENRE_INFO, MGS_FORMAT_REGEX
from fanza.annotations import collect, checkvideolen, checkdate, notnull

class MgstageExtractor(MovieExtractor):
    @notnull
    def extract_title(self) -> str:
        title = self.response.xpath('//h1[@class="tag"]/text()').re_first(r'\n\s*(.*)\n\s*')
        return MGS_TITLE_SUB_REGEX.sub(MGS_SUB_STR, title)

    @collect
    def extract_actress(self) -> Iterator[tuple]:
        return self.mgs_extract_multi_info(MGS_ACTRESS_INFO)

    @notnull
    @checkvideolen
    def extract_video_len(self) -> str:
        return self.response.xpath('//th[contains(., "収録時間")]/following-sibling::td/text()').re_first(r'\d+(?=min)')

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self) -> str:
        return self.mgs_extract_meta_info(RELEASE_DATE_TEXT)

    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self) -> str:
        return self.mgs_extract_meta_info(DELIVERY_DATE_TEXT)

    def extract_director(self):
        return dict()

    @collect
    def extract_label(self) -> Iterator[tuple]:
        return self.mgs_extract_multi_info(MGS_LABEL_INFO)

    @collect
    def extract_maker(self) -> Iterator[tuple]:
        return self.mgs_extract_multi_info(MGS_MAKER_INFO)

    @collect
    def extract_series(self) -> Iterator[tuple]:
        return self.mgs_extract_multi_info(MGS_SERIES_INFO)

    @collect
    def extract_genre(self) -> Iterator[tuple]:
        return self.mgs_extract_multi_info(MGS_GENRE_INFO)

    def mgs_extract_multi_info(self, meta_text: str) -> Iterator[tuple]:
        texts = self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/a/text()').re(r'\n\s*(.*)\n\s*')
        for i in range(0, len(texts)):
            yield i, texts[i]

    def mgs_extract_meta_info(self, meta_text: str) -> str:
        return self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/text()').get()
