# This script gathers password and other stuff from the config file

import os
import database
from database import set_db_setting

# database variables
last_commented = database.last_commented
last_inbox = database.last_inbox

username = None
password = None
user_agent = None
maintainer = None
sleep_time = None
limit = None
subreddit_name = None
source_language = None
target_language = None

if not database.local_app:
    #login
    username = os.environ['REDDIT_USER'] # bot account username
    password = os.environ['REDDIT_PASSWORD'] # bot account password

    #bot
    user_agent = os.environ['REDDIT_USER_AGENT'] # UA string, see bot guidelines for reddit
    maintainer = os.environ['REDDIT_MAINTAINER'] # Maintainer username

    #settings
    sleep_time = int(os.environ['SLEEP_TIME']) # sleep time between pulls
    limit = int(os.environ['SUBMISSION_LIMIT'])  # Number of submissions per iteration
    subreddit_name = os.environ['SUBREDDIT_NAME']
    source_language = os.environ['SOURCE_LANGUAGE']
    target_language = os.environ['TARGET_LANGUAGE']

else:
    import configparser

    FILENAME = 'local.cfg'

    config = configparser.ConfigParser()
    config.read(FILENAME)

    username = config.get('settings', 'username')
    password = config.get('settings', 'password')

    user_agent = config.get('settings', 'user_agent')
    maintainer = config.get('settings', 'maintainer')

    sleep_time = config.getint('settings', 'sleep_time')
    limit = config.getint('settings', 'limit')
    subreddit_name = config.get('settings', 'subreddit_name')
    source_language = config.get('settings', 'source_language')
    target_language = config.get('settings', 'target_language')
