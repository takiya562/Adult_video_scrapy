# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymysql import connect
from pymysql.err import OperationalError
from fanza.items import FanzaImageItem, FanzaItem
from urllib.request import urlretrieve
from os.path import isdir, isfile
from os import makedirs
import logging

class FanzaPipeline:
    pass

class FanzaImagePipeline:
    def process_item(self, item, spider):
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
