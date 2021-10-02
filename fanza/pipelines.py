# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from fanza.image_helper import handle_image_item
from pymysql.err import OperationalError
from fanza.items import AvbookActressBasicItem, AvbookMovieBasicItem, FanzaImageItem, ImageItem, ItemMap, PrestigeActressItem, S1ActressItem, BadRequestItem
from urllib.request import urlretrieve, ProxyHandler, install_opener, build_opener
from os.path import isdir, isfile
from os import makedirs
from fanza.db import AvDB
from pymysql.err import OperationalError
from fanza.db_error_msg_constatns import *
from fanza.common import download_image, save_crawled_to_file, save_to_file
from scrapy import Spider
import logging
from fanza.movie_constants import FAIL_MOVIE_FLAG

class FanzaPipeline:
    def __init__(self):
        logging.info('------------------------------------Item pipeline init------------------------------------')
        self.db = None
        self.committedMovie = set()
        self.committedActress = set()
        self.commitChain = [
            ItemMap('Avbook Movie', AvbookMovieBasicItem, self.commit_movie),
            ItemMap('Avbook S1 Actress', S1ActressItem, self.commit_actress),
            ItemMap('Avbook Prestige Actress', PrestigeActressItem, self.commit_actress)
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
            spider.logger.error('Fail to connect mysql ->\n\terr: %s', err)
            self.close_spider()
        self.logger.info('------------------------------------Connection success-------------------------------------')

    def process_item(self, item, spider):
        res = self.db.trans_dispatch(item)
        for map in self.commitChain:
            if isinstance(item, map.type):
                self.logger.info('--------------------------------------Commit %s %s-------------------------------------', map.itemName, res)
                map.callback(item)
        return item

    def close_spider(self, spider: Spider):
        # write the crawled av into specified file (see CRAWLED_FILE in settings)
        spdier_map_committed_file = spider.settings['SPIDER_ACTRESS_CRAWLED_FILE_MAP']
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

class FanzaImagePipeline:
    def __init__(self) -> None:
        self.logger = logging.getLogger('pipeline-image')

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
                self.logger.info('already exist %s', item.image)
                return
            urlretrieve(item.url, cover_img_des)
            self.logger.info('save cover %s', item.image)
        else:
            preview_img_dir = r'%s/%s/preview' % (img_base_folder, item.censoredId)
            preview_img_des = r'%s/%s.jpg' % (preview_img_dir, item.image)
            if not isdir(preview_img_dir):
                makedirs(preview_img_dir)
            if isfile(preview_img_des):
                self.logger.info('already exist %s', item.image)
                return
            urlretrieve(item.url, preview_img_des)
            self.logger.info('save preview %s', item.image)

class AvbookImagePipeline:
    def __init__(self) -> None:
        self.logger = logging.getLogger('pipeline-avbook-image')
        self.opener = None

    def open_spider(self, spider: Spider):
        img_download_proxy = spider.settings['IMAGE_DOWNLOAD_PROXY']
        self.opener = build_opener(ProxyHandler({'http': img_download_proxy}))
    
    async def process_item(self, item, spider: Spider):
        if not isinstance(item, ImageItem):
            return item
        img_dir, img_des, prefix = handle_image_item(item, spider)
        if not isdir(img_dir):
            makedirs(img_dir)
        if not item.isUpdate and isfile(img_des):
            self.logger.debug('already exist:\t%s %s', prefix, item.imageName)
            return
        download_image(self.opener, item.url, img_des)
        self.logger.info('save img:\t%s %s', prefix, item.imageName)
        
class BadRequestPipline:
    def __init__(self) -> None:
        self.logger = logging.getLogger('pipline-bad-request')
        self.badMap = dict()
        self.badCommitted = 'failed.txt'

    def process_item(self, item, spider: Spider):
        if not isinstance(item, BadRequestItem):
            return item
        flag = self.badMap.get(item.censored_id, 0)
        flag |= item.flag
        self.badMap[item.censored_id] = flag

    def close_spider(self, spider: Spider):
        fail_file = spider.settings['FAIL_FILE']
        if fail_file != '':
            self.badCommitted = fail_file
        with open(self.badCommitted, 'w', encoding='utf-8') as f:
            for censored_id, flag in self.badMap.items():
                if flag == FAIL_MOVIE_FLAG:
                    f.write(censored_id + '\n')
