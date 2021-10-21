from scrapy.http import HtmlResponse
from typing import Dict, Iterator

class MovieExtractor:
    def extract(self, response: HtmlResponse) -> dict:
        self.response = response
        title = self.extract_title()
        video_len = self.extract_video_len()
        actress = self.extract_actress()
        release_date = self.extract_release_date()
        delivery_date = self.extract_delivery_date()
        director = self.extract_director()
        maker = self.extract_maker()
        label = self.extract_label()
        series = self.extract_series()
        genre = self.extract_genre()
        return {
            "title": title,
            "videoLen": video_len,
            "actress": actress,
            "releaseDate": release_date,
            "deliveryDate": delivery_date,
            "director": director,
            "maker": maker,
            "label": label,
            "series": series,
            "genre": genre
        }

    def extract_title(self) -> str:
        pass

    def extract_director(self) -> Iterator[tuple]:
        pass

    def extract_maker(self) -> Iterator[tuple]:
        pass

    def extract_actress(self) -> Iterator[tuple]:
        pass

    def extract_release_date(self) -> str:
        pass

    def extract_delivery_date(self) -> str:
        pass

    def extract_series(self) -> Iterator[tuple]:
        pass

    def extract_video_len(self) -> int:
        pass

    def extract_genre(self) -> Iterator[tuple]:
        pass

    def extract_label(self) -> Iterator[tuple]:
        pass