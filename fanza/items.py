# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item
from dataclasses import dataclass, field

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

class FanzaItem(Item):
    censoredId = Field()
    title = Field()
    actress = Field()
    director = Field()
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
class FanzaItem:
    censoredId: str = field(default=None)
    title: str = field(default=None)
    actress: dict = field(default=None)
    director: dict = field(default=None)
    makerId: int = field(default=None)
    makerName: str = field(default=None)
    labelId: int = field(default=None)
    labelName: str = field(default=None)
    seriesId: int = field(default=None)
    seriesName: str = field(default=None)
    releaseDate: str = field(default=None)
    videoLen: int = field(default=None)
    genre: dict = field(default=None)

class MgsItem(Item):
    censoredId = Field()
    title = Field()
    actressId = Field()
    actressName = Field()
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
class MgsItem:
    censoredId: str = field(default=None)
    title: str = field(default=None)
    actressId: int = field(default=None)
    actressName: str = field(default=None)
    makerId: int = field(default=None)
    makerName: str = field(default=None)
    labelId: int = field(default=None)
    labelName: str = field(default=None)
    seriesId: int = field(default=None)
    seriesName: str = field(default=None)
    releaseDate: str = field(default=None)
    videoLen: int = field(default=None)
    genre: list = field(default=None)

if __name__ == '__main__':
    test = FanzaImageItem('www.baidu.com', 'SIRO-4568', None)
    name = getattr(test, 'image')
    print(name)
