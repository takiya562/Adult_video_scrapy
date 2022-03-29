from scrapy import Request
from fanza.enums import AgeCookie, AgeCookieVal, Store
from fanza.movie.factory.url_factroy import UrlFactory, fanza_url_factories, fanza_amateur_url_factories, mgstage_url_factories, sod_url_factories, fanza_dvd_url_factories
from fanza.movie.movie_constants import MOVIE_STORE

class RequestFactory:
    def __init__(self, *url_factories: UrlFactory) -> None:
        self.url_factories = url_factories

    def get_request(self, callback, censored_id):
        for url_factory in self.url_factories:
            for url in url_factory.get_url(censored_id):
                yield Request(
                    url=url,
                    callback=callback,
                    cb_kwargs={'censored_id': censored_id},
                )

class FanzaRequestFactory(RequestFactory):
    def get_request(self, callback, censored_id):
        for req in super().get_request(callback, censored_id):
            req.cookies = {AgeCookie.FANZA.value: AgeCookieVal.FANZA.value}
            req.cb_kwargs[MOVIE_STORE] = Store.FANZA.value
            yield req

class MgstageRequestFactory(RequestFactory):
    def get_request(self, callback, censored_id):
        for req in super().get_request(callback, censored_id):
            req.cookies = {AgeCookie.MGSTAGE.value: AgeCookieVal.MGSTAGE.value}
            req.cb_kwargs[MOVIE_STORE] = Store.MGSTAGE.value
            req.meta['dont_redirect'] = True
            yield req

class FanzaAmateurRequestFactory(FanzaRequestFactory):
    def get_request(self, callback, censored_id):
        for req in super().get_request(callback, censored_id):
            req.cb_kwargs[MOVIE_STORE] = Store.FANZA_AMATEUR.value
            yield req

class FanzaDvdRequestFactory(FanzaRequestFactory):
    def get_request(self, callback, censored_id):
        for req in super().get_request(callback, censored_id):
            req.cb_kwargs[MOVIE_STORE] = Store.FANZA_DVD.value
            yield req

class SodRequestFactory(RequestFactory):
    def get_request(self, callback, censored_id):
        for req in super().get_request(callback, censored_id):
            req.cb_kwargs[MOVIE_STORE] = Store.SOD.value
            req.meta[MOVIE_STORE] = 'sod'
            req.meta['dont_filter'] = True
            yield req

class RequestGenerateChain:
    def __init__(self, *factories: RequestFactory):
        self.request_factorys = factories

    def generate_request(self, callback, censored_id):
        for request_factory in self.request_factorys:
            for req in request_factory.get_request(callback, censored_id):
                yield req
        

fanza_request_factory = FanzaRequestFactory(*fanza_url_factories)
fanza_amateur_request_factory = FanzaAmateurRequestFactory(*fanza_amateur_url_factories)
fanza_dvd_request_factory = FanzaDvdRequestFactory(*fanza_dvd_url_factories)
mgstage_request_factory = MgstageRequestFactory(*mgstage_url_factories)
sod_request_factory = SodRequestFactory(*sod_url_factories)

request_generate_chain = RequestGenerateChain(fanza_request_factory, mgstage_request_factory, fanza_amateur_request_factory, sod_request_factory, fanza_dvd_request_factory)