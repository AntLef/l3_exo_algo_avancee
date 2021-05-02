import time

from flask import session

from project.src.Table.Exercise.AnswerTable import AnswerTable
from project.src.Table.Exercise.Generate_List_Exo.RandomListExo import RandomListExo
from project.src.Table.Exercise.ListExoTable import ListExoTable


class ExerciseTable:

    def __init__(self, cursor, mysql):
        self.cursor = cursor
        self.mysql = mysql

    def exo_title(self, id):
        self.cursor.execute('SELECT `name` FROM list_exo WHERE `id_list_exo` = %s GROUP BY `name` LIMIT 1', (id,))
        toto = self.cursor.fetchone()['name']
        return toto

    def getResultQuestion(self, result, id):
        session['list_exo'][str(id)]['answer'] = str(result)

    def place(self, operator, pos, title, request):

        if request.method == 'POST' and 'answer' in request.form:
            session['list_exo'][str(int(str(pos).split("-")[0])-1) if str(pos) != "résultat" else str(len(session['list_exo']))]['answer'] = str(request.form['answer'])
            session['list_exo'] = session['list_exo']

        if str(pos) == "début":
            session['list_exo'] = RandomListExo(10, ListExoTable(None).operator()[operator], 4).list_exo() if operator in ListExoTable(None).operator().keys() else ListExoTable(self.cursor).list_exo(operator)
            return "1-"+str(len(session['list_exo']))

        elif str(pos) in [str(str(i)+"-"+str(len(session['list_exo']))) for i in range(1, len(session['list_exo'])+1)]:

            if str(pos) == "1-"+str(len(session['list_exo'])):
                session['time'] = time.time()
            if str(pos).split("-")[0] == str(len(session['list_exo'])):
                return {"var": session['list_exo'][str(pos).split("-")[0]], "f_pos": "résultat", "i": str(pos).split("-")[0]}
            else:
                return {"var": session['list_exo'][str(pos).split("-")[0]], "f_pos": str(int(str(pos).split("-")[0])+1)+"-"+str(len(session['list_exo'])), "i": str(pos).split("-")[0]}

        elif str(pos) == "résultat":
            duration = time.time() - session['time']
            result = AnswerTable(self.cursor).resultTraining()
            AnswerTable(self.cursor).addResultTrainingInBDD(self.mysql, result, title, time.strftime("%H:%M:%S", time.gmtime(duration)))

            def format_time(timing, val):
                return str(timing) + val

            time_result = format_time(time.strftime("%H:%M:%S", time.gmtime(duration)), ' heure') if duration >= 3600 else format_time(time.strftime("%M:%S", time.gmtime(duration)), ' minute') if 60 < duration < 3600 else format_time(time.strftime("%S", time.gmtime(duration)), ' seconde')
            session.pop('list_exo')
            return "temps : " + str( time_result ) + " - résultat : " + result