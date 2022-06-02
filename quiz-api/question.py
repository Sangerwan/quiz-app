
class Question():
	def __init__(self, title: str, text: str, image: str, position: int, id: int = None, possibleAnswers: list = []):
		self.title = title
		self.text = text
		self.image = image
		self.position = position
		self.id = id
		self.possibleAnswers = possibleAnswers

	def convertToJson(self):
		return {
			'title': self.title,
			'text': self.text,
			'image': self.image,
			'position': self.position,
			'possibleAnswers': self.possibleAnswers,
			'id': self.id
		}

	@staticmethod 
	def convertJsonToQuestion(json):
		return Question(json[0], json[1], json[2], json[3], json[4])
