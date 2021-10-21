from fanza.movie.movie_extractor import MovieExtractor
from typing import Iterator
from fanza.movie.movie_constants import DATE_REGEX, RELEASE_DATE_TEXT, DELIVERY_DATE_TEXT
from fanza.movie.movie_constants import FANZA_ACTRESS_INFO, FANZA_DIRECTOR_INFO, FANZA_MAKER_INFO, FANZA_LABEL_INFO
from fanza.movie.movie_constants import FANZA_SERIES_INFO, FANZA_GENRE_INFO
from fanza.annotations import checkdate, checkvideolen, collect, notnull

class FanzaExtractor(MovieExtractor):
    @notnull
    def extract_title(self) -> str:
        return self.response.xpath('//h1[@id="title"]/text()').get()

    @checkdate(regex=DATE_REGEX)
    def extract_release_date(self) -> str:
        return self.fanza_extract_meta_info(RELEASE_DATE_TEXT)

    @checkdate(regex=DATE_REGEX)
    def extract_delivery_date(self) -> str:
        return self.fanza_extract_meta_info(DELIVERY_DATE_TEXT)

    @notnull
    @checkvideolen
    def extract_video_len(self) -> str:
        return self.response.xpath('//table[@class="mg-b20"]/tr/td[contains(., "収録時間")]/following-sibling::td/text()').re_first(r'\d+(?=分)')

    @collect
    def extract_actress(self) -> Iterator[tuple]:
        return self.fanza_extract_multi_info(FANZA_ACTRESS_INFO)

    @collect
    def extract_director(self) -> Iterator[tuple]:
        return self.fanza_extract_multi_info(FANZA_DIRECTOR_INFO)

    @collect
    def extract_maker(self) -> Iterator[tuple]:
        return self.fanza_extract_multi_info(FANZA_MAKER_INFO)

    @collect
    def extract_label(self) -> Iterator[tuple]:
        return self.fanza_extract_multi_info(FANZA_LABEL_INFO)

    @collect
    def extract_series(self) -> Iterator[tuple]:
        return self.fanza_extract_multi_info(FANZA_SERIES_INFO)

    @collect
    def extract_genre(self) -> Iterator[tuple]:
        return self.fanza_extract_multi_info(FANZA_GENRE_INFO)

    def fanza_extract_multi_info(self, meta_info: str) -> Iterator[tuple]:
        ids = self.response.xpath(f'//a[@data-i3pst="{meta_info}"]/@href').re(r'(?<=id=)\d*')
        if len(ids) == 0:
            return {}
        texts = self.response.xpath(f'//a[@data-i3pst="{meta_info}"]/text()').getall()
        n = len(ids) if len(ids) > len(texts) else len(texts)
        for i in range(0, n):
            if not ids[i].isdigit():
                continue
            yield int(ids[i]), texts[i]

    def fanza_extract_meta_info(self, meta_info: str) -> str:
        return self.response.xpath(f'//table[@class="mg-b20"]/tr/td[contains(., "{meta_info}")]/following-sibling::td/text()').re_first(r'(?<=\n).*')
    