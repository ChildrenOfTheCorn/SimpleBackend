import datetime
import os
from bottle import default_app, route, run, template, static_file, error, post, response, request
from dbutils import DbService
from auth import Auth
import json

TEST_PASSWORD = "0000"

TEST_EAN = "0000000000000"

path = os.path.abspath(__file__)
ROOT = os.path.dirname(path)

db = DbService()

############ test auth ######################
auth = Auth(db)
token = auth.register(TEST_EAN, "test name", TEST_PASSWORD)

print "token = " + token
res = auth.auth(TEST_EAN, TEST_PASSWORD)
user_id = res[0]
if not res[0]:
    print 'auth not success', res[1]
    exit(1)

print "auth success", res[1]
token = res[1]

res = auth.check_token(TEST_EAN, token)
if not res:
    print 'check_token not success'
    exit(1)

print "check_token success", res

############## test wallets ################
res = db.add_wallet(user_id, "usd wallet", "USD")
if not res[0]:
    print res[1]

res = db.get_wallets(user_id)
print res


res = db.add_entry(1, user_id, "entry", 1000)
print res[1]

res = db.get_entries(1)
print res[1]

""""
res = json.loads(db.add_request(1, 1))
request_id = None
if res.get('data') != None:
    request_id = res.get('data').get('id')

if request_id == None:
    print 'request_id is None'
    exit(0)

raw = db.approve_request(1)
res = json.loads(raw)
print res
if res.get('data') != True:
    print 'approve_request with error'
    print res.get("error")
    exit(0)
print res
"""
