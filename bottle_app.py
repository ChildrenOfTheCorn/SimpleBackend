import datetime
import os
from bottle import default_app, route, run, template, static_file, error, post, response, request
import json
from dbutils import DbService
from auth import Auth

API = '/api/v2/'
BAD_ACCESS_TOKEN_MESSAGE = '"bad access token"'

BAD_ACCESS_TOKEN = '{"error": {"code": 8, "message": ' + BAD_ACCESS_TOKEN_MESSAGE + '}}'

path = os.path.abspath(__file__)
ROOT = os.path.dirname(path)

# init DB
dberror = None
db = None
auth = None
try:
    db = DbService()
    auth = Auth(db)
except Exception as e:
    dberror = str(e)
    print (dberror)


@route('/main')
@route('/')
def index():
    message = "Automated-testing.info"
    now_time = datetime.datetime.now()
    cur_hour = now_time.hour

    try:
        return template('index', cur_hour=cur_hour, msg=message)
    except Exception as e:
        return "error: " + str(e)

@post('/authorization')
def authorization():
    message = "Automated-testing.info"
    now_time = datetime.datetime.now()
    cur_hour = now_time.hour

    #login = request.query['login']
    response.set_header('Set-Cookie', 'name=value')
    response.add_header('Set-Cookie', 'name2=value2')

    try:
        return template('index', cur_hour=cur_hour, msg=message)
    except Exception as e:
        return "error: " + str(e)


@error(404)
@error(403)
def mistake(code):
    return 'Error on page'


if __name__ == "__main__":
    run(host='localhost', port=8080)
application = default_app()
