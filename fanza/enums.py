from enum import Enum

class Actress(Enum):
    FANZA = 'info_actress'
    MGSTAGE = '出演'
    SOD = '出演者'

class VideoLen(Enum):
    FANZA = '収録時間'
    MGSTAGE = '収録時間'
    SOD = '再生時間'

class ReleaseDate(Enum):
    FANZA = '商品発売日'
    MGSTAGE = '商品発売日'
    SOD = '発売年月日'

class DeliveryDate(Enum):
    FANZA = '配信開始日'
    MGSTAGE = '配信開始日'

class Maker(Enum):
    FANZA = 'info_maker'
    MGSTAGE = 'メーカー'
    SOD = 'メーカー'

class Label(Enum):
    FANZa = 'info_label'
    MGSTAGE = 'レーベル'
    SOD = 'レーベル'

class Genre(Enum):
    FANZA = 'info_genre'
    MGSTAGE = 'ジャンル'
    SOD = 'ジャンル'

class Series(Enum):
    FANZA = 'info_series'
    MGSTAGE = 'シリーズ'
    SOD = 'シリーズ名'

class Director(Enum):
    FANZA = 'info_director'
    SOD = '監督'

class AgeCookie(Enum):
    FANZA = 'age_check_done'
    MGSTAGE = 'adc'

class AgeCookieVal(Enum):
    FANZA = '1'
    MGSTAGE = '1'