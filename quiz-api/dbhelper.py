import sqlite3
from ObjectNotExistException import ObjectNotExistException
import question
import answer
class DBHelper:
	def __init__(self):
		#création d'un objet connection

		# set the sqlite connection in "manual transaction mode"
		# (by default, all execute calls are performed in their own transactions, not what we want)
		
		db_connection = None

		try:
			db_connection = sqlite3.connect("./db.db")
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

		
	def deleteQuestion(self,id_question):
		querySel = (
			f"SELECT id FROM questions WHERE id="+id_question
		)
		queryDel = (
			f"DELETE FROM questions WHERE id="+id_question
		)
		curr = self.db_connection.cursor()
		len_select=0
		try :
			curr.execute("begin")
			curr.execute(querySel)
			len_select=len(curr.fetchall())			
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')
			return

		if len_select==0:
			raise ObjectNotExistException() 

		try :
			curr.execute("begin")
			curr.execute(queryDel)
			curr.execute("commit")
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def insertQuestion(self, question: question.Question):
		question_json = question.convertToJson()
		for idx, key in enumerate(question_json):
			if isinstance(question_json[key], str):
				question_json[key] = question_json[key].replace("'", "''")
				

		query = (
			f"INSERT INTO questions (title, text, image, position) VALUES"
			f"('{question_json['title']}', '{question_json['text']}', '{question_json['image']}', '{question_json['position']}')"
		)
		curr = self.db_connection.cursor()
		try :
			curr.execute("begin")
			curr.execute(query)
			curr.execute("commit")
			question.id = curr.lastrowid
		except Exception as e:
			print(e)
			curr.execute('rollback')

	def insertAnswer(self, answer: answer.Answer):
		answer_json = answer.convertToJson()
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


