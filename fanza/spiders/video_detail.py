from itemloaders.processors import TakeFirst
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from haralyzer import HarParser
from re import search, IGNORECASE
from fanza.fanza_exception import ExtractException, EmptyGenreException, FormatException
from fanza.items import FanzaImageItem, FanzaItem
import logging
from fanza.constants import *
from fanza.extract_helper import *

class VideoDetailSpider(Spider):
    name = 'video_detail'
    allowed_domains = ['dmm.co.jp']

    def __init__(self, *args, **kwargs):
        super(VideoDetailSpider, self).__init__(*args, **kwargs)
        self.fanza_script = """
        function main(splash, args)
        splash:add_cookie{"age_check_done", "1", "/", domain=".dmm.co.jp"}
        splash.images_enabled = true
        splash.js_enabled = false
        assert(splash:go{args.url})
        assert(splash:wait(0.5))
        return {
            html = splash:html(),
            har = splash:har()
        }
        end
        """
        self.mgstage_script = """
        function main(splash, args)
        splash:add_cookie{"adc", "1", "/", domain=".mgstage.com"}
        splash.images_enabled = true
        splash.js_enabled = false
        assert(splash:go{args.url})
        assert(splash:wait(0.5))
        return {
            html = splash:html(),
            har = splash:har()
        }
        end
        """
    def produce_fanza(self, censored_id: str):
        try:
            url = r'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=%s/' % format_censored_id(censored_id)
        except FormatException as err:
            self.logger.error('build request url error ->\n\t%s' % err.message)
            pass
        return SplashRequest(url, endpoint="execute",
                            args={'lua_source': self.fanza_script},
                            meta={'censored_id': censored_id},
                            callback=self.parse)

    def produce_mgstage(self, censored_id: str):
        url = r'https://www.mgstage.com/product/product_detail/%s/' % censored_id
        return SplashRequest(url, endpoint='execute',
                            args={'lua_source': self.mgstage_script},
                            meta={'censored_id': censored_id},
                            callback=self.parse_mgstage)


    def start_requests(self):
        video_dir = self.settings['VIDEO_DIR']
        ext_white_list = self.settings['EXT_WHITE_LIST']
        crawled = get_crawled(self.settings['CRAWLED_FILE'])
        for censored_id in scan_video_dir(video_dir, ext_white_list):
            if censored_id in crawled:
                self.logger.debug('%s is already crawled' % censored_id)
                continue
            yield self.produce_fanza(censored_id)
            yield self.produce_mgstage(censored_id)
                                

    # fanza parse
    def parse(self, response, **kwargs):
        censored_id = response.meta['censored_id']
        if response.status == 404:
            logging.info('Can not find video %s in fanza or wrong censored id', censored_id)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", censored_id)
        self.logger.info("url: %s", response.url)
        il = ItemLoader(item=FanzaItem())
        il.default_output_processor = TakeFirst()
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        title = response.xpath('//h1[@id="title"]/text()').get()
        il.add_value('censoredId', censored_id)
        il.add_value('title', title)
        self.logger.info("Video id: %s", censored_id)
        self.logger.info("Video title: %s", title)
        try:
            # extract actress info
            actress = fanza_extract_actress_info(response)
            # extract director info
            director_id, director_name = fanza_extract_video_info(response, FANZA_DIRECTOR_INFO)
            # extract maker info
            maker_id, maker_name = fanza_extract_video_info(response, FANZA_MAKER_INFO)
            # extract label info
            label_id, label_name = fanza_extract_video_info(response, FANZA_LABEL_INFO)
            # extract series info
            series_id, series_name = fanza_extract_video_info(response, FANZA_SERIES_INFO)
        except ExtractException as err:
            logging.error("extract info_x error ->\n\tmsg: %s\n\turl: %s", err.message, err.url)
            return
        for actress_id, actress_name in actress.items():
            self.logger.info("extract actress info -> actress_id: %s \t actress_name: %s", actress_id, actress_name)
        il.add_value('actress', actress)
        self.logger.info("extract director info -> director_id: %s \t director_name: %s", director_id, director_name)
        il.add_value('directorId', director_id)
        il.add_value('directorName', director_name)
        self.logger.info("extract maker info -> maker_id: %s \t maker_name: %s", maker_id, maker_name)
        il.add_value('makerId', maker_id)
        il.add_value('makerName', maker_name)
        self.logger.info("extract label info -> label_id: %s \t label_name: %s", label_id, label_name)
        il.add_value('labelId', label_id)
        il.add_value('labelName', label_name)
        self.logger.info("extract series info -> series_id: %s \t series_name: %s", series_id, series_name)
        il.add_value('seriesId', series_id)
        il.add_value('seriesName', series_name)
        # extract release date and video length
        try:
            release_date = fanza_extract_meta_info(response, RELEASE_DATE_TEXT)
            video_len = fanza_format_video_len(fanza_extract_meta_info(response, VIDEO_LEN_TEXT))
        except ExtractException as err:
            logging.error("extract meta info error ->\n\tmsg: %s\n\turl: %s", err.message, err.url)
            return
        except FormatException as err:
            logging.error("format data error ->\n\tmsg: %s\n\turl: %s", err.message, response.url)
            return
        self.logger.info("extract video info -> release_data: %s \t video_len: %s", release_date, video_len)
        il.add_value('releaseDate', release_date)
        il.add_value('videoLen', video_len)
        try:
            genre = fanza_extract_genre_info(response)
        except EmptyGenreException as err:
            self.logger.info("attention please ->\n\tmsg: %s\n\turl: %s", err.message, err.url)
            genre = {}
        for genre_id, genre_name in genre.items():
            self.logger.info("extract genre info -> genre_id: %s \t genre_name: %s", genre_id, genre_name)
        il.add_value('genre', genre)
        yield il.load_item()
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        har_data = HarParser(response.data['har']).har_data
        for item in har_data['entries']:
            url = item["request"]["url"]
            if search(r'\.jpg$', url) and search(r'/digital/video', url):
                # har contains thumbnail of video cover and preview pictures
                img_name_m = search(r'(?<=/)[^/]*(?=\.jpg)', url)
                if img_name_m:
                    img_name = format_image_name(img_name_m.group())
                    if search(r'ps$', img_name, IGNORECASE):
                        # replace 'ps' with 'pl' for hi-res cover
                        pl = FANZA_COVER_SUB_REGEX.sub(FANZA_COVER_SUB_STR, url)
                        # lowercase 'PS' for tidy
                        lowercase_ps = FANZA_COVER_SUB_REGEX.sub('ps', img_name)
                        pl_name = FANZA_COVER_SUB_REGEX.sub(FANZA_COVER_SUB_STR, img_name)
                        yield FanzaImageItem(pl, censored_id, pl_name, 1)
                        yield FanzaImageItem(url, censored_id, lowercase_ps, 1)
                    else:
                        # append 'jp' to the end of video id for hi-res preview pictures
                        jp = FANZA_PREVIEW_SUB_REGEX.sub(FANZA_PREVIEW_SUB_STR, url)
                        jp_name = FANZA_PREVIEW_SUB_REGEX.sub(FANZA_PREVIEW_SUB_STR, img_name)
                        yield FanzaImageItem(jp, censored_id, jp_name)
                        yield FanzaImageItem(url, censored_id, img_name)
        save_crawled_to_file(censored_id, self.settings['CRAWLED_FILE'])
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)

    # mgstage parse
    def parse_mgstage(self, response, **kwargs):
        censored_id = response.meta['censored_id']
        if response.status == 404:
            logging.error('Can not find video %s in fanza and mgstage or wrong censored id')
            pass
        self.logger.info("------------------------------------parse %s start------------------------------------", censored_id)
        self.logger.info("url: %s", response.url)
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        try:
            title = response.xpath('//h1[@class="tag"]/text()').get()
            title = mgs_clean_title(title)
            video_len = mgs_extract_meta_info(response, VIDEO_LEN_TEXT)
            video_len = mgs_format_video_len(video_len)
            release_date = mgs_extract_meta_info(response, RELEASE_DATE_TEXT)
            actress = mgs_extract_video_info(response, MGS_ACTRESS_INFO)
            actress = mgs_format_text(actress)
            maker = mgs_extract_video_info(response, MGS_MAKER_INFO)
            maker = mgs_format_text(maker)
            label = mgs_extract_video_info(response, MGS_LABEL_INFO)
            label = mgs_format_text(label)
            series = mgs_extract_video_info(response, MGS_SERIES_INFO)
            series = mgs_format_text(series)
        except FormatException as err:
            logging.error('format error ->\n\tmsg: %s \t url: %s', err.message, response.url)
            return
        except ExtractException as err:
            logging.error('extract error ->\n\tmsg: %s \t url: %s', err.message, err.url)
            return
        self.logger.info("Video id: %s", censored_id)
        self.logger.info("Video title: %s", title)
        self.logger.info("extract actress info -> actress: %s", actress)
        self.logger.info("extract maker info -> maker: %s", maker)
        self.logger.info("extract label info -> label: %s", label)
        self.logger.info("extract series info -> series: %s", series)
        self.logger.info("extract video info -> release_data: %s \t video_len: %s", release_date, video_len)
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)
