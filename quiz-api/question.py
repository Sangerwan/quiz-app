
class Question():
	def __init__(self, title: str, text: str, image: str, position: int, id: int = None):
		self.title = title
		self.text = text
		self.image = image
		self.position = position
		self.id = id

	def convertToJson(self):
		return {
			'title': self.title,
			'text': self.text,
			'image': self.image,
			'position': self.position,
			'id': self.id
		}

	@staticmethod 
	def convertJsonToQuestion(json):
		return Question(json['title'], json['text'], json['image'], json['position'], json['id'])
