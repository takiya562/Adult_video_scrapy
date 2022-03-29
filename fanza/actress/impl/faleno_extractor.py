from fanza.actress.actress_extractor import ActressExtractor
from fanza.common import normalize_space
from fanza.annotations import notnull

class FalenoExtractor(ActressExtractor):
    def maker(self):
        return "faleno"

    @notnull
    def extract_image(self):
        return self.response.xpath('//div[@class="box_actress02_left"]/img/@src').get()

    def extract_birth(self):
        return self.response.xpath('//div[@class="box_actress02_list clearfix"]/ul/li/span[text()="誕生日"]/following-sibling::p/text()').get()

    def extract_three_size(self):
        return self.response.xpath('//div[@class="box_actress02_list clearfix"]/ul/li/span[text()="スリーサイズ"]/following-sibling::p/text()').get()

    def extract_height(self):
        return self.response.xpath('//div[@class="box_actress02_list clearfix"]/ul/li/span[text()="身長"]/following-sibling::p/text()').get()

    def extract_birth_place(self):
        return self.response.xpath('//div[@class="box_actress02_list clearfix"]/ul/li/span[text()="出身地"]/following-sibling::p/text()').get()

    def extract_hobby(self):
        return self.response.xpath('//div[@class="box_actress02_list clearfix"]/ul/li/span[text()="趣味"]/following-sibling::p/text()').get()

    def extract_trick(self):
        return self.response.xpath('//div[@class="box_actress02_list clearfix"]/ul/li/span[text()="特技"]/following-sibling::p/text()').get()

    def extract_blood(self):
        return None