# This script gathers password and other stuff from the config file

import os
import database
from database import set_db_setting

# database variables
last_commented = database.last_commented
last_inbox = database.last_inbox

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

