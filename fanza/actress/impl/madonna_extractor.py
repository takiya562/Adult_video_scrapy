from fanza.actress.actress_extractor import ActressExtractor
from fanza.common import normalize_space
from fanza.annotations import notnull

class MadonnaExtractor(ActressExtractor):
    madonna_base_url = "https://www.madonna-av.com"

    def maker(self):
        return "madonna"
    
    @notnull
    def extract_image(self):
        image_path = self.response.xpath('//div[@class="actress-detail-image"]/img/@src').get()
        return self.madonna_base_url + image_path

    def extract_three_size(self):
        three_size = " ".join(self.response.xpath('//div[@class="actress-detail-info"]/dl/dt[text()="サイズ"]/following-sibling::dd/span/text()').getall())
        return normalize_space(three_size)

    def extract_height(self):
        height = self.response.xpath('//div[@class="actress-detail-info"]/dl/dt[text()="身長"]/following-sibling::dd/text()').get()
        return normalize_space(height)

    def extract_birth(self):
        return None

    def extract_birth_place(self):
        return None

    def extract_blood(self):
        return None

    def extract_hobby(self):
        return None

    def extract_trick(self):
        return None
