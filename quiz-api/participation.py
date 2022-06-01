

class Participation():
	def __init__(self, player_name: int, id_question: int, isAGoodAnswer: str):
		self.player_name = player_name
		self.id_question = id_question
		self.isAGoodAnswer = isAGoodAnswer

	def convertToJson(self):
		return {
			'player_name': self.player_name,
			'id_question': self.id_question,
			'isAGoodAnswer': self.isAGoodAnswer
		}
