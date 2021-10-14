from fanza.items import FanzaAmateurItem, FanzaItem, MgsItem, MovieImageItem, RequestStatusItem
from fanza.movie.movie_constants import *
from fanza.movie.movie_extract_helper import *
from fanza.movie.factory.url_factroy import fanza_url_factory, mgs_url_factory, fanza_amateur_url_factory, fanza_url_blank_replacement_factory
from fanza.exceptions.error_msg_constants import *
from fanza.exceptions.fanza_exception import ExtractException, EmptyGenreException, FormatException
from fanza.common import get_crawled

from scrapy import Spider, Request
from scrapy.http.response.html import HtmlResponse

from re import search, match

class VideoDetailSpider(Spider):
    name = 'video_detail'
    allowed_domains = ['dmm.co.jp', 'mgstage.com']
        
    def produce_fanza(self, censored_id: str, url: str):
        self.logger.debug('Formatted url: %s', url)
        return Request(
            url, cookies={FANZA_AGE_COOKIE: FANZA_AGE_COOKIE_VAL},
            cb_kwargs=dict(censored_id=censored_id),
            callback=self.parse
        )

    def produce_mgstage(self, censored_id: str, url: str):
        self.logger.debug('Formatted url: %s', url)
        return Request(
            url, cookies={MGS_AGE_COOKIE: MGS_AGE_COOKIE_VAL},
            callback=self.parse_mgstage,
            cb_kwargs=dict(censored_id=censored_id)
        )

    def produce_fanza_amateur(self, censored_id: str, url: str):
        self.logger.debug('Formatted url: %s', url)
        return Request(
            url, cookies={FANZA_AGE_COOKIE: FANZA_AGE_COOKIE_VAL},
            callback=self.parse_fanza_amateur,
            cb_kwargs=dict(censored_id=censored_id)
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
            for url in fanza_url_blank_replacement_factory.get_url(censored_id):
                yield self.produce_fanza(censored_id, url)
                                

    # fanza parse
    def parse(self, response: HtmlResponse, censored_id):
        """ This function parse fanza movie page.

        @url https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=cawd00186/
        @cb_kwargs {"censored_id": "CAWD-186"}
        @cookies {"age_check_done": "1"}
        @avbookreturns movieItem 1 imageItem 22 requestStatusItem 1
        @avbookscrapes movieItem {"title": "パーフェクトボディを視姦する超接写コケティッシュ肉感アングル 伊藤舞雪", "censoredId": "CAWD-186", "videoLen": 154}
        """
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
        actress = fanza_extract_multi_info(response, FANZA_ACTRESS_INFO)
        director = fanza_extract_multi_info(response, FANZA_DIRECTOR_INFO)
        maker_id, maker_name = fanza_extract_video_info(response, FANZA_MAKER_INFO)
        label_id, label_name = fanza_extract_video_info(response, FANZA_LABEL_INFO)
        series_id, series_name = fanza_extract_video_info(response, FANZA_SERIES_INFO)
        release_date = fanza_extract_meta_info(response, RELEASE_DATE_TEXT)
        genre = fanza_extract_multi_info(response, FANZA_GENRE_INFO)
        if match(DATE_REGEX, release_date) is None:
            release_date = fanza_extract_meta_info(response, DELIVERY_DATE_TEXT)
        video_len = fanza_format_video_len(fanza_extract_meta_info(response, VIDEO_LEN_TEXT))
        for actress_id, actress_name in actress.items():
            self.logger.info("Extract actress info -> actress_id: %s \t actress_name: %s", actress_id, actress_name)
        for director_id, director_name in actress.items():
            self.logger.info("Extract director info -> director_id: %s \t director_name: %s", director_id, director_name)
        self.logger.info("Extract maker info -> maker_id: %s \t maker_name: %s", maker_id, maker_name)
        self.logger.info("Extract label info -> label_id: %s \t label_name: %s", label_id, label_name)
        self.logger.info("Extract series info -> series_id: %s \t series_name: %s", series_id, series_name)
        self.logger.info("Extract video info -> release_date: %s \t video_len: %s", release_date, video_len)
        for genre_id, genre_name in genre.items():
            self.logger.info("Extract genre info -> genre_id: %s \t genre_name: %s", genre_id, genre_name)
        yield FanzaItem(
            censoredId=censored_id, title=title, actress=actress, director=director,
            makerId=maker_id, makerName=maker_name,
            labelId=label_id, labelName=label_name,
            seriesId=series_id, seriesName=series_name, 
            releaseDate=release_date, videoLen=video_len, 
            genre=genre
        )
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        low_res_cover, high_res_cover = fanza_extract_cover_image(response, censored_id)
        yield MovieImageItem(url=high_res_cover, subDir=censored_id, imageName=censored_id + "pl", isCover=1)
        yield MovieImageItem(url=low_res_cover, subDir=censored_id, imageName=censored_id + "ps", isCover=1)
        for url in fanza_extract_preview_image(response, censored_id):
            num_m = search(FANZA_PREVIEW_NUM_REGEX, url)
            if num_m:
                preview_num = num_m.group()
                jp = FANZA_PREVIEW_SUB_REGEX.sub(FANZA_PREVIEW_SUB_STR, url)
                high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                yield MovieImageItem(url=jp, subDir=censored_id, imageName=high_res_preview_name)
                yield MovieImageItem(url=url, subDir=censored_id, imageName=low_res_preview_name)
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)

    # mgstage parse
    def parse_mgstage(self, response: HtmlResponse, censored_id):
        """ This function parse mgstage movie page.

        @url https://www.mgstage.com/product/product_detail/ABW-013/
        @cb_kwargs {"censored_id": "ABW-013"}
        @cookies {"adc": "1"}
        @avbookreturns movieItem 1 imageItem 26 requestStatusItem 1
        @avbookscrapes movieItem {"title": "声が出せない状況で…こっそり いちゃラブ「密着」SEX vol.02 かつてない閉所でイキまくる3本番密着性交 鈴村あいり 【MGSだけのおまけ映像付き+10分】", "censoredId": "ABW-013", "videoLen": 190}
        """
        if response.status == 404 or response.status == 302 or response.status == 301:
            self.logger.debug(MGS_RESPONSE_STATUS_ERROR_MSG, censored_id)
            yield RequestStatusItem(censored_id, MGS_BAD_REQUEST_FLAG)
            return
        yield RequestStatusItem(censored_id, SUCCESS_REQUEST_FLAG)
        self.logger.info("------------------------------------parse %s start------------------------------------", censored_id)
        self.logger.info("url: %s", response.url)
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        self.logger.info("Video id: %s", censored_id)
        title = msg_extract_title(response)
        release_date = mgs_extract_meta_info(response, RELEASE_DATE_TEXT)
        if release_date is None or match(DATE_REGEX, release_date) is None:
            release_date = mgs_extract_meta_info(response, DELIVERY_DATE_TEXT)
        actress = msg_extract_multi_info(response, MGS_ACTRESS_INFO)
        maker = mgs_extract_video_info(response, MGS_MAKER_INFO)
        label = mgs_extract_video_info(response, MGS_LABEL_INFO)
        genre = msg_extract_multi_info(response, MGS_GENRE_INFO)
        video_len = msg_extract_video_len(response)

        self.logger.info("Video title: %s", title)
        self.logger.info("Extract video info -> release_data: %s \t video_len: %s", release_date, video_len)
        for a in actress:
            self.logger.info("Extract actress info -> actress: %s", a)
        self.logger.info("Extract maker info -> maker: %s", maker)
        self.logger.info("Extract label info -> label: %s", label)
        series = mgs_extract_video_info(response, MGS_SERIES_INFO)
        self.logger.info("Extract series info -> series: %s", series)
        for g in genre:
            self.logger.info("Extract genre info -> genre: %s", g)
        yield MgsItem(
            censoredId=censored_id, title=title, actress=actress,
            makerName=maker,
            labelName=label,
            seriesName=series,
            releaseDate=release_date, videoLen=video_len,
            genre=genre
        )
        self.logger.info('<<<<<<<<<<<<<<<<<<<<<<<<<extract %s video information finish!>>>>>>>>>>>>>>>>>>>>>>>>>', censored_id)
        high_res_cover, low_res_cover = mgs_extract_cover_image(response, censored_id)
        yield MovieImageItem(url=high_res_cover, subDir=censored_id, imageName=censored_id + 'pl', isCover=1)
        yield MovieImageItem(url=low_res_cover, subDir=censored_id, imageName=censored_id + 'ps', isCover=1)
        for url_tuple in mgs_extract_preview_image(response):
            high_res_preview_url = url_tuple[MSG_HIGH_RES_IMG_URL_KEY]
            low_res_preview_url = url_tuple[MGS_LOW_RES_IMG_URL_KEY]
            high_res_preview_num = mgs_extract_preview_num(high_res_preview_url, 0)
            low_res_preview_num = mgs_extract_preview_num(low_res_preview_url, 1)
            high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, high_res_preview_num)
            low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, low_res_preview_num)
            yield MovieImageItem(url=high_res_preview_url, subDir=censored_id, imageName=high_res_preview_name)
            yield MovieImageItem(url=low_res_preview_url, subDir=censored_id, imageName=low_res_preview_name)
        self.logger.info('------------------------------------parse %s success------------------------------------', censored_id)

    def parse_fanza_amateur(self, response: HtmlResponse, censored_id):
        """ This function parse fanza amateur movie page.

        @url https://www.dmm.co.jp/digital/videoc/-/detail/=/cid=yaho012/
        @cb_kwargs {"censored_id": "YAHO-012"}
        @cookies {"age_check_done": "1"}
        @avbookreturns movieItem 1 imageItem 11 requestStatusItem 1
        @avbookscrapes movieItem {"title": "みゆきち", "censoredId": "YAHO-012", "videoLen": 120}
        """
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
        delivery_date = fanza_extract_meta_info(response, DELIVERY_DATE_TEXT)
        video_len = fanza_format_video_len(fanza_extract_meta_info(response, VIDEO_LEN_TEXT))
        amateur = fanza_extract_meta_info(response, AMATEUR_NAME_TEXT)
        three_size = fanza_extract_meta_info(response, AMATEUR_THREE_SIZE_TEXT)
        label_id, label_name = fanza_extract_video_info(response, FANZA_LABEL_INFO)
        genre = fanza_extract_multi_info(response, FANZA_GENRE_INFO)
        self.logger.info("Extract video info -> delivery_date: %s \t video_len: %s", delivery_date, video_len)
        self.logger.info("Extract video info -> amateur: %s \t three_size: %s", amateur, three_size)
        self.logger.info("Extract label info -> label_id: %s \t label_name: %s", label_id, label_name)
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
        cover = fanza_amateur_extract_cover_image(response, censored_id)
        yield MovieImageItem(url=cover, subDir=censored_id, imageName=censored_id + 'pl', isCover=1)
        for url in fanza_extract_preview_image(response, censored_id):
            num_m = search(FANZA_AMATEUR_PREVIEW_NUM_REGEX, url)
            if num_m:
                preview_num = num_m.group()
                jp = FANZA_AMATEUR_PREVIEW_SUB_REGEX.sub(FANZA_AMATEUR_PREVIEW_SUB_STR, url)
                high_res_preview_name = HIGH_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                low_res_preview_name = LOW_PREVIEW_IMAGE_FORMATTER.format(censored_id, preview_num)
                yield MovieImageItem(url=jp, subDir=censored_id, imageName=high_res_preview_name)
                yield MovieImageItem(url=url, subDir=censored_id, imageName=low_res_preview_name)
