from fanza.image_constants import *
from fanza.items import ImageItem, MovieImageItem, ActressImageItem
from scrapy import Spider

def handle_image_item(item: ImageItem, spider: Spider):
    if isinstance(item, MovieImageItem):
        return handle_movie_image_item(item, spider)
    if isinstance(item, ActressImageItem):
        return handle_actress_image_item(item, spider)

def handle_movie_image_item(item: MovieImageItem, spider: Spider):
    base_folder = spider.settings['MOVIE_IMG_BASE_FOLDER']
    if item.isCover :
        img_dir = MOVIE_COVER_IMG_DIR_FORMATTER.format(base_folder, item.subDir)
    else:
        img_dir = MOVIE_PREVIEW_IMG_DIR_FORMATTER.format(base_folder, item.subDir)
    img_des = IMG_DES_FORMATTER.format(img_dir, item.imageName)
    return img_dir, img_des, 'Movie'

def handle_actress_image_item(item: ActressImageItem, spider: Spider):
    base_folder = spider.settings['ACTRESS_IMG_BASE_FOLDER']
    if item.isGallery:
        img_dir = ACTRESS_GALLERY_IMG_DIR_FORMATTER.format(base_folder, item.subDir)
    else:
        img_dir = ACTRESS_PROFILE_IMG_DIR_FORMATTER.format(base_folder, item.subDir)
    img_des = IMG_DES_FORMATTER.format(img_dir, item.imageName)
    return img_dir, img_des, item.actress