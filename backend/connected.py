import pymysql
import pymysql.cursors

def DB_connection():
    try:
        connector=pymysql.connect(
            host='localhost',
            user='root',
            password='Gokulj7959$',
            database='ecommerce',
            port=3030,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return connector
    except pymysql.MySQLError as e:
        raise Exception("error in connecting to db") from e