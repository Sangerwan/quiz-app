import sqlite3
from ObjectNotExistException import ObjectNotExistException
import question
import answer
import participation
import json
class DBHelper:
	def __init__(self):
		#création d'un objet connection

		# set the sqlite connection in "manual transaction mode"
		# (by default, all execute calls are performed in their own transactions, not what we want)
		
		db_connection = None

		try:
			db_connection = sqlite3.connect("./quiz-api/db.db")
			db_connection.isolation_level = None
		except Exception as e:
			print(e)

		self.db_connection = db_connection

	def deleteAnswersOfQuestion(self,id_question):
		query = (
			f"DELETE FROM answers WHERE questionID="+id_question
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			print(curr.execute(query))
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
		
	def deleteQuestion(self,position):
		id=-1
		querySel = (
			f"SELECT id FROM questions WHERE position={position}"
		)

		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(querySel)
			id=curr.fetchone()[0]		
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
			return

		if id==-1:
			raise ObjectNotExistException() 

		queryDel = (
			f"DELETE FROM questions WHERE id={id}"
		)
		try :
			curr.execute("begin")
			curr.execute(queryDel)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

		self.decreaseQuestionPositionFromPosition(position)

		queryDelAnswer = (
			f"DELETE FROM answers WHERE questionID={id}"
		)
		
		try :
			curr.execute("begin")
			curr.execute(queryDelAnswer)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

		


	def insertQuestion(self, question: question.Question, answers: list):
		question_json = question.convertToJson()
		for idx, key in enumerate(question_json):
			if isinstance(question_json[key], str):
				question_json[key] = question_json[key].replace("'", "''")
				

		position = question_json['position']

		if self.getQuestion(position):
			self.increaseQuestionPositionFromPosition(position)

		query = (
			f"SELECT max(position) from questions"
		)
		
		try:
			curr = self.db_connection.cursor()
			curr.execute("begin")
			curr.execute(query)
			max_position = curr.fetchone()[0]
			curr.execute("commit")
			if max_position is None:
				max_position = 0
			else:
				if question_json['position'] > max_position+1:
					question_json['position'] = max_position
		except Exception as e:
			print(e)
			curr.execute('rollback')





		query = (
			f"INSERT INTO questions (title, text, image, position) VALUES"
			f"('{question_json['title']}', '{question_json['text']}', '{question_json['image']}', '{question_json['position']}')"
		)

		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			question.id = curr.lastrowid
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

		for answer in answers:
			answer['questionID'] = question.id
			self.insertAnswerJson(answer)
		

	def insertAnswerJson(self, answer_json: dict):
		for idx, key in enumerate(answer_json):
			if isinstance(answer_json[key], str):
				answer_json[key] = answer_json[key].replace("'", "''")

		query = (
			f"INSERT INTO answers (questionID, text, isCorrect) VALUES"
			f"('{answer_json['questionID']}', '{answer_json['text']}', '{answer_json['isCorrect']}')"
		)

		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def getIdGoodAnswerOfQuestion(self, id_question):
		query = (
			f"SELECT isCorrect FROM ANSWERS where questionID="+str(id_question)
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			index=1
			result = -1
			for (isCorrect) in curr :
				if (isCorrect[0]=='True'):
					result=index
					break				
				index+=1
			
			curr.execute("commit")
			return result

		except Exception as e:
			print(e)
			curr.execute('rollback')
			return -1

	def getScoreForName(self, player_name):
		query = (
			f"Select Score FROM PLAYERS WHERE Name='"+player_name + "'"
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			for (Score) in curr :
				result=Score[0]
			curr.execute("commit")
			return result
		except Exception as e:
			print(e)
			curr.execute('rollback')
			return -1

	def setScoreForName(self, player_name,score):
		query = (
			f"UPDATE PLAYERS SET Score='"+str(score)+"' WHERE Name='"+player_name + "'"
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

			
	def getQuestion(self, position):
		query = (
			f"SELECT * FROM questions WHERE position="+str(position)
		)
		curr = self.db_connection.cursor()
		question_json = None
		try:
			curr.execute("begin")
			curr.execute(query)
			question_json = curr.fetchone()
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
		if question_json is None:
			raise ObjectNotExistException
		return question_json

	def deleteParticipationsFromName(self, player_name):
		query = (
			f"DELETE FROM PARTICIPATIONS where player_name='"+player_name+"'"
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def deleteAllParticipations(self):
		query = (
			f"DELETE FROM PARTICIPATIONS"
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')


	def selectParticipationsFromName(self, player_name):
		query = (
			f"SELECT id FROM PARTICIPATIONS where player_name="+player_name
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			result=curr[0][0]
			curr.execute("commit")
			return result

		except Exception as e:
			print(e)
			curr.execute('rollback')
			return -1

	def selectAllQuestionsId(self):
		query = (
			f"SELECT id FROM questions"
		)
		curr = self.db_connection.cursor()
		try :
			result =[]
			curr.execute("begin")
			curr.execute(query)
			for (id) in curr :
				result.append(id[0])
			curr.execute("commit")
			return result

		except Exception as e:
			print(e)
			curr.execute('rollback')
			return []

	def selectAllPlayersName(self):
		query = (
			f"SELECT player_name FROM PLAYERS"
		)
		curr = self.db_connection.cursor()
		try :
			result = []
			curr.execute("begin")
			curr.execute(query)
			for (player_name) in curr :
				result.append(player_name[0])
			curr.execute("commit")
			return result

		except Exception as e:
			print(e)
			curr.execute('rollback')
			return []

	def selectAllPlayersScore(self):
		query = (
			f"SELECT Score FROM PLAYERS"
		)
		curr = self.db_connection.cursor()
		try :
			result = []
			curr.execute("begin")
			curr.execute(query)
			for (Score) in curr :
				result.append(Score[0])
			curr.execute("commit")
			return result

		except Exception as e:
			print(e)
			curr.execute('rollback')
			return []

	def insertPlayer(self,username):				
		query = (
			f"INSERT INTO PLAYERS (Name,Score) VALUES"
			f"('{username}','-1')"
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')


	def insertParticipation(self, participation: participation.Participation):
		question_json = participation.convertToJson()
		for idx, key in enumerate(question_json):
			if isinstance(question_json[key], str):
				question_json[key] = question_json[key].replace("'", "''")
				
		query = (
			f"INSERT INTO PARTICIPATIONS (player_name, answer_id, good_answer) VALUES"
			f"('{question_json['player_name']}', '{question_json['id_question']}', '{question_json['isAGoodAnswer']}')"
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def getQuestion(self, position):
		query = (
			f"SELECT * FROM questions WHERE position="+str(position)
		)
		curr = self.db_connection.cursor()
		question_json = None
		try:
			curr.execute("begin")
			curr.execute(query)
			question_json = curr.fetchone()
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
		
		if question_json is None:
			return None

		questionWithAnswers = question.Question.convertJsonToQuestion(question_json)
		questionWithAnswers.possibleAnswers = self.getAnswersOfQuestion(questionWithAnswers.id)

		return questionWithAnswers

	def getAnswersOfQuestion(self, id):
		query = (
			f"SELECT * FROM answers WHERE questionID="+str(id)
		)
		curr = self.db_connection.cursor()
		try:
			curr.execute("begin")
			curr.execute(query)
			answers_list = curr.fetchall()
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

		if answers_list is None:
			return None
		return answer.Answer.convertListOfAnswersToJson(answers_list)

	def increaseQuestionPositionFromPosition(self, position):
		query = (
			f"UPDATE questions SET position=position+1 WHERE position>="+str(position)
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
	def increaseQuestionPosition(self, start_position, end_position):
		query = (
			f"UPDATE questions SET position=position+1 WHERE position>="+str(start_position)+" AND position<"+str(end_position)
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def getQuestion(self, position):
		query = (
			f"SELECT * FROM questions WHERE position="+str(position)
		)
		curr = self.db_connection.cursor()
		question_json = None
		try:
			curr.execute("begin")
			curr.execute(query)
			question_json = curr.fetchone()
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
		
		if question_json is None:
			return None

		questionWithAnswers = question.Question.convertJsonToQuestion(question_json)
		questionWithAnswers.possibleAnswers = self.getAnswersOfQuestion(questionWithAnswers.id)

		return questionWithAnswers

	def decreaseQuestionPosition(self, start_position, end_position):
		query = (
			f"UPDATE questions SET position=position-1 WHERE position>"+str(start_position)+" AND position<="+str(end_position)
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def decreaseQuestionPositionFromPosition(self, position):
		query = (
			f"UPDATE questions SET position=position-1 WHERE position>="+str(position)
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def UpdateQuestion(self, new_position :int ,question: question.Question):
		questionID = self.getQuestionID(question)
		old_position = question.position
		if new_position > old_position:
			self.decreaseQuestionPosition(old_position, new_position)
		else:
			self.increaseQuestionPosition(new_position, old_position)
		
		query = (
			f"UPDATE questions SET position={new_position} WHERE id={questionID}"
		)
		try:
			curr = self.db_connection.cursor()
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def getQuestionID(self, question: question.Question):
		question_json = question.convertToJson()
		for idx, key in enumerate(question_json):
			if isinstance(question_json[key], str):
				question_json[key] = question_json[key].replace("'", "''")
		query = (
			f"SELECT id FROM questions WHERE position={question_json['position']} AND text='{question_json['text']}' AND title='{question_json['title']}' AND image='{question_json['image']}'"
		)
		curr = self.db_connection.cursor()
		question_id = -1
		try :
			curr.execute("begin")
			curr.execute(query)
			question_id = curr.fetchone()[0]
			question.id = question_id
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
		return question_id
