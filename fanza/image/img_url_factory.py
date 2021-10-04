from re import Pattern
from fanza.movie.movie_constants import MGS_LOW_RES_COVER_URL_SUB_STR, MGS_LOW_RES_COVER_URL_SUB_REGEX
from fanza.movie.factory.url_factroy import search_pre
from fanza.movie.factory.url_factory_constants import SIRO, GANA

class ImageUrlResult:
    def __init__(self, ok: bool, url: str) -> None:
        self.ok = ok
        self.url = url

class ImageUrlHandler:
    def handle_url(self, prefix: str, url: str) -> ImageUrlResult:
        pass
    
class MgsLowResCoverImageHandler(ImageUrlHandler):
    def __init__(self, prefix: str, sub: str, regex: Pattern) -> None:
        self.prefix = prefix
        self.sub = sub
        self.regex = regex

    def handle_url(self, prefix: str, url: str) -> ImageUrlResult:
        if prefix is not None and self.prefix == prefix:
            return ImageUrlResult(True, self.regex.sub(self.sub, url))
        else:
            return ImageUrlResult(False, url)

class ImageUrlFactory:
    def __init__(self, *args: ImageUrlHandler) -> None:
        self.hanlder_chain = args

    def get_url(self, url: str, censored_id: str):
        pass

class MgsLowResCoverImageUrlFactory(ImageUrlFactory):
    def __init__(self, *args: ImageUrlHandler) -> None:
        super().__init__(*args)

    def get_url(self, url: str, censored_id: str):
        prefix = search_pre(censored_id)
        for handler in self.hanlder_chain:
            result = handler.handle_url(prefix, url)
            if result.ok:
                return result.url
        return url

siro_handler = MgsLowResCoverImageHandler(SIRO, MGS_LOW_RES_COVER_URL_SUB_STR, MGS_LOW_RES_COVER_URL_SUB_REGEX)
gana_handler = MgsLowResCoverImageHandler(GANA, MGS_LOW_RES_COVER_URL_SUB_STR, MGS_LOW_RES_COVER_URL_SUB_REGEX)

mgs_low_res_cover_url_factory = MgsLowResCoverImageUrlFactory(siro_handler, gana_handler)
