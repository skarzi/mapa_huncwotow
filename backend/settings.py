DEBUG = True
SECRET_KEY = 'ala_ma_kota'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///huncwoci.db'
SESSION_TYPE = 'filesystem'
USOS_BASE_URL = 'https://apps.usos.pw.edu.pl/services/'
USOS_REQUEST_TOKEN_URL = f'{USOS_BASE_URL}oauth/request_token'
USOS_ACCESS_TOKEN_URL = f'{USOS_BASE_URL}oauth/access_token'
USOS_AUTHORIZE_URL = f'{USOS_BASE_URL}oauth/authorize'
USOS_CONSUMER_KEY = 'uPD7bpTQJ4qqX9Rxmwwe'
USOS_CONSUMER_SECRET = 'p5GTKdWDsq57VmETSeyaF5rPGxLDJdWrcwRwd9pY'
USOS_SCOPES = {'scopes': 'studies'}
USOS_TIMETABLE_URL = f'{USOS_BASE_URL}tt/user'
USOS_PERSONAL_DATA_URL = f'{USOS_BASE_URL}users/user'
