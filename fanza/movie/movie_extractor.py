from scrapy.http import HtmlResponse

class MovieExtractor:
    def extract(self, response: HtmlResponse) -> dict:
        self.response = response
        title = self.extract_title()
        duration = self.extract_video_len()
        actress = self.extract_actress()
        release = self.extract_release_date()
        delivery = self.extract_delivery_date()
        director = self.extract_director()
        maker = self.extract_maker()
        label = self.extract_label()
        series = self.extract_series()
        genre = self.extract_genre()
        store = self.extract_store()
        return {
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

    def extract_title(self):
        pass

    def extract_director(self):
        pass

    def extract_maker(self):
        pass

    def extract_actress(self):
        pass

    def extract_release_date(self):
        pass

    def extract_delivery_date(self):
        pass

    def extract_series(self):
        pass

    def extract_video_len(self):
        pass

    def extract_genre(self):
        pass

    def extract_label(self):
        pass

    def extract_store(self):
        pass

    def extract_cover(self):
        pass

    def extract_preview(self):
        pass