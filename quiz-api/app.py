from flask import Flask, request
import jwt_utils
from question import Question
from answer import Answer
from dbhelper import DBHelper
app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	if(payload["password"] == "Vive l'ESIEE !"):
		token = jwt_utils.build_token()
		return {"token": token}, 200
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

if __name__ == "__main__":
    app.run(ssl_context='adhoc')
    	