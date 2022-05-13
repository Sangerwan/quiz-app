
class Answer():
	def __init__(self, questionID: int, text:str, isCorrect: bool):
		self.questionID = questionID
		self.text = text
		self.isCorrect = isCorrect

	def convertToJson(self):
		return {
			'questionID': self.questionID,
			'text': self.text,
			'isCorrect': self.isCorrect
		}

	@staticmethod 
	def convertJsonToAnswer(json):
		return Answer(json['questionID'], json['text'], json['isCorrect'])
