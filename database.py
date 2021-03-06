from peewee import *
import urllib.parse
import os

database_url = ''
db = None # For broadening the scope of DB

local_app = False

try:
    database_url = os.environ['CLEARDB_DATABASE_URL']
except:
    local_app = True

if not local_app:
    print('CLEARDB_DATABASE_URL found. Assuming Heroku app.')
    url = urllib.parse.urlparse(os.getenv('CLEARDB_DATABASE_URL'))
    dbname = url.path[1:]

    db = MySQLDatabase(dbname, host=url.hostname, user=url.username, passwd=url.password)
else:
    print('CLEARDB_DATABASE_URL not found. Assuming local operation. '
          'Reading config info from local file. Also creating local DB.')
    db = SqliteDatabase('russiabot.db')


class Setting(Model):
    name = CharField(index=True, unique=True)
    value = DoubleField()

    class Meta:
        database = db


db.connect()


# Create setting table if it doesn't exist already
if 'setting' not in db.get_tables():
    db.create_table(Setting)
    print('Setting table not found. Created.')
else:
    print('Setting table exists. Do nothing.')

# Delete if true
if False:
    print('Deleting all entries in table Setting')
    for setting in Setting.select():
        setting.delete_instance()

# Define function for safely creating setting
def create_safe_setting(name, value):
    setting = Setting()
    try:
        print('Trying to find ' + name + '...')
        setting = Setting.get(Setting.name == name)
        print('Found it! Assigning...')
    except DoesNotExist:
        print(name + ' not found. Creating...')
        setting = Setting.create(name=name, value=value)
        setting.save()
    return setting

# Create setting_1 if it doesn't exist already
last_commented = create_safe_setting('last_commented', 0)
last_inbox = create_safe_setting('last_inbox', 0)

db.close()


def set_db_setting(setting, value):
    print('Writing ' + str(setting.value) + ' to ' + setting.name + ' in database.')
    db.connect()
    setting.value = value
    setting.save()
    db.close()