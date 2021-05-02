from flask_mysqldb import MySQL
import MySQLdb.cursors


class ClassTable:

    def __init__(self, cursor):
        self.cursor = cursor

    def all(self):
        self.cursor.execute('SELECT * FROM class')
        return self.cursor

    def allBySchool(self, id):
        self.cursor.execute('SELECT * FROM class WHERE id_school = %s ', (id,))
        return self.cursor

    def all_info(self, id):
        self.cursor.execute('SELECT * FROM class WHERE id = %s', (id,))
        return self.cursor.fetchone()

    def all_info_by_name(self, name):
        self.cursor.execute('SELECT * FROM class WHERE `name` = %s', (name,))
        return self.cursor.fetchone()

    def add(self, request, mysql, id):
        self.cursor.execute('INSERT INTO class VALUES (NULL, %s, %s)', (request.form['name'], id,))
        mysql.connection.commit()

    def edit(self, request, mysql, id):
        self.cursor.execute("UPDATE class SET `name` = %s WHERE id = %s", (request.form['name'], id,))
        mysql.connection.commit()

    def delete(self, mysql, id):
        self.cursor.execute('DELETE FROM class WHERE `id` = %s', (id,))
        mysql.connection.commit()