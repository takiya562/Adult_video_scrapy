from re import search
from fanza.url_factory_constants import *

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
    def __init__(self, prefix: str, pre_digit: str) -> None:
        self.prefix = prefix
        self.pre_digit = pre_digit

    def format_censored_id(self, censored_id: str, prefix: str) -> CensoredIdResult:
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
    def __init__(self, url_formatter: str, replacement: str, *args: FormatCensoredId) -> None:
        super().__init__(url_formatter, *args)
        self.replacement = replacement

    def get_url(self, censored_id: str) -> str:
        prefix = search_pre(censored_id)
        for formatter in self.formatter_chain:
            result = formatter.format_censored_id(censored_id, prefix)
            if result.ok:
                return self.url_formatter % result.formated.replace('-', self.replacement).lower()
        return self.url_formatter % censored_id.replace('-', self.replacement).lower()

class MgsUrlFactory(UrlFactory):
    def __init__(self, url_formatter: str, *args: FormatCensoredId) -> None:
        super().__init__(url_formatter, *args)

    def get_url(self, censored_id: str) -> str:
        prefix = search_pre(censored_id)
        for formatter in self.formatter_chain:
            result = formatter.format_censored_id(censored_id, prefix)
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
ddh_formatter = FormatCensoredId(DDH, DDH_PRE)
ekw_formatter = FormatCensoredId(EKW, EKW_PRE)
hoi_formatter = FormatCensoredId(HOI, HOI_PRE)
hmdn_formatter = FormatCensoredId(HMDN, HMDN_PRE)
hbad_formatter = FormatCensoredId(HBAD, HBAD_PRE)
dtt_formatter = FormatCensoredId(DTT, DTT_PRE)
maan_formatter = FormatCensoredId(MAAN, MAAN_PRE)
kir_formatter = FormatCensoredId(KIR, KIR_PRE)
kuse_formatter = FormatCensoredId(KUSE, KUSE_PRE)
mfc_formatter = FormatCensoredId(MFC, MFC_PRE)
mgmr_formatter = FormatCensoredId(MGMR, MGMR_PRE)
reiw_formatter = FormatCensoredId(REIW, REIW_PRE)
my_formatter = FormatCensoredId(MY, MY_PRE)
sdde_formatter = FormatCensoredId(SDDE, SDDE_PRE)
simm_formatter = FormatCensoredId(SIMM, SIMM_PRE)

fanza_url_factory = FanzaUrlFactory(FANZA_URL_FORMATTER, FANZA_URL_REPLACEMENT, gvh_formatter, msfh_formatter, toen_formatter, stars_formatter,
                                    davk_formatter, hbad_formatter, kir_formatter, kuse_formatter, sdde_formatter)
mgs_url_factory = MgsUrlFactory(MGS_URL_FORMATTER, dldss_formatter, fsdss_formatter, gana_formatter, luxu_formatter,
                                mium_formatter,jac_formatter,suke_formatter, ntk_formatter, aeg_formatter, ddh_formatter,
                                ekw_formatter, hoi_formatter, hmdn_formatter, dtt_formatter, maan_formatter, mfc_formatter,
                                mgmr_formatter, reiw_formatter, my_formatter, simm_formatter)

fanza_amateur_url_factory = FanzaUrlFactory(FANZA_AMATEUR_URL_FORMATTER, FANZA_AMATEUR_URL_REPLACEMENT)
