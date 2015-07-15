import time
import praw
import goslate
import config

# Initialize Reddit Praw
r = praw.Reddit(user_agent=config.user_agent)
r.login(config.username, config.password)

# Initialize translator
gs = goslate.Goslate()

already_done = []  # list of things that are done

# Main program / loop

subreddit = r.get_subreddit(config.subreddit_name)

while True:
    print('Gathering new submissions.')
    last_commented = config.last_commented

    # Turning the list upside down:
    upside_down = []

    for submission in subreddit.get_new(limit=config.limit):
        upside_down.append(submission)

    upside_down.reverse()

    for submission in upside_down:
        if submission.id not in already_done and submission.created_utc > config.last_commented:
            print('New submission found.')
            language = gs.detect(submission.title)
            if language == 'ru':
                print('Russian language detected. Adding comment...')
                submission.add_comment(gs.translate(submission.title, 'en'))
                print('Comment added.')
            else:
                print('Language other than russian detected.')
            print('Adding element to already-done-list.')
            already_done.append(submission.id)
            last_commented = submission.created_utc
    config.set_last_commented(last_commented)
    print('Done with all submissions. Going to sleep.')
    time.sleep(config.sleep_time)
