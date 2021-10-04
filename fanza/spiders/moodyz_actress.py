import scrapy


class MoodyzActressSpider(scrapy.Spider):
    name = 'moodyz_actress'
    allowed_domains = ['moodyz.com']
    start_urls = ['http://moodyz.com/']

    def parse(self, response):
        pass
