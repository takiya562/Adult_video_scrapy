import json

from fanza.items import AvbookActressBasicItem, AvbookMovieBasicItem, ImageItem, RequestStatusItem

from itemadapter import ItemAdapter
from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy_splash import SplashRequest

class CookiesContract(Contract):
    """ Contract to set the cookies of the request
        @cookies {"key": "value"}
    """

    name = 'cookies'

    def adjust_request_args(self, args):
        args['cookies'] = json.loads(' '.join(self.args))
        return args

class MetaContract(Contract):
    """ Contract to set the meta of the request
        @meta {"key": "value"}
    """

    name = 'meta'

    def adjust_request_args(self, args):
        args['meta'] = json.loads(' '.join(self.args))
        return args

class SplashEndpointContract(Contract):
    """ Contract to set the endpoint of the splash request
        @endpoint render.html
    """

    name = 'endpoint'

    def __init__(self, method, *args):
        super().__init__(method, *args)

        self.request_cls = SplashRequest

    def adjust_request_args(self, args):
        args['endpoint'] = self.args[0]
        return args
