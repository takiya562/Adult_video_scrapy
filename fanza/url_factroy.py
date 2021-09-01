from re import search
from fanza.constants import CENSORED_ID_PRE_REGEX, DAVK, DAVK_PRE, DLDSS, DLDSS_PRE, FSDSS, FSDSS_PRE, GANA, GANA_PRE
from fanza.constants import MIUM, MIUM_PRE, JAC, JAC_PRE, SUKE, SUKE_PRE, GVH, GVH_PRE, LUXU, LUXU_PRE
from fanza.constants import NTK, NTK_PRE, MSFH, MSFH_PRE, AEG, AEG_PRE, TOEN, TOEN_PRE, STARS, STARS_PRE
from fanza.constants import FANZA_URL_FORMATTER, MGS_URL_FORMATTER

class CensoredIdResult:
    def __init__(self, ok: bool, formated: str) -> None:
        self.ok = ok
        self.formated = formated

class FormatCensoredId:
    def __init__(self, prefix: str, pre_digit: str) -> None:
        self.prefix = prefix
        self.pre_digit = pre_digit

    def search_pre(self, censored_id: str):
        m = search(CENSORED_ID_PRE_REGEX, censored_id)
        if m:
            return m.group()
        else:
            return None

    def format_censored_id(self, censored_id: str) -> CensoredIdResult:
        prefix = self.search_pre(censored_id)
        if prefix is not None and prefix == self.prefix:
            return CensoredIdResult(True, self.pre_digit + censored_id)
        else:
            return CensoredIdResult(False, censored_id)

class UrlFactory:
    def __init__(self, url_formatter: str, *args: FormatCensoredId) -> None:
        self.formatter_chain = args
        self.url_formatter = url_formatter
    
    def get_url(self, censored_id: str) -> str:
        pass

class FanzaUrlFactory(UrlFactory):
    def __init__(self, url_formatter: str, *args: FormatCensoredId) -> None:
        super().__init__(url_formatter, *args)

    def get_url(self, censored_id: str) -> str:
        for formatter in self.formatter_chain:
            result = formatter.format_censored_id(censored_id)
            if result.ok:
                return self.url_formatter % result.formated.replace('-', '00').lower()
        return self.url_formatter % censored_id.replace('-', '00').lower()

class MgsUrlFactory(UrlFactory):
    def __init__(self, url_formatter: str, *args: FormatCensoredId) -> None:
        super().__init__(url_formatter, *args)

    def get_url(self, censored_id: str) -> str:
        for formatter in self.formatter_chain:
            result = formatter.format_censored_id(censored_id)
            if result.ok:
                return self.url_formatter % result.formated
        return self.url_formatter % censored_id

dldss_formatter = FormatCensoredId(DLDSS, DLDSS_PRE)
fsdss_formatter = FormatCensoredId(FSDSS, FSDSS_PRE)
gana_formatter = FormatCensoredId(GANA, GANA_PRE)
luxu_formatter = FormatCensoredId(LUXU, LUXU_PRE)
mium_formatter = FormatCensoredId(MIUM, MIUM_PRE)
jac_formatter = FormatCensoredId(JAC, JAC_PRE)
suke_formatter = FormatCensoredId(SUKE, SUKE_PRE)
gvh_formatter = FormatCensoredId(GVH, GVH_PRE)
ntk_formatter = FormatCensoredId(NTK, NTK_PRE)
msfh_formatter = FormatCensoredId(MSFH, MSFH_PRE)
aeg_formatter = FormatCensoredId(AEG, AEG_PRE)
toen_formatter = FormatCensoredId(TOEN, TOEN_PRE)
stars_formatter = FormatCensoredId(STARS, STARS_PRE)
davk_formatter = FormatCensoredId(DAVK, DAVK_PRE)

fanza_url_factory = FanzaUrlFactory(FANZA_URL_FORMATTER, gvh_formatter, msfh_formatter, toen_formatter, stars_formatter,
                                    davk_formatter)
mgs_url_factory = MgsUrlFactory(MGS_URL_FORMATTER, dldss_formatter, fsdss_formatter, gana_formatter, luxu_formatter,
                                mium_formatter,jac_formatter,suke_formatter, ntk_formatter, aeg_formatter)
