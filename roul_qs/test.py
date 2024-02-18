import configparser,psycopg2

config = configparser.ConfigParser()
config.read('roul_qs/db.INI')
print(type((config['db_connection']['password'])))
# print(config['DEFAULT']['path'])     # -> "/path/name/"
# config['DEFAULT']['path'] = '/var/shared/'    # update
# config['DEFAULT']['default_message'] = 'Hey! help me!!'   # create

# with open('FILE.INI', 'w') as configfile:    # save
#     config.write(configfile)


conn = psycopg2.connect(
    host=(config['db_connection']['host']),
    database=(config['db_connection']['database']),
    user=(config['db_connection']['user']),
    password=(config['db_connection']['password'])
)

cur = conn.cursor()
cur.execute('SELECT * FROM books;')
books = cur.fetchall()
print(books)
