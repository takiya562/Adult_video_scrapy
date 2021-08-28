import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from fanza.spiders.video_detail import VideoDetailSpider
from scrapy.utils.project import get_project_settings

logging.basicConfig(filename='error.log', filemode='w', level=logging.ERROR)
s = get_project_settings()
runner = CrawlerRunner(s)
d = runner.crawl(VideoDetailSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()