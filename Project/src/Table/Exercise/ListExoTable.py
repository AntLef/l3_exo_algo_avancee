import random
from flask import session

from project.src.Table.Exercise.Generate_List_Exo.RandomListExo import RandomListExo


class ListExoTable:

    def __init__(self, cursor):
        self.cursor = cursor

    def all(self):
        self.cursor.execute('SELECT * FROM list_exo ')
        return self.cursor

    def all_list_by_prof(self, id_class):
        self.cursor.execute('SELECT l.* FROM account as a INNER JOIN `list_exo` as l WHERE a.id_class = %s GROUP BY l.id_list_exo ', (str(id_class),))
        return [{str(j): str(e) for j, e in i.items()} for i in self.cursor]

    def all_info(self, id):
        self.cursor.execute('SELECT * FROM list_exo WHERE `id_list_exo` = %s', (id,))
        return self.cursor.fetchall()

    def all_info_by_prof(self, id):
        self.cursor.execute('SELECT * FROM list_exo WHERE `id_account` = %s GROUP BY `name` ', (id,))
        return self.cursor

    def last_id(self):
        self.cursor.execute('SELECT `id_list_exo` FROM list_exo GROUP BY `id_list_exo` ')
        return int(1 if len([i for i in self.cursor]) == 0 else int(max( [int(i['id_list_exo']) for i in self.cursor] ))+1)

    def fetchRequest(self, request):
        return [{"name": request.form["name"], "first_numb": request.form["first_numb__"+str(i)], "second_numb": request.form["second_numb__"+str(i)], "operator": request.form["operator__"+str(i)]} for i in list(set( [int(i.split("__")[1]) for i in request.form if '__' in i] )) ]

    def add(self, request, mysql):
        req = self.fetchRequest(request)
        last_id = self.last_id()
        for r in req:
            self.cursor.execute('INSERT INTO list_exo VALUES (%s, %s, %s, %s, %s, %s)',
                                (last_id, session['id'], r['name'], r['first_numb'], r['second_numb'], r['operator'],))
            mysql.connection.commit()

    def edit(self, request, mysql, id):
        req = self.fetchRequest(request)
        self.cursor.execute("UPDATE list_exo SET `name` = %s, address = %s, zip_code = %s, city = %s WHERE id = %s",
                            (session['id'], req['first_numb'], req['second_numb'], req['operator'],))
        mysql.connection.commit()

    def delete(self, mysql, id):
        self.cursor.execute('DELETE FROM list_exo WHERE `id_list_exo` = %s', (id,))
        mysql.connection.commit()

    # ==================================================================================================================

    def operator(self):
        return {"addition": "+", "soustraction": "-", "multiplication": "*", "division": "/"}

    def list_exo(self, operator):

        def question(question):
            operator = self.operator()[question['operator']]
            # ===========================
            question = str(question['first_numb']) + str(self.operator()[question['operator']]) + str(question['second_numb'])
            result = eval(question)
            bad_r = RandomListExo(None, None, 4).bad_question(operator, result)
            random.shuffle(bad_r)
            return {"question": question, "result": result, "possibility": bad_r, "answer": "null"}

        all_info = [i for i in self.all_info(operator[5:])]
        return {i: question(all_info[i-1]) for i in range(1, len(all_info))}