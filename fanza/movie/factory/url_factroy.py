from fanza.movie.factory.url_factory_constants import *

from re import search
import yaml

def search_pre(censored_id: str):
    m = search(CENSORED_ID_PRE_REGEX, censored_id)
    if m:
        return m.group()
    else:
        return None

class CensoredIdResult:
    def __init__(self, ok: bool, formated: str) -> None:
        self.ok = ok
        self.formated = formated

class FormatCensoredId:
    def __init__(self, key: str, prefix: str = "", suffix: str = "") -> None:
        self.key = key
        self.prefix = prefix
        self.suffix = suffix

    def format_censored_id(self, censored_id: str, key: str) -> CensoredIdResult:
        if key is not None and key == self.key:
            return CensoredIdResult(True, self.prefix + censored_id + self.suffix)
        else:
            return CensoredIdResult(False, censored_id)

class UrlFactory:
    def __init__(self, url_formatter: str, *args: FormatCensoredId) -> None:
        self.formatter_dict = dict()
        for formatter in args:
            formatter_set = self.formatter_dict.get(formatter.key, set())
            formatter_set.add(formatter)
            self.formatter_dict[formatter.key] = formatter_set
        self.url_formatter = url_formatter
    
    def get_url(self, censored_id: str) -> str:
        pass

class FanzaUrlFactory(UrlFactory):
    def __init__(self, url_formatter: str, replacement: str, *args: FormatCensoredId) -> None:
        super().__init__(url_formatter, *args)
        self.replacement = replacement

    def get_url(self, censored_id: str) -> str:
        key = search_pre(censored_id)
        for formatter in self.formatter_dict.get(key, set()):
            result = formatter.format_censored_id(censored_id, key)
            if result.ok:
                yield self.url_formatter % result.formated.replace('-', self.replacement).lower()
        yield self.url_formatter % censored_id.replace('-', self.replacement).lower()

class MgsUrlFactory(UrlFactory):
    def __init__(self, url_formatter: str, *args: FormatCensoredId) -> None:
        super().__init__(url_formatter, *args)

    def get_url(self, censored_id: str) -> str:
        key = search_pre(censored_id)
        for formatter in self.formatter_dict.get(key, set()):
            result = formatter.format_censored_id(censored_id, key)
            if result.ok:
                yield self.url_formatter % result.formated
        yield self.url_formatter % censored_id

class FanzaAmateurUrlFactory(UrlFactory):
    def __init__(self, url_formatter: str, replacement: str, black_list: set, *args: FormatCensoredId) -> None:
        super().__init__(url_formatter, *args)
        self.replacement = replacement
        self.black_list = black_list

    def get_url(self, censored_id: str) -> str:
        key = search_pre(censored_id)
        for formatter in self.formatter_dict.get(key, set()):
            result = formatter.format_censored_id(censored_id, key)
            if result.ok:
                yield self.url_formatter % result.formated.replace('-', self.replacement).lower()
        if key not in self.black_list:
            yield self.url_formatter % censored_id.replace('-', self.replacement).lower()

class SodUrlFactory(UrlFactory):
    def __init__(self, url_formatter: str) -> None:
        super().__init__(url_formatter)
    
    def get_url(self, censored_id: str) -> str:
        yield self.url_formatter % censored_id

with open('url_formatter_config.yaml', 'r') as file:
    url_formatter_config = yaml.load(file, Loader=yaml.BaseLoader)
    fanzas = url_formatter_config['fanza']
    mgstages = url_formatter_config['mgstage']
    fanza_amateurs = url_formatter_config['fanza_amateur']
    fanza_dvds = url_formatter_config['fanza_dvd']
    sods = url_formatter_config['sod']
    fanza_url_factories = [FanzaUrlFactory(fanza['url_formatter'], fanza['url_replacement'], *[FormatCensoredId(formatter.get('key'), formatter.get('prefix', ''), formatter.get('suffix', '')) for formatter in fanza['formatters']]) for fanza in fanzas]
    fanza_dvd_url_factories = [FanzaUrlFactory(fanza['url_formatter'], fanza['url_replacement'], *[FormatCensoredId(formatter.get('key'), formatter.get('prefix', ''), formatter.get('suffix', '')) for formatter in fanza['formatters']]) for fanza in fanza_dvds]
    mgstage_url_factories = [MgsUrlFactory(mgstage['url_formatter'], *[FormatCensoredId(formatter.get('key'), formatter.get('prefix', ''), formatter.get('suffix', '')) for formatter in mgstage['formatters']]) for mgstage in mgstages]
    fanza_amateur_url_factories = [FanzaAmateurUrlFactory(fanza_amateur['url_formatter'], fanza_amateur['url_replacement'], fanza_amateur['black_list']) for fanza_amateur in fanza_amateurs ]
    sod_url_factories = [SodUrlFactory(sod['url_formatter']) for sod in sods]
