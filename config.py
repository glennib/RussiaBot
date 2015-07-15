# This script gathers password and other stuff from the config file

import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

username = config.get('Login', 'Username')
password = config.get('Login', 'Password')

user_agent = config.get('Bot', 'UserAgent')

limit = config.getint('Settings', 'Limit')  # Number of submissions per iteration
subreddit_name = config.get('Settings', 'Subreddit')

