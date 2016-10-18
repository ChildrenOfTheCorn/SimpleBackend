#!/usr/bin/python
# -*- coding: utf-8
#
# Тут расположены обработчики запросов
#
import datetime
import os
from bottle import default_app, route, run, template, static_file, error, post, response, request
import json
from dbutils import DbService
from auth import Auth
import methods
import request_fields
import response_fields
import error_codes

API = '/api/upc1/'
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


@post(API + methods.REGISTRATION)
def registration():
    login = request.query[request_fields.LOGIN]
    name = request.query[request_fields.NAME]
    password = request.query[request_fields.PASSWORD]

    is_success, token_data = auth.register(login=login, name=name, password=password)
    if is_success:
        response.set_header('Set-Cookie', response_fields.TOKEN + '=' + token_data)
        response.add_header('Set-Cookie', response_fields.EAN + '=' + login)
        return json.dumps({response_fields.SUCCESS: "OK"})
    return make_error_response(token_data)


@post(API + methods.AUTHORIZATION)
def authorization():
    login = request.query[request_fields.LOGIN]
    password = request.query[request_fields.PASSWORD]

    is_success, token_data = auth.auth(login=login, password=password)
    if is_success:
        response.set_header('Set-Cookie', response_fields.TOKEN + '=' + token_data)
        response.add_header('Set-Cookie', response_fields.EAN + '=' + login)
        return json.dumps({response_fields.SUCCESS: "OK"})
    return make_error_response(token_data)


@route(API + methods.GET_WALLETS)
def get_wallets():
    token = request.get_cookie(response_fields.TOKEN)
    ean = request.get_cookie(response_fields.EAN)
    if token:
        user_id = auth.get_profile_by_token(token)
        if user_id:
            return db.get_wallets(user_id=user_id)

    return make_auth_error_response()


@post(API + methods.ADD_WALLET)
def add_wallet():
    token = request.get_cookie(response_fields.TOKEN)
    ean = request.get_cookie(response_fields.EAN)
    if token:
        user_id = auth.get_profile_by_token(token)
        if user_id:
            name = request.query[request_fields.NAME]
            currency = request.query[request_fields.CURRENCY]
            auth.prolongate_session(user_id)
            return db.add_wallet(user_id=user_id, name=name, currency=currency)

    return make_auth_error_response()


@route(API + methods.GET_ENTRIES)
def get_entries():
    token = request.get_cookie(response_fields.TOKEN)
    ean = request.get_cookie(response_fields.EAN)
    if token:
        user_id = auth.get_profile_by_token(token)
        if user_id:
            wallet_id = request.query[request_fields.WALLET_ID]
            auth.prolongate_session(user_id)
            return db.get_entries(wallet_id=wallet_id)

    return make_auth_error_response()


@error(404)
@error(403)
def mistake(code):
    return 'Error on page'


def make_error_response(errorData):
    return json.dumps({response_fields.SUCCESS: "ERROR",
                       response_fields.ERROR: errorData})


def make_auth_error_response():
    return make_error_response({response_fields.ERROR_CODE: error_codes.ERROR_CODE_AUTH,
                                response_fields.ERROR_MESSAGE: error_codes.ERROR_MESSAGE_AUTH})


if __name__ == "__main__":
    run(host='localhost', port=8080)
application = default_app()
