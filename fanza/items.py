# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from logging import debug
from typing import Any, Callable
from scrapy.item import Field, Item
from dataclasses import dataclass, field

class ItemMap:
    def __init__(self, item_name: str, type: type, callback: Callable[[Item], Any]) -> None:
        self.itemName = item_name
        self.type = type
        self.callback = callback
    
class RequestStatusItem(Item):
    censored_id = Field()
    flag = Field()

@dataclass
class RequestStatusItem:
    censored_id: str = field(default=None)
    flag: int = field(default=0)

class AvbookActressBasicItem(Item):
    id = Field()
    actressName = Field()

@dataclass
class AvbookActressBasicItem:
    id: int = field(default=None)
    actressName: str = field(default=None)

class AvbookMovieBasicItem(Item):
    censoredId = Field()
    title = Field()
    videoLen = Field()

@dataclass
class AvbookMovieBasicItem:
    censoredId: str = field(default=None)
    title: str = field(default=None)
    videoLen: int = field(default=None)

class ImageItem(Item):
    url = Field()
    subDir = Field()
    imageName = Field()
    isUpdate = Field()

@dataclass
class ImageItem:
    url: str = field(default=None)
    subDir: str = field(default=None)
    imageName: str = field(default=None)
    isUpdate: int = field(default=0)

class MovieImageItem(ImageItem):
    isCover = Field()

@dataclass
class MovieImageItem(ImageItem):
    isCover: int = field(default=0)

class ActressImageItem(ImageItem):
    actress = Field()
    isGallery = Field()

@dataclass
class ActressImageItem(ImageItem):
    actress: str = field(default=None)
    isGallery: int = field(default=0)

class FanzaImageItem(Item):
    url = Field()
    censoredId = Field()
    image = Field()
    isCover = Field()

@dataclass
class FanzaImageItem:
    url: str = field(default=None)
    censoredId: str = field(default=None)
    image: str = field(default=None)
    isCover: int = field(default=0)

class FanzaItem(AvbookMovieBasicItem):
    actress = Field()
    director = Field()
    makerId = Field()
    makerName = Field()
    labelId = Field()
    labelName = Field()
    seriesId = Field()
    seriesName = Field()
    releaseDate = Field()
    genre = Field()

@dataclass
class FanzaItem(AvbookMovieBasicItem):
    actress: dict = field(default=None)
    director: dict = field(default=None)
    makerId: int = field(default=None)
    makerName: str = field(default=None)
    labelId: int = field(default=None)
    labelName: str = field(default=None)
    seriesId: int = field(default=None)
    seriesName: str = field(default=None)
    releaseDate: str = field(default=None)
    genre: dict = field(default=None)

class MgsItem(AvbookMovieBasicItem):
    actress = Field()
    makerId = Field()
    makerName = Field()
    labelId = Field()
    labelName = Field()
    seriesId = Field()
    seriesName = Field()
    releaseDate = Field()
    videoLen = Field()
    genre = Field()

@dataclass
class MgsItem(AvbookMovieBasicItem):
    actress: list = field(default=None)
    makerId: int = field(default=None)
    makerName: str = field(default=None)
    labelId: int = field(default=None)
    labelName: str = field(default=None)
    seriesId: int = field(default=None)
    seriesName: str = field(default=None)
    releaseDate: str = field(default=None)
    genre: list = field(default=None)

class FanzaAmateurItem(AvbookMovieBasicItem):
    amateur = Field()
    threeSize = Field()
    labelId = Field()
    labelName = Field()
    deliveryDate = Field()
    genre = Field()

@dataclass
class FanzaAmateurItem(AvbookMovieBasicItem):
    amateur: str = field(default=None)
    threeSize: str = field(default=None)
    labelId: int = field(default=None)
    labelName: str = field(default=None)
    deliveryDate: str = field(default=None)
    genre: dict = field(default=None)

if __name__ == '__main__':
    test = MgsItem()
    print(isinstance(test, AvbookMovieBasicItem))

class S1ActressItem(AvbookActressBasicItem):
    actressNameEn = Field()
    birth = Field()
    height = Field()
    threeSize = Field()
    birthPlace = Field()
    bloodType = Field()
    hobby = Field()
    trick = Field()
    twitter = Field()
    ins = Field()

@dataclass
class S1ActressItem(AvbookActressBasicItem):
    actressNameEn: str = field(default=None)
    birth: str = field(default=None)
    height: str = field(default=None)
    threeSize: str = field(default=None)
    birthPlace: str = field(default=None)
    bloodType: str = field(default=None)
    hobby: str = field(default=None)
    trick: str = field(default=None)
    twitter: str = field(default=None)
    ins: str = field(default=None)

class PrestigeActressItem(AvbookActressBasicItem):
    actressNameEn = Field()
    birth = Field()
    height = Field()
    threeSize = Field()
    birthPlace = Field()
    bloodType = Field()
    hobbyTrick = Field()
    twitter = Field()
    ins = Field()

@dataclass
class PrestigeActressItem(AvbookActressBasicItem):
    actressNameEn: str = field(default=None)
    birth: str = field(default=None)
    height: str = field(default=None)
    threeSize: str = field(default=None)
    birthPlace: str = field(default=None)
    bloodType: str = field(default=None)
    hobbyTrick: str = field(default=None)
    twitter: str = field(default=None)
    ins: str = field(default=None)

class FalenoActressItem(AvbookActressBasicItem):
    actressNameEn = Field()
    birth = Field()
    height = Field()
    threeSize = Field()
    birthPlace = Field()
    hobby = Field()
    trick = Field()

@dataclass
class FalenoActressItem(AvbookActressBasicItem):
    actressNameEn: str = field(default=None)
    birth: str = field(default=None)
    height: str = field(default=None)
    threeSize: str = field(default=None)
    birthPlace: str = field(default=None)
    hobby: str = field(default=None)
    trick: str = field(default=None)
