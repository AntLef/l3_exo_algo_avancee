import random

from project.src.Model.Question import Question


class RandomListExo:

    def __init__(self, nb_question, operator, nb_possibility=3):
        self.nb_question = nb_question
        self.operator = operator
        self.nb_possibility = nb_possibility

    def list_exo(self):
        return {i: self.question() for i in range(1, self.nb_question+1)}

    def bad_question(self, operator, result):
        list = [result]
        while len(list) < int(self.nb_possibility):
            r = eval(str(random.choice(range(1, 11))) + str(operator[0]) + str(random.choice(range(1, 11))))
            if r not in list and r != result:
                list.append(r)
            else:
                pass
        return list

    def getOperator(self):
        if self.operator:
            return [self.operator, [i for i in ["+", "-", "/", "*"] if i != self.operator]]
        else:
            op = random.choice(["+", "-", "/", "*"])
            return [op, [i for i in ["+", "-", "/", "*"] if i != op]]

    def question(self):

        operator = self.getOperator()
        # ===========================
        int_1 = random.choice(range(1, 11))
        int_2 = random.choice(range(1, 11))
        # ===========================
        question = str(int_1) + str(operator[0]) + str(int_2)
        result = eval(question)
        bad_r = self.bad_question(operator, result)
        random.shuffle(bad_r)
        # ===========================
        # Object question, but not serializable
            # return Question(question, result, bad_r)
        return {"question": question, "result": result, "possibility": bad_r, "answer": "null"}