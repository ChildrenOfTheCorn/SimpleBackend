#!/usr/bin/python
# -*- coding: utf-8
#
# Логика работы с авторизацией через Oauth2
#
import json
import uuid
from datetime import timedelta
from datetime import datetime


class OAuth2:
    def __init__(self, dbService):
        self.db = dbService
        self.expire_period = 3600

    def register(self, login, password, name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = ("INSERT INTO user "
               "(login, password, name, access_token, refresh_token, timestamp) "
               "VALUES (%s, %s, %s, %s, %s, %s)")

        res = None
        try:
            # Execute the SQL command
            # generate refersh token, access token
            access_token = self._generateToken()
            refresh_token = self._generateToken()
            timestamp = datetime.now() + timedelta(seconds=self.expire_period)
            ts = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            data = (login, password, name, access_token, refresh_token, ts)
            cursor.execute(sql, data)
            id = cursor.lastrowid
            conn.commit()
            res = json.dumps({ 'data':
                {'accessToken': access_token, 'refreshToken': refresh_token}})
        except Exception as e:
            conn.rollback()
            print "Error: unable to fecth data, " + str(e)
            res = json.dumps({"error": {"code": 1, "message": str(e)}})
        cursor.close()
        return res

    def auth(self, login, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        user_id, user_name = self._get_user_id(cursor, login, password)
        if user_id is None:
            cursor.close()
            return json.dumps({'error': {"code":2, "message": "user not found"}})

        sql = ("UPDATE user "
               " SET access_token = %s, refresh_token = %s, timestamp = %s "
               " WHERE id = %s")
        try:
            # Execute the SQL command
            access_token = self._generateToken()
            refresh_token = self._generateToken()
            timestamp = datetime.now() + timedelta(seconds=self.expire_period)
            data = (access_token, refresh_token, timestamp, user_id)
            cursor.execute(sql, data)
            id = cursor.lastrowid
            conn.commit()
            res = json.dumps({'data':
                {'name': user_name, 'accessToken': access_token, 'refreshToken': refresh_token}})
        except Exception as e:
            conn.rollback()
            print "Error: unable to fecth data, " + str(e)
            res = json.dumps({"error": {"code": 1, "message": str(e)}})
        cursor.close()
        return res

    # find user by login, password
    def _get_user_id(self, cursor, login, password):
        sql = ("SELECT id, name FROM user "
               "WHERE login = %s AND password = %s")
        data = (login, password)
        result = None

        # Execute the SQL command
        cursor.execute(sql,data)
        # Fetch all the rows in a list of lists.
        rows = cursor.fetchall()
        for row in rows:
            result = (row[0], row[1])
            break

        return result

    # refresh access token
    def refresh_token(self, refresh_token):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        user_id = self._get_user_id_by_refresh_token(cursor, refresh_token)
        if user_id is None:
            cursor.close()
            return json.dumps({'error': {"code": 2, "message":"Refresh Token not found"}})

        sql = ("UPDATE user "
               " SET access_token = %s, timestamp = %s "
               " WHERE id = %s")
        try:
            # Execute the SQL command
            access_token = self._generateToken()
            timestamp = datetime.now() + timedelta(seconds=self.expire_period)
            data = (access_token, timestamp, user_id)
            cursor.execute(sql, data)
            id = cursor.lastrowid
            conn.commit()
            res = json.dumps({'data':
                {'accessToken': access_token}})
        except Exception as e:
            conn.rollback()
            print "Error: unable to fecth data, " + str(e)
            res = json.dumps({"error": {"code": 1, "message": str(e)}})
        cursor.close()
        return res

        # find user by login, password

    def _get_user_id_by_refresh_token(self, cursor, refresh_token):
        sql = ("SELECT id FROM user "
               "WHERE refresh_token = %s;")
        data = (refresh_token)
        result = None
        try:
            # Execute the SQL command
            cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = cursor.fetchall()
            for row in rows:
                result = row[0]
                break
        except Exception as e:
            print "Error: unable to fecth data, " + str(e)
        return result

    def get_profile_by_token(self, access_token):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = ("SELECT id, timestamp FROM user "
               "WHERE access_token = '"+access_token+"';")

        data = (access_token)
        profile_id = None
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            rows = cursor.fetchall()
            for row in rows:
                timestamp = row[1]
                now = datetime.now()
                if timestamp > now:
                    profile_id = row[0]
                break
        except Exception as e:
            print "Error: unable to fecth data, " + str(e)
            return "Error: unable to fecth data, " +str(e)+", type = " + type(timestamp)
        cursor.close()
        return profile_id

    def _generateToken(self):
        return uuid.uuid4().hex

