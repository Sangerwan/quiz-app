import json
class Answer():
	def __init__(self, questionID: int, text:str, isCorrect: bool, id: int = None):
		self.id = id
		self.text = text
		self.isCorrect = isCorrect
		self.questionID = questionID

	def convertToJson(self):
		return {
			'id': self.id,
			'text': self.text,
			'isCorrect': self.isCorrect,
			'questionID': self.questionID,
		}

	@staticmethod 
	def convertJsonToAnswer(json):
		return Answer(json[0], json[1], True if json[2] == 'True' else False,json[3])

	@staticmethod
	def convertListOfAnswersToJson(answers: list):
		ret = []
		for answer in answers:
			ret.append(Answer.convertJsonToAnswer(answer).convertToJson())

		return ret
		
