import mysql.connector

__cont = None

def get_sql_connection():
    global __cont
    if __cont is None:
        
    return __cont