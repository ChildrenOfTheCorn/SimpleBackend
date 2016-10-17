#!/usr/bin/python
# -*- coding: utf-8
#
# Тут вся работа с бд
#
import json
import MySQLdb
import sys, traceback
from config import *
import response_fields
import error_codes


# Класс работы с бд
class DbService:
    def __init__(self):
        # подключаемся к базе данных (не забываем указать кодировку, а то в базу запишутся иероглифы)
        self.db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB, charset='utf8')
        # формируем курсор, с помощью которого можно исполнять SQL-запросы
        self.cursor = self.db.cursor()

    # закрываем соединение с базой данных
    def close(self):
        self.db.close()

    def get_connection(self):
        self.db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB, charset='utf8')
        self.cursor = self.db.cursor()
        return self.db

    # API
    def get_wallets(self, user_id):
        self.get_connection()
        sql = "SELECT id, name, currency FROM wallets WHERE user_id = %s;"
        data = [user_id]
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({response_fields.ID: row[0],
                               response_fields.NAME: row[1],
                               response_fields.CURRENCY: row[2]})
            return self._make_success(result)
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            return self._make_error(str(e))
        finally:
            self.close()

    # services list for client
    def add_wallet(self, user_id, name, currency):
        is_success = True
        self.get_connection()
        sql = ("INSERT INTO wallets "
               "(user_id, name, currency) "
               "VALUES (%s, %s, %s)")
        data = (user_id, name, currency)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            id = self.cursor.lastrowid
            res = self._make_success({
                response_fields.ID: id,
                response_fields.NAME: name,
                response_fields.CURRENCY: currency})
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            is_success = False
            print ("Error: unable to fecth data, " + str(e))
            res = self._make_error(str(e))
        finally:
            self.close()
        return (is_success, res)

    def add_entry(self, wallet_id, user_id, name, price):
        self.get_connection()
        is_success = True
        sql = ("INSERT INTO entry "
               "(wallet_id, user_id, name, price) "
               "VALUES (%s, %s, %s, %s)")
        data = (wallet_id, user_id, name, price)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            id = self.cursor.lastrowid
            res = self._make_success({response_fields.ID: id,
                                      response_fields.NAME: name,
                                      response_fields.PRICE: price})
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            is_success = False
            print ("Error: unable to fecth data, " + str(e))
            res = self._make_error(str(e))
        finally:
            self.close()
        return (is_success, res)

    def get_entries(self, wallet_id):
        self.get_connection()
        sql = ("SELECT e.id, e.name, e.price FROM entry AS e "
               " WHERE e.wallet_id = %s"
               " ORDER BY e.name;")

        data = [wallet_id]
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({response_fields.ID: row[0],
                               response_fields.NAME: row[1],
                               response_fields.PRICE: row[2]})
            return True, self._make_success(result)
        except Exception as e:
            print ("Error: unable to fetch data, " + str(e))
            return False, self._make_error(str(e))
        finally:
            self.close()

    def delete_entry(self, id):
        self.get_connection()
        sql = ("DELETE FROM entry WHERE id = %s")
        data = [id]
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            self.db.commit()
            return self._make_success_empty()
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            return self._make_error(str(e))
        finally:
            self.close()

    def _make_error(self, error_data):
        return json.dumps({response_fields.SUCCESS: "ERROR",
                           response_fields.ERROR: {
                               response_fields.ERROR_CODE: error_codes.ERROR_CODE_SQL_ECXEPTION,
                               response_fields.ERROR_MESSAGE: error_data}})

    def _make_success(self, data):
        return json.dumps({response_fields.SUCCESS: "OK",
                           response_fields.DATA: data})

    def _make_success_empty(self):
        return json.dumps({response_fields.SUCCESS: "OK"})
