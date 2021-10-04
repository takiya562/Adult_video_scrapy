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
    def __init__(self, key: str, prefix: str, suffix: str) -> None:
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

dldss_formatter = FormatCensoredId(DLDSS, DLDSS_PRE, '')
fsdss_mgs_formatter = FormatCensoredId(FSDSS, FSDSS_MGS_PRE, '')
fsdss_fanza_formatter = FormatCensoredId(FSDSS, FSDSS_FANZA_PRE, '')
gana_formatter = FormatCensoredId(GANA, GANA_PRE, '')
luxu_formatter = FormatCensoredId(LUXU, LUXU_PRE, '')
mium_formatter = FormatCensoredId(MIUM, MIUM_PRE, '')
jac_formatter = FormatCensoredId(JAC, JAC_PRE, '')
suke_formatter = FormatCensoredId(SUKE, SUKE_PRE, '')
gvh_formatter = FormatCensoredId(GVH, GVH_PRE, '')
ntk_formatter = FormatCensoredId(NTK, NTK_PRE, '')
msfh_formatter = FormatCensoredId(MSFH, MSFH_PRE, '')
aeg_formatter = FormatCensoredId(AEG, AEG_PRE, '')
toen_formatter = FormatCensoredId(TOEN, TOEN_PRE, '')
stars_formatter = FormatCensoredId(STARS, STARS_PRE, '')
davk_formatter = FormatCensoredId(DAVK, DAVK_PRE, '')
ddh_formatter = FormatCensoredId(DDH, DDH_PRE, '')
ekw_formatter = FormatCensoredId(EKW, EKW_PRE, '')
hoi_formatter = FormatCensoredId(HOI, HOI_PRE, '')
hmdn_formatter = FormatCensoredId(HMDN, HMDN_PRE, '')
hbad_formatter = FormatCensoredId(HBAD, HBAD_PRE, '')
dtt_formatter = FormatCensoredId(DTT, DTT_PRE, '')
maan_formatter = FormatCensoredId(MAAN, MAAN_PRE, '')
kir_formatter = FormatCensoredId(KIR, KIR_PRE, '')
kuse_formatter = FormatCensoredId(KUSE, KUSE_PRE, '')
mfc_formatter = FormatCensoredId(MFC, MFC_PRE, '')
mgmr_formatter = FormatCensoredId(MGMR, MGMR_PRE, '')
reiw_formatter = FormatCensoredId(REIW, REIW_PRE, '')
my_formatter = FormatCensoredId(MY, MY_PRE, '')
sdde_formatter = FormatCensoredId(SDDE, SDDE_PRE, '')
simm_formatter = FormatCensoredId(SIMM, SIMM_PRE, '')
dandan_formatter = FormatCensoredId(DANDAN, DANDAN_PRE, '')
dandy_formatter = FormatCensoredId(DANDY, DANDY_PRE, '')
dcv_formatter = FormatCensoredId(DCV, DCV_PRE, '')
dfdm_formatter = FormatCensoredId(DFDM, DFDM_PRE, '')
dfe_formatter = FormatCensoredId(DFE, DFE_PRE, '')
dht_formatter = FormatCensoredId(DHT, DHT_PRE, '')
ecb_formatter = FormatCensoredId(ECB, ECB_PRE, '')
fcdss_formatter = FormatCensoredId(FCDSS, FCDSS_PRE, '')
hawa_formatter = FormatCensoredId(HAWA, HAWA_PRE, '')
hdka_formatter = FormatCensoredId(HDKA, HDKA_PRE, '')
hzgd_formatter = FormatCensoredId(HZGD, HZGD_PRE, '')
imgn_formatter = FormatCensoredId(IMGN, IMGN_PRE, '')
inst_formatter = FormatCensoredId(INST, INST_PRE, '')
iqqq_formatter = FormatCensoredId(IQQQ, IQQQ_PRE, '')
jnt_formatter = FormatCensoredId(JNT, JNT_PRE, '')
kbi_formatter = FormatCensoredId(KBI, KBI_PRE, '')
knb_formatter = FormatCensoredId(KNB, KNB_PRE, '')
kir_formatter = FormatCensoredId(KIR, KIR_PRE, '')
mcsr_formatter = FormatCensoredId(MCSR, MCSR_PRE, '')
mgfx_formatter = FormatCensoredId(MGFX, MGFX_PRE, '')
nhdtb_formatter = FormatCensoredId(NHDTB, NHDTB_PRE, '')
oks_formatter = FormatCensoredId(OKS, OKS_PRE, '')
orec_formatter = FormatCensoredId(OREC, OREC_PRE, '')
san_formatter = FormatCensoredId(SAN, SAN_PRE, '')
shh_formatter = FormatCensoredId(SHH, SHH_PRE, '')
skmj_formatter = FormatCensoredId(SKMJ, SKMJ_PRE, '')
scpy_formatter = FormatCensoredId(SCPY, SCPY_PRE, '')
ss_formatter = FormatCensoredId(SS, SS_PRE, '')
stcv_formatter = FormatCensoredId(STCV, STCV_PRE, '')
zex_formatter = FormatCensoredId(ZEX, ZEX_PRE, '')
hmgl_formatter = FormatCensoredId(HMGL, HMGL_PRE, '')
ssis_formatter = FormatCensoredId(SSIS, '', SSIS_SUF)

fanza_url_factory = FanzaUrlFactory(FANZA_URL_FORMATTER, FANZA_URL_REPLACEMENT, gvh_formatter, msfh_formatter, toen_formatter, stars_formatter,
                                    davk_formatter, hbad_formatter, kir_formatter, kuse_formatter, sdde_formatter, dandan_formatter,
                                    dandy_formatter, dfdm_formatter, dfe_formatter, ecb_formatter, fsdss_fanza_formatter,
                                    hawa_formatter, hdka_formatter, hzgd_formatter, iqqq_formatter, kir_formatter, mcsr_formatter,
                                    nhdtb_formatter, oks_formatter, san_formatter, skmj_formatter, ss_formatter, zex_formatter,
                                    hmgl_formatter, ssis_formatter)
mgs_url_factory = MgsUrlFactory(MGS_URL_FORMATTER, dldss_formatter, fsdss_mgs_formatter, gana_formatter, luxu_formatter,
                                mium_formatter,jac_formatter,suke_formatter, ntk_formatter, aeg_formatter, ddh_formatter,
                                ekw_formatter, hoi_formatter, hmdn_formatter, dtt_formatter, maan_formatter, mfc_formatter,
                                mgmr_formatter, reiw_formatter, my_formatter, simm_formatter, dcv_formatter, dht_formatter,
                                fcdss_formatter, imgn_formatter, inst_formatter, jnt_formatter, kbi_formatter, knb_formatter,
                                mgfx_formatter, orec_formatter, shh_formatter, scpy_formatter, stcv_formatter)

fanza_amateur_url_factory = FanzaUrlFactory(FANZA_AMATEUR_URL_FORMATTER, FANZA_AMATEUR_URL_REPLACEMENT)
