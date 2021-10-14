from fanza.movie.factory.url_factory_constants import *

from re import search

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

# only pre
# special
fsdss_mgs_formatter = FormatCensoredId(FSDSS, prefix=FSDSS_MGS_PRE)
fsdss_fanza_formatter = FormatCensoredId(FSDSS, prefix=FSDSS_FANZA_PRE)

# 6
dandan_formatter = FormatCensoredId(DANDAN, prefix=DANDAN_PRE)

# 5
dldss_formatter = FormatCensoredId(DLDSS, prefix=DLDSS_PRE)
stars_formatter = FormatCensoredId(STARS, prefix=STARS_PRE)
dandy_formatter = FormatCensoredId(DANDY, prefix=DANDY_PRE)
fcdss_formatter = FormatCensoredId(FCDSS, prefix=FCDSS_PRE)
nhdtb_formatter = FormatCensoredId(NHDTB, prefix=NHDTB_PRE)

# 4
gana_formatter = FormatCensoredId(GANA, prefix=GANA_PRE)
luxu_formatter = FormatCensoredId(LUXU, prefix=LUXU_PRE)
mium_formatter = FormatCensoredId(MIUM, prefix=MIUM_PRE)
suke_formatter = FormatCensoredId(SUKE, prefix=SUKE_PRE)
msfh_formatter = FormatCensoredId(MSFH, prefix=MSFH_PRE)
toen_formatter = FormatCensoredId(TOEN, prefix=TOEN_PRE)
davk_formatter = FormatCensoredId(DAVK, prefix=DAVK_PRE)
hmdn_formatter = FormatCensoredId(HMDN, prefix=HMDN_PRE)
hbad_formatter = FormatCensoredId(HBAD, prefix=HBAD_PRE)
maan_formatter = FormatCensoredId(MAAN, prefix=MAAN_PRE)
kuse_formatter = FormatCensoredId(KUSE, prefix=KUSE_PRE)
mgmr_formatter = FormatCensoredId(MGMR, prefix=MGMR_PRE)
reiw_formatter = FormatCensoredId(REIW, prefix=REIW_PRE)
sdde_formatter = FormatCensoredId(SDDE, prefix=SDDE_PRE)
simm_formatter = FormatCensoredId(SIMM, prefix=SIMM_PRE)
dfdm_formatter = FormatCensoredId(DFDM, prefix=DFDM_PRE)
hawa_formatter = FormatCensoredId(HAWA, prefix=HAWA_PRE)
hdka_formatter = FormatCensoredId(HDKA, prefix=HDKA_PRE)
hzgd_formatter = FormatCensoredId(HZGD, prefix=HZGD_PRE)
imgn_formatter = FormatCensoredId(IMGN, prefix=IMGN_PRE)
inst_formatter = FormatCensoredId(INST, prefix=INST_PRE)
iqqq_formatter = FormatCensoredId(IQQQ, prefix=IQQQ_PRE)
mcsr_formatter = FormatCensoredId(MCSR, prefix=MCSR_PRE)
mgfx_formatter = FormatCensoredId(MGFX, prefix=MGFX_PRE)
orec_formatter = FormatCensoredId(OREC, prefix=OREC_PRE)
skmj_formatter = FormatCensoredId(SKMJ, prefix=SKMJ_PRE)
scpy_formatter = FormatCensoredId(SCPY, prefix=SCPY_PRE)
stcv_formatter = FormatCensoredId(STCV, prefix=STCV_PRE)
hmgl_formatter = FormatCensoredId(HMGL, prefix=HMGL_PRE)
isrd_formatter = FormatCensoredId(ISRD, prefix=ISRD_PRE)
mara_formatter = FormatCensoredId(MARA, prefix=MARA_PRE)
milk_formatter = FormatCensoredId(MILK, prefix=MILK_PRE)
nacr_formatter = FormatCensoredId(NACR, prefix=NACR_PRE)
tkwa_formatter = FormatCensoredId(TKWA, prefix=TKWA_PRE)
hodv_formatter = FormatCensoredId(HODV, prefix=HODV_PRE)
redb_formatter = FormatCensoredId(REBD, prefix=REBD_PRE)

# 3
jac_formatter = FormatCensoredId(JAC, prefix=JAC_PRE)
gvh_formatter = FormatCensoredId(GVH, prefix=GVH_PRE)
ntk_formatter = FormatCensoredId(NTK, prefix=NTK_PRE)
aeg_formatter = FormatCensoredId(AEG, prefix=AEG_PRE)
ddh_formatter = FormatCensoredId(DDH, prefix=DDH_PRE)
ekw_formatter = FormatCensoredId(EKW, prefix=EKW_PRE)
hoi_formatter = FormatCensoredId(HOI, prefix=HOI_PRE)
dtt_formatter = FormatCensoredId(DTT, prefix=DTT_PRE)
kir_formatter = FormatCensoredId(KIR, prefix=KIR_PRE)
mfc_formatter = FormatCensoredId(MFC, prefix=MFC_PRE)
dcv_formatter = FormatCensoredId(DCV, prefix=DCV_PRE)
dfe_formatter = FormatCensoredId(DFE, prefix=DFE_PRE)
dht_formatter = FormatCensoredId(DHT, prefix=DHT_PRE)
ecb_formatter = FormatCensoredId(ECB, prefix=ECB_PRE)
jnt_formatter = FormatCensoredId(JNT, prefix=JNT_PRE)
kbi_formatter = FormatCensoredId(KBI, prefix=KBI_PRE)
knb_formatter = FormatCensoredId(KNB, prefix=KNB_PRE)
kir_formatter = FormatCensoredId(KIR, prefix=KIR_PRE)
oks_formatter = FormatCensoredId(OKS, prefix=OKS_PRE)
san_formatter = FormatCensoredId(SAN, prefix=SAN_PRE)
shh_formatter = FormatCensoredId(SHH, prefix=SHH_PRE)
zex_formatter = FormatCensoredId(ZEX, prefix=ZEX_PRE)
ara_formatter = FormatCensoredId(ARA, prefix=ARA_PRE)
gcp_formatter = FormatCensoredId(GCP, prefix=GCP_PRE)
hhh_formatter = FormatCensoredId(HHH, prefix=HHH_PRE)
mla_formatter = FormatCensoredId(MLA, prefix=MLA_PRE)

# 2
my_formatter = FormatCensoredId(MY, prefix=MY_PRE)
ss_formatter = FormatCensoredId(SS, prefix=SS_PRE)
sw_formatter = FormatCensoredId(SW, prefix=SW_PRE)

# only suffix
# 4
ssis_formatter = FormatCensoredId(SSIS, suffix=SSIS_SUF)

fanza_url_factory = FanzaUrlFactory(
    FANZA_URL_FORMATTER, FANZA_URL_REPLACEMENT,
    gvh_formatter, msfh_formatter, toen_formatter, stars_formatter,
    davk_formatter, hbad_formatter, kir_formatter, kuse_formatter, sdde_formatter, dandan_formatter,
    dandy_formatter, dfdm_formatter, dfe_formatter, ecb_formatter, fsdss_fanza_formatter,
    hawa_formatter, hdka_formatter, hzgd_formatter, iqqq_formatter, kir_formatter, mcsr_formatter,
    nhdtb_formatter, oks_formatter, san_formatter, skmj_formatter, ss_formatter, zex_formatter,
    hmgl_formatter, ssis_formatter, isrd_formatter, mara_formatter, milk_formatter, nacr_formatter,
    sw_formatter, redb_formatter
)

fanza_url_blank_replacement_factory = FanzaUrlFactory(
    FANZA_URL_FORMATTER, FANZA_URL_BLANK_REPLACEMENT,
    hodv_formatter
)

mgs_url_factory = MgsUrlFactory(
    MGS_URL_FORMATTER,
    dldss_formatter, fsdss_mgs_formatter, gana_formatter, luxu_formatter,
    mium_formatter,jac_formatter,suke_formatter, ntk_formatter, aeg_formatter, ddh_formatter,
    ekw_formatter, hoi_formatter, hmdn_formatter, dtt_formatter, maan_formatter, mfc_formatter,
    mgmr_formatter, reiw_formatter, my_formatter, simm_formatter, dcv_formatter, dht_formatter,
    fcdss_formatter, imgn_formatter, inst_formatter, jnt_formatter, kbi_formatter, knb_formatter,
    mgfx_formatter, orec_formatter, shh_formatter, scpy_formatter, stcv_formatter, ara_formatter,
    gcp_formatter, hhh_formatter, mla_formatter, tkwa_formatter
)

fanza_amateur_url_factory = FanzaUrlFactory(
    FANZA_AMATEUR_URL_FORMATTER, FANZA_AMATEUR_URL_REPLACEMENT
)
