from re import search, compile, IGNORECASE

RELEASE_DATE_TEXT = '商品発売日'

VIDEO_LEN_TEXT = '収録時間'

GENRE_INFO = 'ジャンル'

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

FANZA_IMAGE_NAME_SUB_REGEX = compile(r'(?<=[A-Za-z])0{2}(?=\d)')

FANZA_IMAGE_NAME_SUB_STR = '-'

MGS_FORMAT_REGEX = compile(r'\s*\n\s*')

MGS_TITLE_SUB_REGEX = compile(r'【.*MGS.*】')

MGS_SUB_STR = ''

MGS_ACTRESS_INFO = '出演'

MGS_MAKER_INFO = 'メーカー'

MGS_SERIES_INFO = 'シリーズ'

MGS_LABEL_INFO = 'レーベル'
