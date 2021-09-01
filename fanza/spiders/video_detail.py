from scrapy import Spider, Request
from re import search, match
from fanza.fanza_exception import ExtractException, EmptyGenreException, FormatException
from fanza.items import FanzaItem, FanzaImageItem, MgsItem
import logging
from fanza.constants import *
from fanza.extract_helper import *
from fanza.error_msg_constants import *
from fanza.url_factroy import fanza_url_factory, mgs_url_factory

class VideoDetailSpider(Spider):
    name = 'video_detail'
    allowed_domains = ['dmm.co.jp']

    def produce_fanza(self, censored_id: str):
        url = fanza_url_factory.get_url(censored_id)
        logging.info('Formatted url: %s', url)
        return Request(url, cookies={FANZA_AGE_COOKIE: FANZA_AGE_COOKIE_VAL}, meta={CENSORED_ID_META: censored_id}, callback=self.parse)

    def produce_mgstage(self, censored_id: str):
        url = mgs_url_factory.get_url(censored_id)
        return Request(url, cookies={MGS_AGE_COOKIE: MGS_AGE_COOKIE_VAL}, callback=self.parse_mgstage, meta={CENSORED_ID_META: censored_id})

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
    def parse(self, response: HtmlResponse, **kwargs):
        censored_id = response.meta[CENSORED_ID_META]
        if response.status == 404 or response.status == 302:
            logging.info(FANZA_RESPONSE_STATUS_ERROR_MSG, censored_id)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", censored_id)
        self.logger.info("url: %s", response.url)
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        title = response.xpath('//h1[@id="title"]/text()').get()
        self.logger.info("Video id: %s", censored_id)
        self.logger.info("Video title: %s", title)
        try:
            # extract actress info
            actress = fanza_extract_multi_info(response, FANZA_ACTRESS_INFO)
            for actress_id, actress_name in actress.items():
                self.logger.info("Extract actress info -> actress_id: %s \t actress_name: %s", actress_id, actress_name)
            # extract director info
            director = fanza_extract_multi_info(response, FANZA_DIRECTOR_INFO)
            for director_id, director_name in actress.items():
                self.logger.info("Extract director info -> director_id: %s \t director_name: %s", director_id, director_name)
            # extract maker info
            maker_id, maker_name = fanza_extract_video_info(response, FANZA_MAKER_INFO)
            self.logger.info("Extract maker info -> maker_id: %s \t maker_name: %s", maker_id, maker_name)
            # extract label info
            label_id, label_name = fanza_extract_video_info(response, FANZA_LABEL_INFO)
            self.logger.info("Extract label info -> label_id: %s \t label_name: %s", label_id, label_name)
            # extract series info
            series_id, series_name = fanza_extract_video_info(response, FANZA_SERIES_INFO)
            self.logger.info("Extract series info -> series_id: %s \t series_name: %s", series_id, series_name)
        except ExtractException as err:
            logging.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        # extract release date and video length
        try:
            release_date = fanza_extract_meta_info(response, RELEASE_DATE_TEXT)
            if release_date is None or match(DATE_REGEX, release_date) is None:
                release_date = fanza_extract_meta_info(response, DELIVERY_DATE_TEXT)
            video_len = fanza_format_video_len(fanza_extract_meta_info(response, VIDEO_LEN_TEXT))
        except ExtractException as err:
            logging.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        except FormatException as err:
            logging.error(FORMAT_GLOBAL_ERROR_MSG, err.message, response.url)
            return
        self.logger.info("Extract video info -> release_date: %s \t video_len: %s", release_date, video_len)
        try:
            genre = fanza_extract_genre_info(response)
        except EmptyGenreException as err:
            self.logger.info("Attention please ->\n\tmsg: %s\n\turl: %s", err.message, err.url)
            genre = {}
        for genre_id, genre_name in genre.items():
            self.logger.info("Extract genre info -> genre_id: %s \t genre_name: %s", genre_id, genre_name)
        # itemloader is suitable to yield multiple items 
        yield FanzaItem(
            censored_id, title, actress, director,
            maker_id, maker_name,
            label_id, label_name,
            series_id, series_name, 
            release_date, video_len, 
            genre
        )
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        try:
            high_res_cover, low_res_cover = fanza_extract_cover_image(response, censored_id)
        except ExtractException as err:
            logging.error(EXTRACT_COVER_ERROR_MSG, err.message, err.url)
            return
        yield FanzaImageItem(high_res_cover, censored_id, censored_id + "pl", 1)
        yield FanzaImageItem(low_res_cover, censored_id, censored_id + "ps", 1)
        try:
            for url in fanza_extract_preview_image(response, censored_id):
                num_m = search(FANZA_PREVIEW_NUM_REGEX, url)
                if num_m:
                    # append 'jp' to the end of video id for hi-res preview pictures
                    preview_num = num_m.group()
                    jp = FANZA_PREVIEW_SUB_REGEX.sub(FANZA_PREVIEW_SUB_STR, url)
                    high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                    low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                    yield FanzaImageItem(jp, censored_id, high_res_preview_name)
                    yield FanzaImageItem(url, censored_id, low_res_preview_name)
        except ExtractException as err:
            logging.error(EXTRACT_PREVIEW_ERROR_MSG, err.message, err.url)
            return
        save_crawled_to_file(censored_id, self.settings['CRAWLED_FILE'])
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)

    # mgstage parse
    def parse_mgstage(self, response: HtmlResponse, **kwargs):
        censored_id = response.meta[CENSORED_ID_META]
        if response.status == 404 or response.status == 302:
            logging.error(MGS_RESPONSE_STATUS_ERROR_MSG, censored_id)
            return
        self.logger.info("------------------------------------parse %s start------------------------------------", censored_id)
        self.logger.info("url: %s", response.url)
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        try:
            self.logger.info("Video id: %s", censored_id)
            title = response.xpath('//h1[@class="tag"]/text()').get()
            title = mgs_clean_title(title)
            self.logger.info("Video title: %s", title)
            video_len = mgs_extract_meta_info(response, VIDEO_LEN_TEXT)
            video_len = mgs_format_video_len(video_len)
            release_date = mgs_extract_meta_info(response, RELEASE_DATE_TEXT)
            if release_date is None or match(DATE_REGEX, release_date) is None:
                release_date = mgs_extract_meta_info(response, DELIVERY_DATE_TEXT)
            self.logger.info("Extract video info -> release_data: %s \t video_len: %s", release_date, video_len)
            actress = mgs_extract_video_info(response, MGS_ACTRESS_INFO)
            actress = mgs_clean_text(actress)
            self.logger.info("Extract actress info -> actress: %s", actress)
            maker = mgs_extract_video_info(response, MGS_MAKER_INFO)
            maker = mgs_clean_text(maker)
            self.logger.info("Extract maker info -> maker: %s", maker)
            label = mgs_extract_video_info(response, MGS_LABEL_INFO)
            label = mgs_clean_text(label)
            self.logger.info("Extract label info -> label: %s", label)
            series = mgs_extract_video_info(response, MGS_SERIES_INFO)
            series = mgs_clean_text(series)
            self.logger.info("Extract series info -> series: %s", series)
            genre = mgs_extract_genre_info(response)
            for g in genre:
                self.logger.info("Extract genre info -> genre: %s", g)
        except FormatException as err:
            logging.error(FORMAT_GLOBAL_ERROR_MSG, err.message, response.url)
            return
        except ExtractException as err:
            logging.error(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        yield MgsItem(
            censored_id, title, 
            None, actress,
            None, maker,
            None, label,
            None, series,
            release_date, video_len,
            genre
        )
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        try:
            high_res_cover, low_res_cover = mgs_extract_cover_image(response, censored_id)
            yield FanzaImageItem(high_res_cover, censored_id, censored_id + 'pl', 1)
            yield FanzaImageItem(low_res_cover, censored_id, censored_id + 'ps', 1)
        except ExtractException as err:
            logging.error(EXTRACT_COVER_ERROR_MSG, err.message, err.url)
            return
        try:
            for url_tuple in mgs_extract_preview_image(response, censored_id):
                high_res_preview_url = url_tuple['high_res_url']
                low_res_preview_url = url_tuple['low_res_url']
                high_res_preview_num = mgs_extract_preview_num(high_res_preview_url, censored_id, 0)
                low_res_preview_num = mgs_extract_preview_num(low_res_preview_url, censored_id, 1)
                high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, high_res_preview_num)
                low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, low_res_preview_num)
                yield FanzaImageItem(high_res_preview_url, censored_id, high_res_preview_name)
                yield FanzaImageItem(low_res_preview_url, censored_id, low_res_preview_name)
        except ExtractException as err:
            logging.error(EXTRACT_PREVIEW_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)
