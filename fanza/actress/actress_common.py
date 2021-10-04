from fanza.actress.actress_constants import *

def build_flag(mode: str):
    flag = 0
    for s in mode.split('-'):
        flag |= MODE_MAP.get(s, 0)
    if flag & ACTRESS_AGGR_MODE == 0:
        flag |= ACTRESS_AGGR_MODE
    return flag

def isUpdate(flag: int):
    return flag & ACTRESS_UPDATE_MODE

def isGround(flag: int):
    return flag & ACTRESS_TOP_GROUND_MODE != 0

def isTarget(flag: int):
    return flag & ACTRESS_TARGET_MODE != 0

def isImage(flag: int):
    return flag & ACTRESS_IMAGE_MODE != 0