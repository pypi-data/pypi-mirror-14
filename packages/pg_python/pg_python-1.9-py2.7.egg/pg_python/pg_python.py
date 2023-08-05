from _db_object import Db
from _write import make_postgres_write_statement
from _read import make_postgres_read_statement, prepare_values
from _update import make_postgres_update_statement
from _delete import make_postgres_delete_statement


db = None

def _get_db():
    global db
    return db

print_debug_log = True
params_map = {}
def pg_server(db_name, username, password, host_address, debug=True):
  global db, print_debug_log, params_map
  params_map = {
    'dbname': db_name,
    'user': username,
    'password': password,
    'host': host_address,
    }
  db = Db(params_map)
  print_debug_log = debug

def write(table, kv_map):
    """
    :param table: String.
    :param kv_map: Key values.
    :return success_bool:
    """
    global db, print_debug_log, params_map
    connection = db.get_connection()
    cursor = db.get_cursor()
    command, values = make_postgres_write_statement(table, kv_map, print_debug_log)
    try:
        cursor.execute(command, values)
        connection.commit()
    except Exception as e:
        print("Db Cursor Write Error: %s" % e)
        db = Db(params_map)
        return False
    return True

def read(table, keys_to_get, kv_map, limit=None, order_by=None, order_type=None):
    """
    :param table: String
    :param keys_to_get: list of strings
    :param kv_map: key value map, if this is None, then limit is maxed at 1000
    :param limit: None or integer
    :param order_by: None or must be of a type String
    :param order_type: String None, "ASC" or "DESC" only
    :return: values in an array of key value maps
    """
    error_return = None
    cursor = db.get_cursor()
    command, values = make_postgres_read_statement(table, kv_map, keys_to_get, limit, order_by, order_type, print_debug_log)
    try:
        cursor.execute(command, values)
        all_values = cursor.fetchall()
        return prepare_values(all_values, keys_to_get)
    except Exception as e:
        print("Db Cursor Read Error: %s" % e)
        return []

def update(table, update_kv_map, where_kv_map):
    """
    :param table: table name, type string
    :param update_kv_map: the NEW keyvalue map for values to be updated
    :param where_kv_map: the kv map to search for values, all values ARE ANDed.
    :return: Success or Failure.
    """
    global db, print_debug_log, params_map
    connection = db.get_connection()
    cursor = db.get_cursor()
    command, values = make_postgres_update_statement(table, update_kv_map, where_kv_map, print_debug_log)
    try:
        cursor.execute(command, values)
        connection.commit()
    except Exception as e:
        print("Db Cursor Update Error: %s" % e)
        db = Db(params_map)
        return False
    return True


def delete(table, where_kv_map):
    """
    Delete the rows resulting from the mentined kv map. No limit.
    :param table: table name, must be string
    :param where_kv_map: the kv map to search for values, all values ARE ANDed.
    :return: True or False
    """
    global db, print_debug_log, params_map
    connection = db.get_connection()
    cursor = db.get_cursor()
    command, values = make_postgres_delete_statement(table, where_kv_map, print_debug_log)
    try:
        cursor.execute(command, values)
        connection.commit()
    except Exception as e:
        print("Db Cursor Delete Error: %s" % e)
        db = Db(params_map)
        return False
    return True
