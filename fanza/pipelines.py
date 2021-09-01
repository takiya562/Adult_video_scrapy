# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymysql.err import OperationalError
from fanza.items import FanzaImageItem, FanzaItem, MgsItem
from urllib.request import urlretrieve, ProxyHandler, install_opener, build_opener
from os.path import isdir, isfile
from os import makedirs
from fanza.db import AvDB
from scrapy.exceptions import DropItem
from pymysql import ProgrammingError, IntegrityError
from pymysql.err import DataError, OperationalError
from fanza.db_error_msg_constatns import *
from fanza.extract_helper import save_crawled_to_file
from scrapy import Spider
import logging

class FanzaPipeline:
    def __init__(self):
        logging.info('------------------------------------Item pipeline init------------------------------------')
        self.db = None
        self.committed = [str]
        logging.info('--------------------------------Item pipeline init finish!--------------------------------')

    def open_spider(self, spider: Spider):
        host = spider.settings['MYSQL_HOST']
        port = spider.settings['MYSQL_PORT']
        databse = spider.settings['MYSQL_DATABASE']
        user = spider.settings['MYSQL_USER']
        passwd = spider.settings['MYSQL_PASSWD']
        logging.info('------------------------------------Connecting to mysql------------------------------------')
        try:
            self.db = AvDB(host=host, user=user, passwd=passwd, database=databse, port=port)
        except OperationalError as err:
            logging.error('Fail to connect mysql ->\n\terr: %s', err)
            self.close_spider()
        logging.info('------------------------------------Connection success-------------------------------------')

    def process_item(self, item, spider):
        if isinstance(item, FanzaItem):
            logging.info('--------------------------------------Sync fanza mysql start-------------------------------------')
            try:
                self.db.insert_fanza_movie(item)
            except ProgrammingError as err:
                self.db.rollback()
                logging.error(PROGRAMMING_ERROR_MSG, item.censoredId, err)
                raise DropItem(DROP_ITEM_PROGRAMMING_ERROR_MSG.format(item))
            except IntegrityError as err:
                logging.debug(INTEGRITY_ERROR_MSG, item.censoredId, err)
            except DataError as err:
                self.db.rollback()
                logging.error(DATA_ERROR_MSG, item.censoredId, err)
                raise DropItem(DROP_ITEM_DATA_ERROR_MSG.format(item))
            except AttributeError as err:
                self.db.rollback()
                logging.error(ATTRIBUTE_ERROR_MSG, item.censoredId, err)
                raise DropItem(DROP_ITEM_ATTRIBUTE_ERROR_MSG.format(item))
            # database sync succeeds, then add censored id to the list preparing to record crawled av
            self.committed.append(item.censoredId)
            logging.info('-------------------------------------Sync fanza mysql finished-----------------------------------')
        elif isinstance(item, MgsItem):
            logging.info('--------------------------------------Sync mgs mysql start-------------------------------------')
            try:
                self.db.insert_mgs_movie(item)
            except ProgrammingError as err:
                self.db.rollback()
                logging.error(PROGRAMMING_ERROR_MSG, item.censoredId, err)
                raise DropItem(DROP_ITEM_PROGRAMMING_ERROR_MSG.format(item))
            except IntegrityError as err:
                logging.debug(INTEGRITY_ERROR_MSG, item.censoredId, err)
            except DataError as err:
                self.db.rollback()
                logging.error(DATA_ERROR_MSG, item.censoredId, err)
                raise DropItem(DROP_ITEM_DATA_ERROR_MSG.format(item))
            except AttributeError as err:
                self.db.rollback()
                logging.error(ATTRIBUTE_ERROR_MSG, item.censoredId, err)
                raise DropItem(DROP_ITEM_ATTRIBUTE_ERROR_MSG.format(item))
            # database sync succeeds, then add censored id to the list preparing to record crawled av
            self.committed.append(item.censoredId)
            logging.info('-------------------------------------Sync mgs mysql finished-----------------------------------')
        return item

    def close_spider(self, spider: Spider):
        # write the crawled av into specified file (see CRAWLED_FILE in settings)
        for committed in self.committed:
            save_crawled_to_file(committed, spider.settings['CRAWLED_FILE'])
        if self.db is not None:
            self.db.close()


class FanzaImagePipeline:
    def open_spider(self, spider):
        logging.info('------------------------------------Image pipeline init------------------------------------')
        proxy = ProxyHandler({'http': '127.0.0.1:8181'})
        opener = build_opener(proxy)
        install_opener(opener)

    def process_item(self, item, spider: Spider):
        if not isinstance(item, FanzaImageItem):
            return item
        img_base_folder = spider.settings['IMG_BASE_FOLDER']
        if item.isCover:
            cover_img_dir = r'%s/%s' % (img_base_folder, item.censoredId)
            cover_img_des = r'%s/%s.jpg' % (cover_img_dir, item.image)
            if not isdir(cover_img_dir):
                makedirs(cover_img_dir)
            if isfile(cover_img_des):
                logging.info('already exist %s', item.image)
                return
            urlretrieve(item.url, cover_img_des)
            logging.info('save cover %s', item.image)
        else:
            preview_img_dir = r'%s/%s/preview' % (img_base_folder, item.censoredId)
            preview_img_des = r'%s/%s.jpg' % (preview_img_dir, item.image)
            if not isdir(preview_img_dir):
                makedirs(preview_img_dir)
            if isfile(preview_img_des):
                logging.info('already exist %s', item.image)
                return
            urlretrieve(item.url, preview_img_des)
            logging.info('save preview %s', item.image)
