from scrapy import Spider, Request
from scrapy.http.response.html import HtmlResponse
from re import search, match
from fanza.fanza_exception import ExtractException, EmptyGenreException, FormatException
from fanza.items import FanzaAmateurItem, FanzaItem, MgsItem, MovieImageItem, RequestStatusItem
from fanza.movie_constants import *
from fanza.movie_extract_helper import *
from fanza.error_msg_constants import *
from fanza.url_factroy import fanza_url_factory, mgs_url_factory, fanza_amateur_url_factory
from fanza.common import get_crawled

class VideoDetailSpider(Spider):
    name = 'video_detail'
    allowed_domains = ['dmm.co.jp', 'mgstage.com']
        
    def produce_fanza(self, censored_id: str, url: str):
        self.logger.debug('Formatted url: %s', url)
        return Request(
            url, cookies={FANZA_AGE_COOKIE: FANZA_AGE_COOKIE_VAL},
            meta={CENSORED_ID_META: censored_id},
            callback=self.parse
        )

    def produce_mgstage(self, censored_id: str, url: str):
        self.logger.debug('Formatted url: %s', url)
        return Request(
            url, cookies={MGS_AGE_COOKIE: MGS_AGE_COOKIE_VAL},
            callback=self.parse_mgstage,
            meta={CENSORED_ID_META: censored_id}
        )

    def produce_fanza_amateur(self, censored_id: str, url: str):
        self.logger.debug('Formatted url: %s', url)
        return Request(
            url, cookies={FANZA_AGE_COOKIE: FANZA_AGE_COOKIE_VAL},
            meta={CENSORED_ID_META: censored_id},
            callback=self.parse_fanza_amateur
        )

    def start_requests(self):
        video_dir = self.settings['VIDEO_DIR']
        ext_white_list = self.settings['EXT_WHITE_LIST']
        crawled = get_crawled(self.settings['CRAWLED_FILE'])
        for censored_id in scan_video_dir(video_dir, ext_white_list):
            id_m = search(CENSORED_ID_REGEX, censored_id)
            if id_m is None:
                self.logger.info('%s is filtered!', censored_id)
                continue
            censored_id = id_m.group()
            if censored_id in crawled:
                self.logger.debug('%s is already crawled' % censored_id)
                continue
            for url in fanza_url_factory.get_url(censored_id):
                yield self.produce_fanza(censored_id, url)
            for url in mgs_url_factory.get_url(censored_id):
                yield self.produce_mgstage(censored_id, url)
            for url in fanza_amateur_url_factory.get_url(censored_id):
                yield self.produce_fanza_amateur(censored_id, url)
                                

    # fanza parse
    def parse(self, response: HtmlResponse, **kwargs):
        censored_id = response.meta[CENSORED_ID_META]
        if response.status == 404 or response.status == 302 or response.status == 301:
            self.logger.debug(FANZA_RESPONSE_STATUS_ERROR_MSG, censored_id)
            yield RequestStatusItem(censored_id, FANZA_BAD_REQUEST_FLAG)
            return
        yield RequestStatusItem(censored_id, SUCCESS_REQUEST_FLAG)
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
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        # extract release date and video length
        try:
            release_date = fanza_extract_meta_info(response, RELEASE_DATE_TEXT)
            if release_date is None or match(DATE_REGEX, release_date) is None:
                release_date = fanza_extract_meta_info(response, DELIVERY_DATE_TEXT)
            video_len = fanza_format_video_len(fanza_extract_meta_info(response, VIDEO_LEN_TEXT))
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        except FormatException as err:
            self.logger.exception(FORMAT_GLOBAL_ERROR_MSG, err.message, response.url)
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
            censoredId=censored_id, title=title, actress=actress, director=director,
            makerId=maker_id, makerName=maker_name,
            labelId=label_id, labelName=label_name,
            seriesId=series_id, seriesName=series_name, 
            releaseDate=release_date, videoLen=video_len, 
            genre=genre
        )
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        try:
            low_res_cover, high_res_cover = fanza_extract_cover_image(response, censored_id)
        except ExtractException as err:
            self.logger.exception(EXTRACT_COVER_ERROR_MSG, err.message, err.url)
            return
        yield MovieImageItem(url=high_res_cover, subDir=censored_id, imageName=censored_id + "pl", isCover=1)
        yield MovieImageItem(url=low_res_cover, subDir=censored_id, imageName=censored_id + "ps", isCover=1)
        try:
            for url in fanza_extract_preview_image(response, censored_id):
                num_m = search(FANZA_PREVIEW_NUM_REGEX, url)
                if num_m:
                    # append 'jp' to the end of video id for hi-res preview pictures
                    preview_num = num_m.group()
                    jp = FANZA_PREVIEW_SUB_REGEX.sub(FANZA_PREVIEW_SUB_STR, url)
                    high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                    low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                    yield MovieImageItem(url=jp, subDir=censored_id, imageName=high_res_preview_name)
                    yield MovieImageItem(url=url, subDir=censored_id, imageName=low_res_preview_name)
        except ExtractException as err:
            self.logger.exception(EXTRACT_PREVIEW_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)

    # mgstage parse
    def parse_mgstage(self, response: HtmlResponse, **kwargs):
        censored_id = response.meta[CENSORED_ID_META]
        if response.status == 404 or response.status == 302 or response.status == 301:
            self.logger.debug(MGS_RESPONSE_STATUS_ERROR_MSG, censored_id)
            yield RequestStatusItem(censored_id, MGS_BAD_REQUEST_FLAG)
            return
        yield RequestStatusItem(censored_id, SUCCESS_REQUEST_FLAG)
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
            actress = mgs_extract_actress_info(response)
            for a in actress:
                self.logger.info("Extract actress info -> actress: %s", a)
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
            self.logger.exception(FORMAT_GLOBAL_ERROR_MSG, err.message, response.url)
            return
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        yield MgsItem(
            censoredId=censored_id, title=title, actress=actress,
            makerName=maker,
            labelName=label,
            seriesName=series,
            releaseDate=release_date, videoLen=video_len,
            genre=genre
        )
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        try:
            high_res_cover, low_res_cover = mgs_extract_cover_image(response, censored_id)
            yield MovieImageItem(url=high_res_cover, subDir=censored_id, imageName=censored_id + 'pl', isCover=1)
            yield MovieImageItem(url=low_res_cover, subDir=censored_id, imageName=censored_id + 'ps', isCover=1)
        except ExtractException as err:
            self.logger.exception(EXTRACT_COVER_ERROR_MSG, err.message, err.url)
            return
        try:
            for url_tuple in mgs_extract_preview_image(response, censored_id):
                high_res_preview_url = url_tuple[MSG_HIGH_RES_IMG_URL_KEY]
                low_res_preview_url = url_tuple[MGS_LOW_RES_IMG_URL_KEY]
                high_res_preview_num = mgs_extract_preview_num(high_res_preview_url, censored_id, 0)
                low_res_preview_num = mgs_extract_preview_num(low_res_preview_url, censored_id, 1)
                high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, high_res_preview_num)
                low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, low_res_preview_num)
                yield MovieImageItem(url=high_res_preview_url, subDir=censored_id, imageName=high_res_preview_name)
                yield MovieImageItem(url=low_res_preview_url, subDir=censored_id, imageName=low_res_preview_name)
        except ExtractException as err:
            self.logger.exception(EXTRACT_PREVIEW_ERROR_MSG, err.message, err.url)
            return
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)

    def parse_fanza_amateur(self, response: HtmlResponse, **kwargs):
        censored_id = response.meta[CENSORED_ID_META]
        if response.status == 404 or response.status == 302 or response.status == 301:
            self.logger.debug(FANZA_AMATEUR_RESPONSE_STATUS_ERROR_MSG, censored_id)
            yield RequestStatusItem(censored_id, FANZA_AMATEUR_BAD_REQUEST_FLAG)
            return
        yield RequestStatusItem(censored_id, SUCCESS_REQUEST_FLAG)
        self.logger.info("------------------------------------parse %s start------------------------------------", censored_id)
        self.logger.info("url: %s", response.url)
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        title = response.xpath('//h1[@id="title"]/text()').get()
        self.logger.info("Video id: %s", censored_id)
        self.logger.info("Video title: %s", title)
        try:
            delivery_date = fanza_extract_meta_info(response, DELIVERY_DATE_TEXT)
            video_len = fanza_format_video_len(fanza_extract_meta_info(response, VIDEO_LEN_TEXT))
            amateur = fanza_extract_meta_info(response, AMATEUR_NAME_TEXT)
            three_size = fanza_extract_meta_info(response, AMATEUR_THREE_SIZE_TEXT)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        except FormatException as err:
            self.logger.exception(FORMAT_GLOBAL_ERROR_MSG, err.message, response.url)
            return
        self.logger.info("Extract video info -> delivery_date: %s \t video_len: %s", delivery_date, video_len)
        self.logger.info("Extract video info -> amateur: %s \t three_size: %s", amateur, three_size)
        try:
            # extract label info
            label_id, label_name = fanza_extract_video_info(response, FANZA_LABEL_INFO)
            self.logger.info("Extract label info -> label_id: %s \t label_name: %s", label_id, label_name)
        except ExtractException as err:
            self.logger.exception(EXTRACT_GLOBAL_ERROR_MSG, err.message, err.url)
            return
        try:
            genre = fanza_extract_genre_info(response)
        except EmptyGenreException as err:
            self.logger.info("Attention please ->\n\tmsg: %s\n\turl: %s", err.message, err.url)
            genre = {}
        for genre_id, genre_name in genre.items():
            self.logger.info("Extract genre info -> genre_id: %s \t genre_name: %s", genre_id, genre_name)
        yield FanzaAmateurItem(
            censoredId=censored_id,
            title=title,
            amateur=amateur,
            threeSize=three_size,
            labelId=label_id,
            labelName=label_name,
            deliveryDate=delivery_date,
            videoLen=video_len,
            genre=genre
        )
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        try:
            cover = fanza_amateur_extract_cover_image(response, censored_id)
        except ExtractException as err:
            self.logger.exception(EXTRACT_COVER_ERROR_MSG, err.message, err.url)
            return
        yield MovieImageItem(url=cover, subDir=censored_id, imageName=censored_id + 'pl', isCover=1)
        try:
            for url in fanza_extract_preview_image(response, censored_id):
                num_m = search(FANZA_AMATEUR_PREVIEW_NUM_REGEX, url)
                if num_m:
                    preview_num = num_m.group()
                    jp = FANZA_AMATEUR_PREVIEW_SUB_REGEX.sub(FANZA_AMATEUR_PREVIEW_SUB_STR, url)
                    high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                    low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                    yield MovieImageItem(url=jp, subDir=censored_id, imageName=high_res_preview_name)
                    yield MovieImageItem(url=url, subDir=censored_id, imageName=low_res_preview_name)
        except ExtractException as err:
            self.logger.exception(EXTRACT_PREVIEW_ERROR_MSG, err.message, err.url)
            return
