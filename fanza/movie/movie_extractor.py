from scrapy.http import HtmlResponse

class MovieExtractor:
    def extract(self, response: HtmlResponse, censored_id: str) -> dict:
        title = self.extract_title(response)
        duration = self.extract_video_len(response)
        actress = self.extract_actress(response)
        release = self.extract_release_date(response)
        delivery = self.extract_delivery_date(response)
        director = self.extract_director(response)
        maker = self.extract_maker(response)
        label = self.extract_label(response)
        series = self.extract_series(response)
        genre = self.extract_genre(response)
        store = self.extract_store()
        return {
            "censored_id": censored_id,
            "title": title,
            "duration": duration,
            "actress": actress,
            "release": release,
            "delivery": delivery,
            "director": director,
            "maker": maker,
            "label": label,
            "series": series,
            "genre": genre,
            "store": store
        }

    def extract_title(self, response: HtmlResponse):
        pass

    def extract_director(self, response: HtmlResponse):
        pass

    def extract_maker(self, response: HtmlResponse):
        pass

    def extract_actress(self, response: HtmlResponse):
        pass

    def extract_release_date(self, response: HtmlResponse):
        pass

    def extract_delivery_date(self, response: HtmlResponse):
        pass

    def extract_series(self, response: HtmlResponse):
        pass

    def extract_video_len(self, response: HtmlResponse):
        pass

    def extract_genre(self, response: HtmlResponse):
        pass

    def extract_label(self, response: HtmlResponse):
        pass

    def extract_store(self):
        pass

    def extract_cover(self, response: HtmlResponse):
        pass

    def extract_preview(self, response: HtmlResponse):
        pass