# -*- coding: utf-8 -*-

# Scrapy settings for tm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tm'

SPIDER_MODULES = ['tm.spiders']
NEWSPIDER_MODULE = 'tm.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tm (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tm.middlewares.TmSpiderMiddleware': 543,
#}

HTTPERROR_ALLOWED_CODES = [500]

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'tm.pipelines.ValidateItemPipeline': 700,
   'tm.pipelines.MongoDBPipeline': 800
}

DUPEFILTER_DEBUG = True

LOG_LEVEL = "WARNING"
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

POINT_RULES = ['2p', '3p']

COMPETITION_DATA = {
    'BL1': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'AWAY_GOALS_H2H',
            'AWAY_GOALS',
        ],
    },
    'BL2': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'AWAY_GOALS_H2H',
            'AWAY_GOALS',
        ],
    },
    'BL3': {
        'point_rules': [
            {
                'season_from': 2008,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'AWAY_GOALS_H2H',
            'AWAY_GOALS',
        ],
    },
    'PL': {
        'point_rules': [
            {
                'season_from': 1992,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'ELC': {
        'point_rules': [
            {
                'season_from': 2004,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'EL1': {
        'point_rules': [
            {
                'season_from': 2004,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'SA': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'SB': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'FL1': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'FL2': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'PD': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOALS_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'SD': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOALS_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
}
