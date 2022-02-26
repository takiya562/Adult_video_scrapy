# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from fanza.items import ImageItem
from fanza.common import download_image
from fanza.image.image_helper import handle_image_item

from scrapy.exceptions import DropItem
from scrapy import Spider

from time import sleep
from socket import timeout
from urllib.request import ProxyHandler, build_opener
from urllib.error import URLError, HTTPError
from os.path import isdir, isfile
from os import makedirs

class AvbookImagePipeline:
    def __init__(self) -> None:
        self.opener = None

    def open_spider(self, spider: Spider):
        img_download_proxy = spider.settings['IMAGE_DOWNLOAD_PROXY']
        self.opener = build_opener(ProxyHandler({'https': img_download_proxy, 'http': img_download_proxy}))
        self.img_fail = spider.settings['IMAGE_FAIL_FILE']
        self.failed = set()
    
    async def process_item(self, item, spider: Spider):
        if not isinstance(item, ImageItem):
            return item
        img_dir, img_des, prefix = handle_image_item(item, spider)
        if not isdir(img_dir):
            makedirs(img_dir)
        if not item.isUpdate and isfile(img_des):
            spider.logger.debug('already exist: %s %s', prefix, item.imageName)
            return
        retry = 0
        delay = 1
        retry_limit = spider.settings['RETRY_LIMIT']
        while True:
            try:
                download_image(self.opener, item.url, img_des)
                break
            except (URLError, HTTPError, timeout):
                if retry > retry_limit:
                    spider.logger.exception("download image error, url: %s", item.url)
                    if item.subDir not in self.failed:
                        self.failed.add(item.subDir)
                        with open(self.img_fail, 'w', encoding='utf-8') as f:
                            f.write(f'{item.subDir}\n')
                    raise DropItem(f'download error happend\titem: {item}')
                sleep(delay)
                retry += 1
                delay *= 2
                spider.logger.debug('retry download image: retry\t%s url\t%s', retry, item.url)
        spider.logger.info('save img:\t%s %s', prefix, item.imageName)

class SuccessResponsePipeline:
    def close_spider(self, spider: Spider):
        if spider.name != 'movie_detail' and spider.name != 'movie_image':
            return
        spider.logger.info('------------------------------------save failed------------------------------------')
        failed = spider.processed - spider.successed
        with open('failed.txt', 'w', encoding='utf-8') as f:
            for failed_id in failed:
                f.write(failed_id + '\n')
