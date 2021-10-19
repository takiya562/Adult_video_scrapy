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

class AvbookScrapesContract(Contract):
    """ Contract to check value of fields in scraped items
        @avbookscrapes item {"key": "value", ...} ...

        e.g.:
        @avbookscrapes movieItem {"title": "title", "censoredId": "ABC-123"}
    """

    name = 'avbookscrapes'

    object_type_verifiers = {
        'movieItem': lambda x: isinstance(x, AvbookMovieBasicItem),
        'actressItem': lambda x: isinstance(x, AvbookActressBasicItem),
    }

    def __init__(self, method, *args):
        super().__init__(method, *args)

        self.obj_name = self.args[0] or None
        self.object_type_verifier = self.object_type_verifiers[self.obj_name]
        self.field_value = json.loads(' '.join(self.args[1:]))

    def post_process(self, output):
        for x in output:
            if self.object_type_verifier(x):
                item_adapter = ItemAdapter(x)
                mismatch = [field for field, value in self.field_value.items() if field not in item_adapter or value != item_adapter[field]]
                if mismatch:
                    msg = ""
                    for field in mismatch:
                        if field not in item_adapter:
                            msg += f"Missing field: {field} "
                        else:
                            msg += f"Returned {self.obj_name} {field} value is {item_adapter[field]}, expected {self.field_value[field]} "
                    raise ContractFail(msg)


class AvbookReturnsContract(Contract):
    """ Contract to check output of a callback

        general form:
        @avbookreturns movieItem/ImageItem num ...

        e.g.:
        @avbookreturns movieItem 2
        @avbookreturns ImageItem 3
        @avbookreturns movieItem 3 ImageItem 4
    """

    name = 'avbookreturns'

    object_type_verifiers = {
        'movieItem': lambda x: isinstance(x, AvbookMovieBasicItem),
        'actressItem': lambda x: isinstance(x, AvbookActressBasicItem),
        'imageItem': lambda x: isinstance(x, ImageItem),
        'requestStatusItem': lambda x: isinstance(x, RequestStatusItem),
    }

    def __init__(self, method, *args):
        super().__init__(method, *args)
        
        if len(self.args) not in [2, 4, 6]:
            raise ValueError(
                f"Incorrect argument quantity: expected 2, 4 or 6, got {len(self.args)}"
            )
        self.item_names = list()
        self.item_nums = list()
        self.item_verifiers = list()
        for i in range(0, len(self.args), 2):
            item_name = self.args[i] or None
            self.item_names.append(item_name)
            self.item_nums.append(int(self.args[i + 1]))
            self.item_verifiers.append(self.object_type_verifiers[item_name])

    def post_process(self, output):
        n = len(self.item_names)
        occurrences = [0] * n
        for x in output:
            for i in range(0, n):
                if self.item_verifiers[i](x):
                    occurrences[i] += 1
        
        fail = False
        msg = ""
        for i in range(0, n):
            if occurrences[i] != self.item_nums[i]:
                fail = True
            msg += f"Returned {occurrences[i]} {self.item_names[i]}, expected {self.item_nums[i]} "

        if fail:
            raise ContractFail(msg)

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
