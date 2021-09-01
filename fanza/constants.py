from re import search, compile, IGNORECASE

CENSORED_ID_PRE_REGEX = r'\w+(?=-)'

FANZA_URL_FORMATTER = 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=%s/'

MGS_URL_FORMATTER = 'https://www.mgstage.com/product/product_detail/%s/'

DATE_REGEX = r'\d{4}\/\d{2}\/\d{2}'

DAVK = 'DAVK'

DAVK_PRE = '55'

STARS = 'STARS'

STARS_PRE = '1'

TOEN = 'TOEN'

TOEN_PRE = 'h_086'

AEG = 'AEG'

AEG_PRE = '360'

MSFH = 'MSFH'

MSFH_PRE = '1'

NTK = 'NTK'

NTK_PRE = '300'

LUXU = 'LUXU'

LUXU_PRE = '259'

MIUM = 'MIUM'

MIUM_PRE = '300'

JAC = 'JAC'

JAC_PRE = '390'

SUKE = 'SUKE'

SUKE_PRE = '428'

GVH = 'GVH'

GVH_PRE = '13'

GANA = 'GANA'

GANA_PRE = '200'

FSDSS = 'FSDSS'

FSDSS_PRE = '406'

DLDSS = 'DLDSS'

DLDSS_PRE = '513'

RELEASE_DATE_TEXT = '商品発売日'

DELIVERY_DATE_TEXT = '配信開始日'

VIDEO_LEN_TEXT = '収録時間'

GENRE_INFO = 'ジャンル'

GENRE_TABLE = 'genre'

LABEL_TABLE = 'label'

SERIES_TABLE = 'series'

MAKER_TABLE = 'maker'

DIRECTOR_TABLE = 'director'

ACTRESS_TABLE = 'actress'

CENSORED_ID_META = 'censored_id'

FANZA_AGE_COOKIE = 'age_check_done'

FANZA_AGE_COOKIE_VAL = '1'

FANZA_ACTRESS_INFO = 'info_actress'

FANZA_DIRECTOR_INFO = 'info_director'

FANZA_MAKER_INFO = 'info_maker'

FANZA_LABEL_INFO = 'info_label'

FANZA_SERIES_INFO = 'info_series'

FANZA_BLACK_GENRE_LIST = [r'セール', r'ギリモザ', r'ハイビジョン', r'独占配信', r'単体作品', r'ブランドストア30％OFF！']

MGS_BLACK_GENRE_LIST = [r'MGSだけのおまけ映像付き']

FANZA_COVER_SUB_REGEX = compile(r'ps(?=(\.jpg)*$)', IGNORECASE)

FANZA_COVER_SUB_STR = 'pl'

FANZA_PREVIEW_SUB_REGEX = compile(r'-(?=\d{1,2}(\.jpg)*$)')

FANZA_PREVIEW_SUB_STR = 'jp-'

FANZA_PREVIEW_NUM_REGEX = r'(?<=-)\d+(?=\.jpg)'

FANZA_IMAGE_NAME_SUB_REGEX = compile(r'(?<=[A-Za-z])0{2}(?=\d)')

FANZA_IMAGE_NAME_SUB_STR = '-'

MGS_AGE_COOKIE = 'adc'

MGS_AGE_COOKIE_VAL = '1'

MGS_FORMAT_REGEX = compile(r'\s*\n\s*')

MGS_TITLE_SUB_REGEX = compile(r'【.*MGS.*】')

MGS_SUB_STR = ''

MGS_ACTRESS_INFO = '出演'

MGS_MAKER_INFO = 'メーカー'

MGS_SERIES_INFO = 'シリーズ'

MGS_LABEL_INFO = 'レーベル'

MGS_COVER_URL_SUB_REGEX = compile(r'(?<=\/)pf_o1(?=_)')

MGS_COVER_URL_SUB_STR = 'pb_e'

HIGH_PREVIEW_IMAGE_FORMATTER = '{}jp-{}'

LOW_PREVIEW_IMAGE_FORMATTER = '{}-{}'

MGS_LOW_RES_PREVIEW_REGEX = r'(?<=cap_t1_)\d+(?=_)'

MGS_HIGH_RES_PREVIEW_REGEX = r'(?<=cap_e_)\d+(?=_)'