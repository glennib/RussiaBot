# This script gathers password and other stuff from the config file

import configparser

FILENAME = 'config.cfg'

config = configparser.ConfigParser()
config.read(FILENAME)

#login
username = config.get('Login', 'Username')
password = config.get('Login', 'Password')

#bot
user_agent = config.get('Bot', 'UserAgent')
last_commented = config.getfloat('Bot', 'LastCommented')

#settings
sleep_time = config.getint('Settings', 'SleepTime')
limit = config.getint('Settings', 'Limit')  # Number of submissions per iteration
subreddit_name = config.get('Settings', 'Subreddit')
source_language = config.get('Settings', 'SourceLanguage')
target_language = config.get('Settings', 'TargetLanguage')

def set_last_commented(last):
    last_string = '%.1f' % last
    config.set('Bot', 'LastCommented', last_string)
    with open(FILENAME, 'w') as configfile:
        config.write(configfile)
    global last_commented
    last_commented = last
