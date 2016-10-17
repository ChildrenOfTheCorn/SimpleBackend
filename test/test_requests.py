import datetime
import os
from bottle import default_app, route, run, template, static_file, error, post, response, request
from dbutils import DbService
import json

path = os.path.abspath(__file__)
ROOT = os.path.dirname(path)

db = DbService()
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
raw = db.get_requests(1)
print raw
res = json.loads(raw)
request_id = None
if res.get('data') != None:
    request_id = res.get('data').get('id')

if request_id == None:
    print 'request_id is None'
    exit(0)

db.close()
