from flask_mysqldb import MySQL
import MySQLdb.cursors


class SchoolTable:

    def __init__(self, cursor):
        self.cursor = cursor

    def all(self):
        self.cursor.execute('SELECT * FROM school')
        return self.cursor

    def all_info(self, id):
        self.cursor.execute('SELECT * FROM school WHERE id = %s', (id,))
        return self.cursor.fetchone()

    def all_info_by_name(self, name):
        self.cursor.execute('SELECT * FROM school WHERE `name` = %s', (name,))
        return self.cursor.fetchone()

    def name(self, id):
        self.cursor.execute('SELECT `name` FROM school WHERE `id` = %s', (id,))
        return self.cursor.fetchone()['name']

    def fetchRequest(self, request):
        return [request.form['name'], request.form['address'], request.form['zip_code'], request.form['city']]

    def add(self, request, mysql):
        req = self.fetchRequest(request)
        self.cursor.execute('INSERT INTO school VALUES (NULL, %s, %s, %s, %s)', (req[0], req[1], req[2], req[3]))
        mysql.connection.commit()

    def edit(self, request, mysql, id):
        req = self.fetchRequest(request)
        self.cursor.execute("UPDATE school SET `name` = %s, address = %s, zip_code = %s, city = %s WHERE id = %s",
                            (req[0], req[1], req[2], req[3], id,))
        mysql.connection.commit()

    def delete(self, mysql, id):
        self.cursor.execute('DELETE FROM school WHERE `id` = %s', (id,))
        mysql.connection.commit()