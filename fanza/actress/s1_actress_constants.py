from re import compile

S1_ACTRESSID_META_KEY = 'id'

S1_ACTRESS_TITLE = 'ピックアップ女優'

S1_ACTRESS_DETAIL_BIRTH_TEXT = '誕生日'

S1_ACTRESS_DETAIL_HEIGHT_TEXT = '身長'

S1_ACTRESS_DETAIL_SIZE_TEXT = '3サイズ'

S1_ACTRESS_DETAIL_PLACE_TEXT = '出身地'

S1_ACTRESS_DETAIL_BLOOD_TYPE_TEXT = '血液型'

S1_ACTRESS_DETAIL_HOBBY_TEXT = '趣味'

S1_ACTRESS_DETAIL_TRICK_TEXT = '特技'

S1_ACTRESS_TWITTER_INDEX = 1

S1_ACTRESS_INS_INDEX = 2

S1_ACTRESS_PROFILE_CLEAN_REGEX = compile(r'\s*\n\s*')

S1_ACTRESS_PROFILE_CLEAN_STR = ''

S1_ACTRESS_ID_REGEX = r'(?<=\/)\d+$'

S1_ACTRESS_TOP = 'https://s1s1s1.com/actress'

S1_ACTRESS_TARGET_FORMATTER = 'https://s1s1s1.com/actress/detail/{}'

S1_ACTRESS_PROFILE_IMGNAME = 'profile'

S1_ACTRESS_GALLERY_IMGNAME_FORMATTER = "gallery-{}"

S1_ACTRESS_PROFILE_IMG_SUBDIR_FORMATTER = "s1/{}"