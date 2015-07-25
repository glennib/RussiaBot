import time
import praw
import goslate
import config
import auxiliary

# transfering to heroku

def delete_comment(message):
    submission = r.get_submission(submission_id=message.subject[-6:])
    if submission.author.name == message.author.name:
        for comment in submission.comments:
            if comment.author.name == config.username:
                print('Comment by me found. Deleting.')
                comment.delete()
    else:
        print('Someone who\'s not OP tried to delete a message.')

def replace_comment(message):
    submission = r.get_submission(submission_id=message.subject[-6:])
    if submission.author.name == message.author.name:
        delete_comment(message)
        post_comment(submission, message.body)
    else:
        print('Someone who\'s not OP tried to replace a message.')


def parse_action(message):
    if message.subject[7:].startswith('Delete'):
        print('Delete action. Deleting comment...')
        delete_comment(message)  # pass ID which should be in message body
    elif message.subject[7:].startswith('Replace'):
        print('Replace action. Replacing comment...')
        replace_comment(message)
    else:
        print('Unknown action. Forwarding to maintainer.')
        forward(message)


def forward(message):
    sender = message.author.name
    message_body = 'Sent by: ' + sender + '\n\n---\n\n'
    message_body += message.body
    # r.send_message(config.maintainer, message.subject, message_body)


def parse_message(message):
    if message.subject.startswith('Action:'):
        print('Action message found. Parsing action...')
        parse_action(message)
    else:
        print('Non-action message found. Forwarding to maintainer...')
        forward(message)


def check_inbox():
    # Acquiring and sorting list.
    messages = []
    for message in r.get_inbox():
        messages.append(message)
    messages.reverse()

    for message in messages:
        if message.created_utc > config.last_inbox.value:
            print('Unseen message found. Processing...')
            try:
                parse_message(message)
            except:
                print('Something happened while trying to process a message in inbox.')
            config.set_db_setting(config.last_inbox, message.created_utc)


def translated_title(submission):
    return gs.translate(submission.title, config.target_language)


def clear_comment():
    global _current_comment
    _current_comment = ''


def append_title(submission, translation=''):
    global _current_comment
    if translation == '':
        translation = translated_title(submission)
    _current_comment += '**'
    _current_comment += translation
    _current_comment += '**'


def append_translation_link(submission):
    global _current_comment
    _current_comment += '\n\n'
    url = 'https://translate.google.com/translate?hl=en&sl=auto&tl=en&u='
    url += submission.url
    _current_comment += auxiliary.create_url('Read webpage with Google Translate', url)
    _current_comment += '.'


def append_footer(submission):
    global _current_comment
    _current_comment += '\n\n---\n\n' \
                       'I am a bot. I provide the English title translation of posts in Russian here in /r/russia.' \
                       '\n\n' \
                       'Feedback? '
    _current_comment += auxiliary.create_url('Message the author',
                                             'https://np.reddit.com/message/compose/?to=RussiaBot')
    _current_comment += '. OP: You may '
    url = 'https://np.reddit.com/message/compose/?to=RussiaBot&subject=Action:Delete:'
    url += submission.id
    url += '&message=Leave a comment or just as it is.'
    _current_comment += auxiliary.create_url('delete', url)
    _current_comment += ' or '
    url = 'https://np.reddit.com/message/compose/?to=RussiaBot&subject=Action:Replace:'
    url += submission.id
    url += '&message=Replace this text with your translation, and I will replace it soon.'
    _current_comment += auxiliary.create_url('replace', url)
    _current_comment += ' if you think this is a bad translation.'

def append_disclaimer():
    global _current_comment
    _current_comment += '\n\n' \
                        '*This translation was suggested by OP.*'

def post_comment(submission, translation=''):
    clear_comment()
    append_title(submission, translation)
    if not submission.is_self:
        append_translation_link(submission)
    append_footer(submission)
    if translation != '':
        append_disclaimer()
    comment = submission.add_comment(_current_comment)  # Add comment of translated text
    print('Comment added.')  # debug

def check_submissions():
    last_commented = config.last_commented.value

    # Turning the list upside down:
    upside_down = []

    for submission in subreddit.get_new(limit=config.limit):
        upside_down.append(submission)

    upside_down.reverse()

    for submission in upside_down:
        if submission.created_utc > config.last_commented.value:
            print('New submission found.')  # debug
            language = gs.detect(submission.title)  # get language
            if language == config.source_language:  # check language
                print('Russian language detected. Adding comment...')  # debug
                post_comment(submission)
            else:
                print('Language other than russian detected.')  # debug
            # print('Adding element to already-done-list.')  # debug
            # already_done.append(submission.id)
            last_commented = submission.created_utc
    config.set_db_setting(config.last_commented, last_commented)


# Initialize Reddit Praw
r = praw.Reddit(user_agent=config.user_agent)
r.login(config.username, config.password)

# Initialize translator
gs = goslate.Goslate()

# already_done = []  # list of things that are done

# Main program / loop

subreddit = r.get_subreddit(config.subreddit_name)

_current_comment = ''  # this is used for building the comment

while True:
    print('Gathering new submissions.')
    check_submissions()
    print('Done with all submissions. Checking inbox.')
    check_inbox()
    print('Done with inbox. Going to sleep.')
    time.sleep(config.sleep_time)
