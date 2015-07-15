import time
import praw
import goslate
import configparser

# Configurations
config = configparser.ConfigParser()
config.read('config.cfg')

username = config.get('Login', 'Username')
password = config.get('Login', 'Password')

user_agent = config.get('Bot', 'UserAgent')

limit = config.getint('Settings', 'Limit')  # Number of submissions per iteration

# Initialize Reddit Praw
r = praw.Reddit(user_agent=user_agent)
r.login(username, password)

# Initialize translator
gs = goslate.Goslate()

already_done = []  # list of things that are done

# Debug
print(username)
print(password)
print(user_agent)
print(limit)
print(already_done)

# Main loop
while True:
    # time.sleep(120)
    subreddit = r.get_subreddit('russia')
    for submission in subreddit.get_new(limit=limit):
        if submission.id not in already_done:
            language = gs.detect(submission.title)
            already_done.append(submission.id)
            if language == 'ru':
                submission.add_comment(gs.translate(submission.title, 'en'))
    time.sleep(120)
