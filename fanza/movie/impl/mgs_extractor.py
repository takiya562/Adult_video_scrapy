from scrapy.http import HtmlResponse
from fanza.movie.movie_extractor import MovieExtractor
from typing import Iterator
from fanza.movie.movie_constants import *
from fanza.movie.movie_error_msg_constants import *
from fanza.annotations import collect, checkvideolen, checkdate

class MgstageExtractor(MovieExtractor):
    def extract_title(self) -> str:
        title = self.response.xpath('//h1[@class="tag"]/text()').re_first(r'\n\s*(.*)\n\s*')
        return MGS_TITLE_SUB_REGEX.sub(MGS_SUB_STR, self.mgs_clean_text(title))

    @collect
    def extract_actress(self) -> Iterator[tuple]:
        return self.mgs_extract_multi_info(MGS_ACTRESS_INFO)

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

    def mgs_clean_text(self, text: str):
        return MGS_FORMAT_REGEX.sub(MGS_SUB_STR, text)

    def mgs_extract_multi_info(self, meta_text: str) -> Iterator[tuple]:
        texts = self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/a/text()').re(r'\n\s*(.*)\n\s*')
        for i in range(0, len(texts)):
            yield i, texts[i]

    def mgs_extract_meta_info(self, meta_text: str) -> str:
        return self.response.xpath(f'//th[contains(., "{meta_text}")]/following-sibling::td/text()').get()
