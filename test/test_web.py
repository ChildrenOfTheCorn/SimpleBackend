from webtest import TestApp
import bottle_app
import json
def register(app):
    res = app.post('/api/register', {'login': '111', 'password': '101010', 'name': 'Test'})  # log in and get a cookie
    json_resp = json.loads(res.body)
    assert json_resp.get('data') != None  # fetch a page successfully
    return json_resp.get('data').get('accessToken')


def auth(app):
    res = app.post('/api/auth', {'login': '111', 'password': '101010'})  # log in and get a cookie
    json_resp = json.loads(res.body)
    print json_resp
    assert json_resp.get('data') != None  # fetch a page successfully
    return json_resp.get('data').get('accessToken')

def test_register():
    app = TestApp(bottle_app.application)
    res = register(app=app)
    print res

def test_auth():
    app = TestApp(bottle_app.application)
    res = auth(app=app)
    print res

#test_register()
test_auth()