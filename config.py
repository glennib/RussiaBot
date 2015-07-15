# This script gathers password and other stuff from the config file

import configparser

FILENAME = 'config.cfg'

config = configparser.ConfigParser()
config.read(FILENAME)

username = config.get('Login', 'Username')
password = config.get('Login', 'Password')

user_agent = config.get('Bot', 'UserAgent')
last_commented = config.getfloat('Bot', 'LastCommented')

sleep_time = config.getint('Settings', 'SleepTime')
limit = config.getint('Settings', 'Limit')  # Number of submissions per iteration
subreddit_name = config.get('Settings', 'Subreddit')

def set_last_commented(last):
    last_string = '%.1f' % last
    config.set('Bot', 'LastCommented', last_string)
    with open(FILENAME, 'w') as configfile:
        config.write(configfile)
    global last_commented
    last_commented = last
