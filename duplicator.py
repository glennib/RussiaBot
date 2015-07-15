# The point of this script is to duplicate the posts of /r/russia to /r/RussiaBot for testing purposes.

from pprint import pprint
import config
import praw

r = praw.Reddit(user_agent=config.user_agent)
r.login(config.username, config.password)

sourceSub = r.get_subreddit('russia')
targetSub = r.get_subreddit('RussiaBot')

alreadyPosted = []

for submission in targetSub.get_new(limit = 10):
    if submission.is_self:
        alreadyPosted.append(submission.title)
    else:
        alreadyPosted.append(submission.url)


for submission in sourceSub.get_new(limit=10):
    #pprint(vars(submission))
    if submission.is_self and submission.title not in alreadyPosted:
        r.submit('RussiaBot', submission.title, text=submission.selftext)
        print('Posted a self text post')
    elif submission.url not in alreadyPosted:
        r.submit('RussiaBot', submission.title, url=submission.url)
        print('Posted a link')

