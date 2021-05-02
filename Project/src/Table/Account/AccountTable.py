from flask_mysqldb import MySQL
import MySQLdb.cursors


class AccountTable:

    def __init__(self, cursor):
        self.cursor = cursor

    def all(self):
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        self.cursor.execute('SELECT * FROM account')
        account = self.cursor.fetchone()
        return account

    def all_info(self, id):
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        self.cursor.execute('SELECT * FROM account WHERE id = %s', (id,))
        account = self.cursor.fetchone()
        return account