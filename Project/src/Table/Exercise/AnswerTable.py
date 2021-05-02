from flask import session


class AnswerTable:

    def __init__(self, cursor):
        self.cursor = cursor

    def addResultTrainingInBDD(self, mysql, result, operator, duration, list_prof=None):
        self.cursor.execute('INSERT INTO result_exo VALUES (NULL, %s, %s, %s, %s, %s, %s)',
                            (session['id'], int(result.split("-")[0]), int(result.split("-")[1]), operator,  duration, list_prof))
        mysql.connection.commit()

    def resultTraining(self):
        return str(len([i for i in range(1, len(session['list_exo'])+1) if str(session['list_exo'][str(i)]["result"]) == str(session['list_exo'][str(i)]["answer"])])) + "-" + str(len(session['list_exo']))

    def answerTable(self):
        self.cursor.execute('SELECT ROUND(r_e.nunb_good_resp * 100.0 / r_e.numb_questions) AS percent, '
                            'SEC_TO_TIME(ROUND(TIME_TO_SEC(r_e.duration) / r_e.numb_questions)) AS time_by_resp, '
                            'CONCAT(UCASE(LEFT(r_e.operator, 1)), LCASE(SUBSTRING(r_e.operator, 2))) AS operator, r_e.duration, '
                            'CONCAT(UCASE(LEFT(a.firstname, 1)), LCASE(SUBSTRING(a.firstname, 2))) AS firstname, UCASE(a.surname) AS surname '
                            'FROM `result_exo` AS r_e '
                            'INNER JOIN `account` AS a ON a.`id` = r_e.`id_account` '
                            'ORDER BY `percent` DESC, `time_by_resp` ASC LIMIT 10')
        val = [i for i in self.cursor]
        return {i+1: val[i] for i in range(0, len(val))}
