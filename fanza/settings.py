# Scrapy settings for fanza project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fanza'

SPLASH_URL = 'http://127.0.0.1:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

SPIDER_MODULES = ['fanza.spiders']
NEWSPIDER_MODULE = 'fanza.spiders'
MOVIE_IMG_BASE_FOLDER = r'fanza/img/movie'
ACTRESS_IMG_BASE_FOLDER = r'fanza/img/actress'
LOG_LEVEL = 'INFO'
LOG_FILE = 'logfile.log'
FAIL_FILE = r'resources/failed.txt'
IMAGE_FAIL_FILE = 'img-failed.txt'
MOVIE_DIR = r'L:/Finished'
CRAWLED_FILE = r'resources/crawled.txt'
EXT_WHITE_LIST = ['.mp4', '.mkv']
HTTPERROR_ALLOWED_CODES = [404, 302, 301]
# REDIRECT_MAX_TIMES = 1
IMAGE_DOWNLOAD_PROXY = '127.0.0.1:8181'
DOWNLOAD_TIMEOUT = 60
# sod needs to utilize redirect middleware, so this setting is commented
# mgstage request add `dont_redirect` meta
# REDIRECT_ENABLED = False
RETRY_LIMIT = 3
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0
DOWNLOAD_DELAY = 0.25

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'fanza (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    'fanza.middlewares.GlobalExceptionHandleSpiderMiddleware': 352,
    # 'fanza.middlewares.FanzaSpiderMiddleware': 542,
}

# Customized contracts
SPIDER_CONTRACTS = {
    'fanza.contracts.CookiesContract': 10,
    'fanza.contracts.SplashEndpointContract': 13,
    'fanza.contracts.MetaContract': 14,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'fanza.middlewares.ProxyMiddleware': 351,
    # 'fanza.middlewares.FanzaDownloaderMiddleware': 543,
    'fanza.middlewares.SodDownloaderMiddleware': 544,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'fanza.pipelines.FanzaPipeline': 300,
    # 'fanza.pipelines.FanzaImagePipeline': 301,
    # 'fanza.pipelines.AvbookImagePipeline': 302,
    # 'fanza.pipelines.SuccessResponsePipeline': 303,
    # 'fanza.pipelines.RequestStatusPipline': 303,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = False
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
