#!/usr/bin/python
# -*- coding: utf-8
#
# Логика работы с авторизацией через куки
#
import json
import uuid
from datetime import timedelta
from datetime import datetime
import error_codes
import response_fields


class Auth:
    def __init__(self, db_service):
        self.db = db_service
        self.expire_period = 60 * 5

    def register(self, login, name, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = ("INSERT INTO users "
               "(ean, name, password, token, timestamp) "
               "VALUES (%s, %s, %s, %s, %s)")

        try:
            # Execute the SQL command
            # generate refresh token, access token
            token = self._generateToken()

            timestamp = datetime.now() + timedelta(seconds=self.expire_period)

            ts = timestamp.strftime('%Y-%m-%d %H:%M:%S')

            data = (login, name, password, token, ts)
            cursor.execute(sql, data)
            id = cursor.lastrowid
            conn.commit()
            return True, token
        except Exception as e:
            conn.rollback()
            print "Error: unable to fetch data, " + str(e)
            return False, {response_fields.ERROR_CODE: error_codes.ERROR_CODE_SQL_ECXEPTION,
                           response_fields.ERROR_MESSAGE: str(e)}
        finally:
            cursor.close()

    # return (is_success, data)
    def auth(self, login, password):
        is_success = True
        conn = self.db.get_connection()
        cursor = conn.cursor()
        user_id, user_name = self._get_user_id(cursor, login, password)
        if user_id is None:
            cursor.close()
            return False, {response_fields.ERROR_CODE: error_codes.ERROR_CODE_AUTH,
                           response_fields.ERROR_MESSAGE: error_codes.ERROR_MESSAGE_AUTH}

        sql = ("UPDATE users "
               " SET token = %s, timestamp = %s "
               " WHERE id = %s")
        try:
            # Execute the SQL command
            token = self._generateToken()
            timestamp = datetime.now() + timedelta(seconds=self.expire_period)
            data = (token, timestamp, user_id)
            cursor.execute(sql, data)
            id = cursor.lastrowid
            conn.commit()
            res = token
        except Exception as e:
            conn.rollback()
            is_success = False
            print "Error: unable to fecth data, " + str(e)
            res = {response_fields.ERROR_CODE: error_codes.ERROR_CODE_SQL_ECXEPTION,
                   response_fields.ERROR_MESSAGE: str(e)}
        cursor.close()
        return (is_success, res)

    def check_token(self, ean, token):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        user_id = self._get_user_id_by_token(cursor, token)
        if user_id is None:
            cursor.close()
            return False

        sql = ("UPDATE users "
               " SET timestamp = %s "
               " WHERE id = %s")
        try:
            # Execute the SQL command
            timestamp = datetime.now() + timedelta(seconds=self.expire_period)
            data = (timestamp, user_id)
            cursor.execute(sql, data)
            id = cursor.lastrowid
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print "Error: unable to fecth data, " + str(e)
            res = {response_fields.ERROR_CODE: error_codes.ERROR_CODE_SQL_ECXEPTION,
                   response_fields.ERROR_MESSAGE: str(e)}
            return False
        finally:
            cursor.close()

    def prolongate_session(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = ("UPDATE users "
               " SET timestamp = %s "
               " WHERE id = %s")
        try:
            # Execute the SQL command
            timestamp = datetime.now() + timedelta(seconds=self.expire_period)
            data = (timestamp, user_id)
            cursor.execute(sql, data)
            id = cursor.lastrowid
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print "Error: unable to fecth data, " + str(e)
            res = {response_fields.ERROR_CODE: error_codes.ERROR_CODE_SQL_ECXEPTION,
                   response_fields.ERROR_MESSAGE: str(e)}
            return False
        finally:
            cursor.close()

    # find user by login, password
    def _get_user_id(self, cursor, login, password):
        sql = ("SELECT id, name FROM users "
               "WHERE ean = %s AND password = %s")
        data = (login, password)

        # Execute the SQL command
        cursor.execute(sql, data)
        # Fetch all the rows in a list of lists.
        rows = cursor.fetchall()
        for row in rows:
            return row[0], row[1]
        return None, None

    def get_profile_by_token(self, token):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = ("SELECT id, timestamp FROM users "
               "WHERE token = %s;")

        data = [token]
        profile_id = None
        try:
            # Execute the SQL command
            cursor.execute(sql, data)
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
            return "Error: unable to fecth data, " + str(e) + ", type = " + type(timestamp)
        cursor.close()
        return profile_id

    def _get_user_id_by_token(self, cursor, token):
        sql = ("SELECT id, timestamp FROM users "
               "WHERE token = %s;")
        data = [token]
        profile_id = None
        try:
            # Execute the SQL command
            cursor.execute(sql, data)
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
        return profile_id

    def _generateToken(self):
        return uuid.uuid4().hex
