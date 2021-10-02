from re import compile, IGNORECASE

CENSORED_ID_REGEX = r'^[A-Z]{2,5}-\d{3,4}'

DATE_REGEX = r'\d{4}\/\d{2}\/\d{2}'

AMATEUR_NAME_TEXT = '名前'

AMATEUR_THREE_SIZE_TEXT = 'サイズ'

RELEASE_DATE_TEXT = '商品発売日'

DELIVERY_DATE_TEXT = '配信開始日'

VIDEO_LEN_TEXT = '収録時間'

GENRE_INFO = 'ジャンル'

CENSORED_ID_META = 'censored_id'

FANZA_AGE_COOKIE = 'age_check_done'

FANZA_AGE_COOKIE_VAL = '1'

FANZA_ACTRESS_INFO = 'info_actress'

FANZA_DIRECTOR_INFO = 'info_director'

FANZA_MAKER_INFO = 'info_maker'

FANZA_LABEL_INFO = 'info_label'

FANZA_SERIES_INFO = 'info_series'

FANZA_BLACK_GENRE_LIST = [r'セール', r'ギリモザ', r'ハイビジョン', r'独占配信', r'単体作品', r'ブランドストア30％OFF！']

FANZA_COVER_SUB_REGEX = compile(r'ps(?=(\.jpg)*$)', IGNORECASE)

FANZA_COVER_SUB_STR = 'pl'

FANZA_PREVIEW_SUB_REGEX = compile(r'-(?=\d{1,2}(\.jpg)*$)')

FANZA_PREVIEW_SUB_STR = 'jp-'

FANZA_AMATEUR_PREVIEW_SUB_REGEX = compile(r'\w{2}(?=-\d{3,4}(\.jpg){0,1}$)')

FANZA_AMATEUR_PREVIEW_SUB_STR = 'jp'

FANZA_PREVIEW_NUM_REGEX = r'(?<=-)\d+(?=\.jpg)'

FANZA_AMATEUR_PREVIEW_NUM_REGEX = r'(?<=-00)\d{1,2}(?=\.jpg$)'

FANZA_IMAGE_NAME_SUB_REGEX = compile(r'(?<=[A-Za-z])0{2}(?=\d)')

FANZA_IMAGE_NAME_SUB_STR = '-'

MGS_BLACK_GENRE_LIST = [r'MGSだけのおまけ映像付き']

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

MGS_LOW_RES_COVER_URL_SUB_REGEX = compile(r'(?<=\/)pb_p(?=_)')

MGS_LOW_RES_COVER_URL_SUB_STR = 'pf_t1'

HIGH_PREVIEW_IMAGE_FORMATTER = '{}jp-{}'

LOW_PREVIEW_IMAGE_FORMATTER = '{}-{}'

MGS_LOW_RES_PREVIEW_REGEX = r'(?<=cap_t1_)\d+(?=_)'

MGS_HIGH_RES_PREVIEW_REGEX = r'(?<=cap_e_)\d+(?=_)'

MGS_LOW_RES_IMG_URL_KEY = 'low_res_url'

MSG_HIGH_RES_IMG_URL_KEY = 'high_res_url'
