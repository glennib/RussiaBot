import time
import praw
import goslate
import config

# defining functions:


def translated_title(submission):
    return gs.translate(submission.title, config.target_language)


def clear_comment():
    global current_comment
    current_comment = ''


def append_title(submission):
    global current_comment
    translation = translated_title(submission)
    current_comment += '**'
    current_comment += translation
    current_comment += '**'

def append_translation_link(submission):
    global current_comment
    current_comment += '\n\n' \
                       '[Read webpage with Google Translate]' \
                       '(https://translate.google.com/translate?hl=en&sl=auto&tl=en&u='
    current_comment += submission.url
    current_comment += ').'

def append_footer(submission):
    global current_comment
    current_comment += '\n\n---\n\n' \
                       'I am a bot. I provide the English title translation of posts in Russian here in /r/russia.' \
                       '\n\n' \
                       'Feedback? [Message the author](https://www.reddit.com/message/compose/?to=RussiaBot). ' \
                       'OP: You may [delete](https://www.reddit.com/message/compose/?to=RussiaBot&subject=' \
                       'Action:Delete&message='
    current_comment += submission.id
    current_comment += ') if you think this is a bad translation.'

# Initialize Reddit Praw
r = praw.Reddit(user_agent=config.user_agent)
r.login(config.username, config.password)

# Initialize translator
gs = goslate.Goslate()

#already_done = []  # list of things that are done

# Main program / loop

subreddit = r.get_subreddit(config.subreddit_name)

current_comment = ''  # this is used for building the comment

while True:
    print('Gathering new submissions.')
    last_commented = config.last_commented

    # Turning the list upside down:
    upside_down = []

    for submission in subreddit.get_new(limit=config.limit):
        upside_down.append(submission)

    upside_down.reverse()

    for submission in upside_down:
        if submission.created_utc > config.last_commented:
            print('New submission found.')  # debug
            language = gs.detect(submission.title)  # get language
            if language == config.source_language:  # check language
                print('Russian language detected. Adding comment...')  # debug
                clear_comment()
                append_title(submission)
                if not submission.is_self:
                    append_translation_link(submission)
                append_footer(submission)
                submission.add_comment(current_comment)  # Add comment of translated text
                print('Comment added.')  # debug
            else:
                print('Language other than russian detected.')  # debug
            print('Adding element to already-done-list.')  # debug
            #already_done.append(submission.id)
            last_commented = submission.created_utc
    config.set_last_commented(last_commented)
    print('Done with all submissions. Going to sleep.')
    time.sleep(config.sleep_time)
