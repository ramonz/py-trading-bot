### Setting of the trading bot ###
import os

_settings={
## IB configuration
"IB_LOCALHOST":'127.0.0.1',
"IB_PORT": os.environ.get("IB_PORT",7496), #IB Gateway 4001, TWS 7496

## Preselection to be used for the different stock exchanges ##
# possible values out-of-the-box:
# "retard","macd_vol","divergence", "wq7","wq31","wq53","wq54", "realmadrid"

"ETF_IB_auth":False,   

"17h_stock_exchanges":["Paris","XETRA","EUREX"], #exchange to scan at 17h  
"22h_stock_exchanges":["Nasdaq","NYSE"], #exchange to scan at 22h   
"NYSE_SECTOR_TO_SCAN":["it", "fin"],  ##"realestate","industry","it","com","staples","consumer","utilities","energy",\ 
          #"fin","materials","healthcare"
          
          
## Configuration of Telegram ##
"PF_CHECK":True,
"INDEX_CHECK":True,
"REPORT_17h":True, #for Paris and XETRA
"REPORT_22h":True, #for Nasdaq and Nyse
"HEARTBEAT":False, # to test telegram
"HEARTBEAT_IB":False, # to test telegram
"UPDATE_SLOW_STRAT":True, 

"ALERT_THRESHOLD":3, #in %
"ALARM_THRESHOLD":5, #in %
"ALERT_HYST":1, #margin to avoid alert/recovery at high frequency

"TIME_INTERVAL_CHECK":10, #in minutes, interval between two checks of pf values

## Order settings ##
"USED API_FOR_DATA":{
    "alerting":os.environ.get("USED API_FOR_DATA_ALERTING","IB"), #"IB" or "YF"
    "reporting":os.environ.get("USED API_FOR_DATA_REPORTING","YF"), #"IB" or "YF"
    },
    
"IB_STOCK_NO_PERMISSION":["^NDX","^DJI","^IXIC"],

"PERFORM_ORDER":True, #test or use IB to perform orders
"BYPASS_ORDERCAPITAL_IF_IB":False, #bypass the restriction linked to order capital if using IB. with other words, 
#if there is enough money on your account, the order will be performed, 
#without considering how many orders/strategy you want to perform
"ORDER_SIZE":15000, 
## Configuration of the strategies ##
"DIVERGENCE_MACRO":False, #if set to true divergence_blocked will used, otherwise divergence, when the key word divergence is selected
"RETARD_MACRO":True, #if set to true retard_macro will used, otherwise retard, when the key word retard is selected

"STRATEGY_NORMAL_STOCKS":"StratG",
"STRATEGY_NORMAL_INDEX":"StratIndexB",
"STRATEGY_RETARD_KEEP":"StratG",

# Frequency is the number of days between successive candidates actualisation
"DAILY_REPORT_PERIOD":3, #in year

"VOL_MAX_CANDIDATES_NB":1,
"MACD_VOL_MAX_CANDIDATES_NB":1,
"HIST_VOL_MAX_CANDIDATES_NB":1,
"DIVERGENCE_THRESHOLD":0.005,
"VOL_SLOW_FREQUENCY":10,
"VOL_SLOW_MAX_CANDIDATES_NB":2,
"MACD_VOL_SLOW_FREQUENCY":10,
"MACD_VOL_SLOW_MAX_CANDIDATES_NB":2,
"HIST_VOL_SLOW_FREQUENCY":10,
"HIST_VOL_SLOW_MAX_CANDIDATES_NB":2,
"REALMADRID_DISTANCE":400,
"REALMADRID_FREQUENCY":30,
"REALMADRID_MAX_CANDIDATES_NB":2, 
"RETARD_MAX_HOLD_DURATION":15,

"STOCH_LL":20,
"STOCH_LU":80,
"BBAND_THRESHOLD":0.15,

"CALCULATE_PATTERN":True, #pattern calculation is time consuming
"CALCULATE_TREND":True,   #trend calculation is time consuming

#for some major events, that cannot be detected only with technical analysis
"FORCE_MACRO_TO":"" #"bull"/"uncertain"/""
}

"""
Django settings for trading_bot project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

### Configuration Django
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG',True)

if DEBUG and DEBUG!="False":
    with open(os.path.join(BASE_DIR, 'trading_bot/etc/DJANGO_SECRET')) as f:
        SECRET_KEY = f.read().strip()
    with open(os.path.join(BASE_DIR, 'trading_bot/etc/DB_SECRET')) as f:
        DB_SECRET_KEY = f.read().strip()
    with open(os.path.join(BASE_DIR, 'trading_bot/etc/DB_USER')) as f:
        DB_USER = f.read().strip()
else:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    DB_SECRET_KEY = os.environ.get('POSTGRES_PASSWORD') 
    DB_USER=os.environ.get('POSTGRES_USER') 
   

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reporting.apps.ReportingConfig',
    'orders.apps.OrdersConfig',
    'django_filters'
    
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trading_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'trading_bot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  os.getenv('POSTGRES_DB','pgtradingbotdb'),
        'USER': DB_USER,
        'PASSWORD': DB_SECRET_KEY,
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '')
    }
}  

REDIS_PASSWORD=""
REDIS_PORT="6379"
REDIS_DB=0

REDIS_URL = ':%s@%s:%s/%d' % (
        REDIS_PASSWORD,
        os.getenv("REDIS_HOST","localhost"),
        REDIS_PORT,
        REDIS_DB)

CELERY_BROKER_URL = 'redis://'+REDIS_URL 

# CELERY
if not DEBUG:
    CELERY_BROKER_POOL_LIMIT= 1
    CELERY_BROKER_HEARTBEAT = None # We're using TCP keep-alive instead
    CELERY_BROKER_CONNECTION_TIMEOUT = 120 # May require a long timeout due to Linux DNS timeouts etc
    CELERY_RESULT_BACKEND = None 
    CELERY_WORKER_PREFETCH_MULTIPLIER = 1
#CELERY_RESULT_BACKEND = 'pyamqp://guest@localhost//'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    URL_ROOT= 'http://localhost:8000' 
else:
    URL_ROOT='https://tradingbot.herokuapp.com'

#?Celery
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(lineno)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'trade_format': {
            'format': '[%(asctime)s]  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    
    'handlers': {
        'info_file': {
            'level': 'INFO',# INFO
            'class': 'logging.FileHandler',
            'filename': 'logs/info.log',
             'formatter': 'default',
             },
       'warning_file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': 'logs/warning_and_error.log',
                 'formatter': 'default',
            },
       'trade_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': 'logs/trade.log',
                 'formatter': 'trade_format',
            },       
    },
    'loggers': {
        '': {
            'handlers': ['info_file', 'warning_file'],
            'level': 'INFO',
            'propagate': True,
        },
       'trade': {
           'handlers': ['trade_file'],
           'level': 'INFO',
           'propagate': True,
       }, 
    },
}
