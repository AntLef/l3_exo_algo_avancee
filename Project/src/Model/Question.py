class Question:

    def __init__(self, question, result, bad_result):
        self.question   = question
        self.result      = result
        self.bad_result = bad_result

    @property
    def getQuestion(self):
        return self.question

    @getQuestion.setter
    def setQuestion(self, a):
        self.question = a

    @property
    def getResult(self):
        return self.result

    @getResult.setter
    def setResult(self, a):
        self.result = a

    @property
    def getBadResult(self):
        return self.bad_result

    @getBadResult.setter
    def setBadResult(self, a):
        self.bad_result = a