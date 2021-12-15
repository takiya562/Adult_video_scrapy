# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from fanza.items import AvbookActressBasicItem, AvbookMovieBasicItem, FanzaImageItem, ImageItem, ItemMap, RequestStatusItem, SuccessResponseItem
from fanza.common import download_image, save_crawled_to_file
from fanza.database.db import AvDB
from fanza.database.db_error_msg_constatns import *
from fanza.movie.movie_constants import FAIL_MOVIE_FLAG
from fanza.image.image_helper import handle_image_item

import logging
from scrapy.exceptions import DropItem
from scrapy import Spider
from pymysql.err import OperationalError
from pymysql.err import OperationalError
from deprecated.sphinx import deprecated

from time import sleep
from socket import timeout
from urllib.request import urlretrieve, ProxyHandler, build_opener
from urllib.error import URLError
from os.path import isdir, isfile
from os import makedirs

class FanzaPipeline:
    def __init__(self):
        logging.info('------------------------------------Item pipeline init------------------------------------')
        self.db = None
        self.committedMovie = set()
        self.committedActress = set()
        self.commitChain = [
            ItemMap('Avbook Movie', AvbookMovieBasicItem, self.commit_movie),
            ItemMap('Avbook Actress', AvbookActressBasicItem, self.commit_actress),
        ]
        self.logger = logging.getLogger('pipeline-database')
        logging.info('--------------------------------Item pipeline init finish!--------------------------------')

    def open_spider(self, spider: Spider):
        host = spider.settings['MYSQL_HOST']
        port = spider.settings['MYSQL_PORT']
        databse = spider.settings['MYSQL_DATABASE']
        user = spider.settings['MYSQL_USER']
        passwd = spider.settings['MYSQL_PASSWD']
        spider.logger.info('------------------------------------Connecting to mysql------------------------------------')
        try:
            self.db = AvDB(host=host, user=user, passwd=passwd, database=databse, port=port)
        except OperationalError as err:
            spider.logger.exception('fail to connect mysql', exc_info=err)
            self.close_spider()
        spider.logger.info('------------------------------------Connection success-------------------------------------')

    def process_item(self, item, spider: Spider):
        res = self.db.trans_dispatch(item)
        for map in self.commitChain:
            if isinstance(item, map.type):
                spider.logger.info('--------------------------------------Commit %s %s-------------------------------------', map.itemName, res)
                map.callback(item)
        return item

    def close_spider(self, spider: Spider):
        # write the crawled av into specified file (see CRAWLED_FILE in settings)
        spdier_map_committed_file = spider.settings['SPIDER_ACTRESS_CRAWLED_FILE_MAP']
        spider.logger.info('movie sync to mysql: total\t%d', len(self.committedMovie))
        spider.logger.info('actress sync to mysql: total\t%d', len(self.committedActress))
        for committed in self.committedMovie:
            save_crawled_to_file(committed, spider.settings['CRAWLED_FILE'])
        for committed in self.committedActress:
            committed_file = spdier_map_committed_file.get(spider.name)
            save_crawled_to_file(committed, committed_file)
        if self.db is not None:
            self.db.close()

    def commit_movie(self, item: AvbookMovieBasicItem):
        self.committedMovie.add(item.censoredId)
    
    def commit_actress(self, item: AvbookActressBasicItem):
        self.committedActress.add(item.id)

@deprecated(version='1.0', reason="This pipeline has been replaced by AvbookImagePipeline")
class FanzaImagePipeline:
    def process_item(self, item, spider: Spider):
        if not isinstance(item, FanzaImageItem):
            return item
        img_base_folder = spider.settings['MOVIE_IMG_BASE_FOLDER']
        if item.isCover:
            cover_img_dir = r'%s/%s' % (img_base_folder, item.censoredId)
            cover_img_des = r'%s/%s.jpg' % (cover_img_dir, item.image)
            if not isdir(cover_img_dir):
                makedirs(cover_img_dir)
            if isfile(cover_img_des):
                spider.logger.info('already exist %s', item.image)
                return
            urlretrieve(item.url, cover_img_des)
            spider.logger.info('save cover %s', item.image)
        else:
            preview_img_dir = r'%s/%s/preview' % (img_base_folder, item.censoredId)
            preview_img_des = r'%s/%s.jpg' % (preview_img_dir, item.image)
            if not isdir(preview_img_dir):
                makedirs(preview_img_dir)
            if isfile(preview_img_des):
                spider.logger.info('already exist %s', item.image)
                return
            urlretrieve(item.url, preview_img_des)
            spider.logger.info('save preview %s', item.image)

class AvbookImagePipeline:
    def __init__(self) -> None:
        self.opener = None

    def open_spider(self, spider: Spider):
        img_download_proxy = spider.settings['IMAGE_DOWNLOAD_PROXY']
        self.opener = build_opener(ProxyHandler({'https': img_download_proxy, 'http': img_download_proxy}))
    
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
            except (URLError, timeout):
                if retry > retry_limit:
                    spider.logger.exception("download image error, url: %s", item.url)
                    raise DropItem(DROP_ITEM_DOWNLOAD_ERROR_MSG.format(item))
                sleep(delay)
                retry += 1
                delay *= 2
                spider.logger.debug('retry download image: retry\t%s url\t%s', retry, item.url)
        spider.logger.info('save img:\t%s %s', prefix, item.imageName)

class SuccessResponsePipeline:
    def close_spider(self, spider: Spider):
        for success_response in spider.successed:
            save_crawled_to_file(success_response, spider.settings['CRAWLED_FILE'])
        failed = spider.processed - spider.successed
        with open('failed.txt', 'w', encoding='utf-8') as f:
            for failed_id in failed:
                f.write(failed_id + '\n')
        
class RequestStatusPipline:
    def __init__(self) -> None:
        self.reqDict = dict()
        self.badCommitted = 'failed.txt'

    def process_item(self, item, spider: Spider):
        if not isinstance(item, RequestStatusItem):
            return item
        flag = self.reqDict.get(item.censored_id, 0)
        flag |= item.flag
        self.reqDict[item.censored_id] = flag

    def close_spider(self, spider: Spider):
        fail_file = spider.settings['FAIL_FILE']
        if fail_file != '':
            self.badCommitted = fail_file
        with open(self.badCommitted, 'w', encoding='utf-8') as f:
            for censored_id, flag in self.reqDict.items():
                if flag == FAIL_MOVIE_FLAG:
                    f.write(censored_id + '\n')
