#!/usr/bin/python
# -*- coding: utf-8
#
# Тут вся работа с бд
#
import json
import MySQLdb
import sys, traceback
from config import *

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

    #API
    def get_users(self):
        self.get_connection()
        sql = "SELECT id, login, name, access_token, refresh_token, access_token FROM user;"
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({'id': row[0],
                               'login': row[1],
                               'name': row[2],
                               'accessToken':row[3],
                               'refreshToken':row[4]})
            return json.dumps({"data": result})
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            return '{"error":{ "code":1, "message":' + str(e) + '}}'
        finally:
            self.close()

    # services list for client
    def add_request(self, user_id, list_id):
        self.get_connection()
        sql = ("INSERT INTO request "
               "(user_id, shop_list_id) "
               "VALUES (%s, %s)")
        data = (user_id, list_id)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            id = self.cursor.lastrowid
            res = json.dumps({"data": {"id":id}})
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    # incoming request list
    def get_all_requests(self, user_id):
        self.get_connection()
        sql = ("SELECT r.id, s.user_id, u.name, u.login, r.shop_list_id, s.name list_name FROM request AS r "
                "INNER JOIN shop_list AS s ON s.id = r.shop_list_id "
                "INNER JOIN user AS u ON r.user_id = u.id "
                "WHERE r.approved = 0 AND s.user_id = %s;")
        data = (user_id)
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({'id':row[0],
                                'ownerId': row[1],
                               'ownerName': row[2],
                               'ownerLogin': row[3],
                               'listId': row[4],
                               'listName': row[5]})
            return json.dumps({"data": result})
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            return '{"error":{ "code":1, "message":' + str(e) + '}}'
        finally:
            self.close()

    # get requests for subscribtion
    def get_requests(self, list_id):
        self.get_connection()
        sql = ("SELECT r.id, r.user_id, u.name, u.login FROM request AS r "
               " INNER JOIN user AS u ON r.user_id = u.id "
               " WHERE r.approved = 0 AND r.shop_list_id = %s;")
        result = []
        data = (list_id)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({'id': row[0],
                                'userId':row[1],
                                'userName': row[2],
                                'userLogin': row[3]})
            return json.dumps({"data": result})
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            traceback.print_exc(file=sys.stdout)
            return '{"error":{ "code":1, "message":' + str(e) + '}}'
        finally:
            self.close()

    # get subscriptions to another lists
    def get_subscriptions(self, user_id):
        self.get_connection()
        sql = ("SELECT s.user_id, u.name, u.login, r.shop_list_id, s.name list_name, r.approve FROM request AS r "
               "INNER JOIN shop_list AS s ON s.id = r.shop_list_id "
               "INNER JOIN user AS u ON s.user_id = u.id"
               "WHERE r.user_id = %s "
               "ORDER BY r.approve, s.user_id, u.name")

        data = (user_id)
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({'userId': row[0],
                               'name': row[1],
                               'login': row[2],
                               'listId': row[3],
                               'listName': row[4],
                               'approve':row[5]})
            return json.dumps({"data": result})
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            return '{"error":{ "code":1, "message":' + str(e) + '}}'
        finally:
            self.close()

    # approve request
    def approve_request(self, request_id):
        self.get_connection()
        sql = ("UPDATE request SET approved = 1 "
               "WHERE id = %s;")
        data = (request_id)
        res = None
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            res = '{"data":true}'
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    #reject request
    def reject_request(self, request_id):
        self.get_connection()
        sql = ("DELETE FROM request "
               "WHERE id = %s;")
        data = (request_id)
        res = None
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            res = '{"data":true}'
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    # add shop list
    def create_shop_list(self, user_id, name, is_public):
        self.get_connection()
        sql = ("INSERT INTO shop_list "
               "(user_id, name, is_public) "
               "VALUES (%s, %s, %s)")
        data = (user_id, name, is_public)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            id = self.cursor.lastrowid
            res = json.dumps({"data": {"id":id}})
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print ( "Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    # not empty slots list for client
    def get_shop_lists(self, user_id):
        self.get_connection()
        sql = ( "SELECT s.id, s.name, s.is_public, u.id, u.login, u.name user_name FROM shop_list AS s "
                " LEFT JOIN request AS r ON r.shop_list_id = s.id "
                " INNER JOIN user AS u ON u.id = s.user_id "
                " WHERE (r.user_id = %s AND r.approved = 1) OR (s.user_id = %s);")
        data = (user_id, user_id)
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                user_id_res = row[3]
                if user_id_res == user_id:
                    user_id_res = 0
                result.append({'id': row[0],
                                'name': row[1],
                                'isPublic': row[2] == 1,
                                'ownerId': user_id_res,
                                'ownerLogin': row[4],
                                'ownerName': row[5]
                               })
            return json.dumps({"data": result})
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            return json.dumps({"error": {"code": 1, "message": str(e)}})
        finally:
            self.close()


    # not empty slots list for client
    def get_public_shop_lists(self, login):
        self.get_connection()
        sql = ("SELECT s.id, s.name FROM user AS u "
                " INNER JOIN shop_list AS s ON u.id = s.user_id"
                " WHERE u.login = '"+login+"' AND s.is_public = 1;")
        data = (login)
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({'id': row[0], 'name': row[1]})
            return json.dumps({"data": result})
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            return json.dumps({"error": {"code": 1, "message": str(e), "description": login}})
        finally:
            self.close()

    # delete user
    def delete_user(self, id):
        self.get_connection()
        sql = ("DELETE FROM user WHERE id = %s")
        data = (id)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            id = self.cursor.lastrowid
            self.db.commit()
            res = '{"data":true}'
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    def delete_shop_list(self, id):
        self.get_connection()
        sql = ("DELETE FROM shop_list WHERE id = %s")
        data = (id)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            self.db.commit()
            res = '{"data":true}'
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    def add_entry(self, list_id, user_id, name, count):
        self.get_connection()
        sql = ("INSERT INTO entry "
               "(shop_list_id, user_id, name, count, state) "
               "VALUES (%s, %s, %s, %s, 0)")
        data = (list_id, user_id, name, count)
        res = None
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            id = self.cursor.lastrowid
            res = json.dumps({"data": {"id":id}})
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    def get_entries(self,list_id):
        self.get_connection()
        sql = ("SELECT e.id, e.name, e.owner_id, u.login, u.name, e.state FROM entry AS e "
               " LEFT JOIN user AS u ON e.owner_id = u.id "
               " WHERE e.shop_list_id = %s"
               " ORDER BY e.state, e.name;")

        data = (list_id)
        result = []
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            # Fetch all the rows in a list of lists.
            rows = self.cursor.fetchall()
            for row in rows:
                result.append({'id': row[0],
                                'name': row[1],
                                'ownerId': row[2],
                                'ownerLogin': row[3],
                                'ownerName': row[4],
                                'state':row[5]})
            return json.dumps({"data": result})
        except Exception as e:
            print ("Error: unable to fecth data, " + str(e))
            return json.dumps({"success": False, "error": 1, "errorString": str(e)})
        finally:
            self.close()

    def delete_entry(self, id):
        self.get_connection()
        sql = ("DELETE FROM entry WHERE id = %s")
        data = (id)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            id = self.cursor.lastrowid
            self.db.commit()
            res = '{"data":true}'
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res

    # update entry state
    def update_entry_state(self, entry_id, owner_id, state):
        self.get_connection()
        sql = ("UPDATE entry SET state = %s,  owner_id = %s "
               "WHERE id = %s;")
        data = (state, owner_id, entry_id)
        res = None
        try:
            # Execute the SQL command
            self.cursor.execute(sql, data)
            res = '{"data":true}'
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print ("Error: unable to fecth data, " + str(e))
            res = '{"error":{"code":1, "message":' + str(e) + '}}'
        finally:
            self.close()
        return res
