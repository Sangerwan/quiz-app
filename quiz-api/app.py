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
		username="random"
			
	if(payload["password"] == "Vive l'ESIEE !"):
		token = jwt_utils.build_token()
		dbHelper = DBHelper()
		dbHelper.insertPlayer(username)
		return {"token": token}, 200
	return '', 401 

@app.route('/is-logged', methods=['GET'])
def isLogged():
	try:
		token = request.headers.get('Authorization')
		token = token.split(',')[0]
	except AttributeError as e:
		return {"isLogged": False}, 200
	try:
		#check if the token is valid
		if jwt_utils.decode_token(token) == "quiz-app-admin":
			return {"isLogged": True}, 200
		else :
			return {"isLogged": False}, 200
	except jwt_utils.JwtError as e:
			return {"isLogged": False}, 200
	return '', 401 

@app.route('/questions', methods=['POST'])
def SetQuestions():
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
			dbHelper.insertQuestion(question)
			possibleAnswers = payload['possibleAnswers']
			for answer in possibleAnswers:
				answer = Answer(question.id, answer['text'], answer['isCorrect'])
				dbHelper.insertAnswer(answer)
			return '', 200
	except jwt_utils.JwtError as e:
			return e.message, 401


@app.route('/questions/<id>', methods=['DELETE'])
def DeleteQuestions(id):
	try:
		token = request.headers.get('Authorization')
		#token = token.split(' ')[1]
		#token=token
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		#check if the token is valid
		if jwt_utils.decode_token(token) == "quiz-app-admin":

			dbHelper = DBHelper()
			dbHelper.deleteQuestion(id)
			dbHelper.deleteAnswersOfQuestion(id)				
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
		if jwt_utils.decode_token(token) == "quiz-app-admin":

			dbHelper = DBHelper()
			dbHelper.deleteAllParticipations()
			return 'ok deleted', 204
	except jwt_utils.JwtError as e:
			return e.message, 401



@app.route('/participations', methods=['POST'])
def AnswersToQuestion():
	try:
		token = request.headers.get('Authorization')
		#token = token.split(' ')[1]
	except AttributeError as e:
		return 'Wrong Token / Format', 401
	
	try:
		#check if the token is valid
		#if jwt_utils.decode_token(token) == "quiz-app-admin":

			dbHelper = DBHelper()
			payload = request.get_json()
			player_name = payload['playerName']
			answersId = payload['answers']
			
			questionsId = dbHelper.selectAllQuestionsId()
			if (len(questionsId)!=len(answersId)):
				return "Bad request", 400

			#clean old participation
			dbHelper.deleteParticipationsFromName(player_name)

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
				dbHelper.insertParticipation(Participation(player_name,index,isAGoodAnswer))
				index += 1
			dbHelper.setScoreForName(player_name,countPlayer)

			return '', 200
	except jwt_utils.JwtError as e:
			return e.message, 401


if __name__ == "__main__":
    app.run()

    	