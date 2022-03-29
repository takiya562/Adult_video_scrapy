from scrapy.http import HtmlResponse
from fanza.common import normalize_space
from fanza.annotations import notnull

class ActressExtractor:
    def extract(self, response: HtmlResponse) -> dict:
        self.response = response
        image = self.extract_image()
        birth = self.extract_birth()
        three_size = self.extract_three_size()
        height = self.extract_height()
        birth_place = self.extract_birth_place()
        blood = self.extract_blood()
        hobby = self.extract_hobby()
        trick = self.extract_trick()
        return {
            "birth": birth,
            "three_size": three_size,
            "height": height,
            "birth_place": birth_place,
            "blood": blood,
            "hobby": hobby,
            "trick": trick,
            "maker": self.maker(),
        }

    @notnull
    def extract_image(self):
        return self.response.xpath('//div[@class="p-profile__imgArea"]//img/@data-src').get()

    def extract_birth(self):
        birth = self.response.xpath('//div[@class="p-profile__info"]/div[@class="table"]/div[@class="item"]/p[text()="誕生日"]/following-sibling::*/text()').get()
        return normalize_space(birth)

    def extract_three_size(self):
        three_size = self.response.xpath('//div[@class="p-profile__info"]/div[@class="table"]/div[@class="item"]/p[text()="3サイズ"]/following-sibling::*/text()').get()
        return normalize_space(three_size)

    def extract_height(self):
        height = self.response.xpath('//div[@class="p-profile__info"]/div[@class="table"]/div[@class="item"]/p[text()="身長"]/following-sibling::*/text()').get()
        return normalize_space(height)

    def extract_birth_place(self):
        birth_place = self.response.xpath('//div[@class="p-profile__info"]/div[@class="table"]/div[@class="item"]/p[text()="出身地"]/following-sibling::*/text()').get()
        return normalize_space(birth_place)
    
    def extract_blood(self):
        blood = self.response.xpath('//div[@class="p-profile__info"]/div[@class="table"]/div[@class="item"]/p[text()="血液型"]/following-sibling::*/text()').get()
        return normalize_space(blood)

    def extract_hobby(self):
        hobby = self.response.xpath('//div[@class="p-profile__info"]/div[@class="table"]/div[@class="item"]/p[text()="趣味"]/following-sibling::*/text()').get()
        return normalize_space(hobby)
    
    def extract_trick(self):
        trick = self.response.xpath('//div[@class="p-profile__info"]/div[@class="table"]/div[@class="item"]/p[text()="特技"]/following-sibling::*/text()').get()
        return normalize_space(trick)

    def maker(self):
        pass