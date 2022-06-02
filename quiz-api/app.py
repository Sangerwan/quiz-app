from typing import Dict
from flask import Flask, request
from flask_cors import CORS
from ObjectNotExistException import ObjectNotExistException
import jwt_utils
from question import Question
from answer import Answer
from participation import Participation
from dbhelper import DBHelper
app = Flask(__name__)
CORS(app)

username_mdp = {"admin": "Vive l'ESIEE !"}

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():

	dbHelper = DBHelper()
	scores=dbHelper.selectAllPlayersScore()		
	numberQuestions = len(dbHelper.selectAllQuestionsId())

	return {"size": numberQuestions, "scores": scores}, 200

@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	try :
		username =payload["username"]
	except Exception as e :
		#No username
		username="admin"

	password=payload["password"]
	isNewUser=False
	passwordToFind=""
	try :#check if it's a new user or not
		passwordToFind = username_mdp[username]
	except Exception as e : #New user
		isNewUser=True
	
	if isNewUser :
		username_mdp[username]=password
		passwordToFind = username_mdp[username]
		
	if(password == passwordToFind):
		token = jwt_utils.build_token(username)
		dbHelper = DBHelper()
		if isNewUser :
			dbHelper.insertPlayer(username)
		return {"token": token}, 200
	return '', 401 

@app.route('/is-logged', methods=['GET'])
def isLogged():
	try:
		token = request.headers.get('Authorization')
		token = token.split(' ')[1]
	except AttributeError as e:
		return {"isLogged": False}, 200
	try:
		#check if the token is valid
		payload = request.get_json()
		if jwt_utils.decode_token(token) == payload["username"]:
			return {"isLogged": True}, 200
		else :
			return {"isLogged": False}, 200
	except jwt_utils.JwtError as e:
			return {"isLogged": False}, 200
	return '', 401 

<<<<<<< HEAD
=======
@app.route('/questions', methods=['POST'])
def AddQuestions():
	try:
		token = request.headers.get('Authorization')
		token = token.split(' ')[1]
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		#check if the token is valid
		payload = request.get_json()
		if jwt_utils.decode_token(token) == payload["username"]:

			question = Question(payload['title'], payload['text'], payload['image'], payload['position'])
			dbHelper = DBHelper()

			dbHelper.insertQuestion(question, payload['possibleAnswers'])

			# possibleAnswers = payload['possibleAnswers']

			# for answer in possibleAnswers:
			# 	answer = Answer(question.id, answer['text'], answer['isCorrect'])
			# 	dbHelper.insertAnswer(answer)

			return '', 200
	except jwt_utils.JwtError as e:
			return e.message, 401
>>>>>>> 085171996de268d2e9230d95d6e19b0454a443b2


@app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestions(position):
	try:
		token = request.headers.get('Authorization')
		#token = token.split(' ')[1]
		#token=token
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		#check if the token is valid
		payload = request.get_json()
		if jwt_utils.decode_token(token) == payload["username"]:

			dbHelper = DBHelper()
			dbHelper.deleteQuestion(position)
			dbHelper.deleteAnswersOfQuestion(position)				
			return '', 200
	except jwt_utils.JwtError as e:
		return e.message, 401
	except ObjectNotExistException as e_custom:	
		return e_custom.message, 404
	except Exception as e_base:	
		return e_base.message, 404


@app.route('/participations', methods=['DELETE'])
def DeleteParticipation():
	try:
		token = request.headers.get('Authorization') 
		token = token.split(' ')[1]
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		#check if the token is valid
		payload = request.get_json()
		if jwt_utils.decode_token(token) == payload["username"]:

			dbHelper = DBHelper()
			dbHelper.deleteAllParticipations()
			return 'ok deleted', 204
	except jwt_utils.JwtError as e:
			return e.message, 401



@app.route('/participations', methods=['POST'])
def AnswersToQuestion():
	try:
		token = request.headers.get('Authorization')
		token = token.split(' ')[1]
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		payload = request.get_json()
		username = payload['username']
		answersId = payload['answers']
		#check if the token is valid
		if jwt_utils.decode_token(token) == username:

			dbHelper = DBHelper()
			
			
			questionsId = dbHelper.selectAllQuestionsId()
			if (len(questionsId)!=len(answersId)):
				return "Bad request", 400

			#clean old participation
			dbHelper.deleteParticipationsFromName(username)

			index=0
			countPlayer=0
			for questionId in questionsId:
				answerId = answersId[index]
				indexOfGoodAnswer = dbHelper.getIdGoodAnswerOfQuestion(questionId)
				if  (indexOfGoodAnswer==answerId) :
					isAGoodAnswer = 'True'
					countPlayer+=1
				else :
					isAGoodAnswer = 'False'
				dbHelper.insertParticipation(Participation(username,index,isAGoodAnswer))
				index += 1
			dbHelper.setScoreForName(username,countPlayer)

			return '', 200
	except jwt_utils.JwtError as e:
			return e.message, 401


@app.route('/questions', methods=['POST'])
def AddQuestions():
	try:
		token = request.headers.get('Authorization')
		token = token.split(' ')[1]
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		#check if the token is valid
		if jwt_utils.decode_token(token) == "quiz-app-admin":

			payload = request.get_json()
			question = Question(payload['title'], payload['text'], payload['image'], payload['position'])
			dbHelper = DBHelper()

			dbHelper.insertQuestion(question, payload['possibleAnswers'])

			# possibleAnswers = payload['possibleAnswers']

			# for answer in possibleAnswers:
			# 	answer = Answer(question.id, answer['text'], answer['isCorrect'])
			# 	dbHelper.insertAnswer(answer)

			return '', 200
	except jwt_utils.JwtError as e:
			return e.message, 401




@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):
	print("GetQuestion")
	# try:
	# 	token = request.headers.get('Authorization')
	# 	#token = token.split(' ')[1]
	# 	token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTQwMDUzNzEsImlhdCI6MTY1NDAwMTc3MSwic3ViIjoicXVpei1hcHAtYWRtaW4ifQ.VbuZl12E0bXjI6GEsizjnQIdSesxlnLTF9OlmBFvYN4"
	# except AttributeError as e:
	# 	return 'Wrong Token / Format', 401
	
	# try:
	# 	#check if the token is valid
	# 	if jwt_utils.decode_token(token) == "quiz-app-admin":

	dbHelper = DBHelper()
	question = dbHelper.getQuestion(position)
	ret = question.convertToJson()
	return ret, 200
	# except jwt_utils.JwtError as e:
	# 	return e.message, 401
	# except ObjectNotExistException as e_custom:	
	# 	return e_custom.message, 404
	# except Exception as e_base:	
	# 	return e_base.message, 404

@app.route('/questions/<position>/answers', methods=['GET'])
def getAnswersOfQuestion(position):

	dbHelper = DBHelper()
	answers = dbHelper.getAnswersOfQuestion(position)
	for key in answers:
		answers[key].pop('questionID', None)
		answers[key].pop('isCorrect', None)
	return answers, 200

@app.route('/questions/<position>', methods=['PUT'])
def PutQuestion(position):
	try:
		token = request.headers.get('Authorization')
		token = token.split(' ')[1]
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		#check if the token is valid
		if jwt_utils.decode_token(token) == "quiz-app-admin":

			payload = request.get_json()
			question = Question(payload['title'], payload['text'], payload['image'], payload['position'])
			dbHelper = DBHelper()

			dbHelper.insertQuestion(question, payload['possibleAnswers'])

			# possibleAnswers = payload['possibleAnswers']

			# for answer in possibleAnswers:
			# 	answer = Answer(question.id, answer['text'], answer['isCorrect'])
			# 	dbHelper.insertAnswer(answer)

			return '', 200
	except jwt_utils.JwtError as e:
			return e.message, 401



if __name__ == "__main__":
    app.run()

    	