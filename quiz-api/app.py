from msilib.schema import Error
from typing import Dict
from flask import Flask, request
from flask_cors import CORS
from ObjectNotExistException import ObjectNotExistException
import jwt_utils
from question import Question
from answer import Answer
from dbhelper import DBHelper
import bcrypt
app = Flask(__name__)
CORS(app)

username_mdp = {"admin": "Vive l'ESIEE !"}

###
# AUTHENTICATION
###

def check_token(token):
    try:
        token = token.split()
        if token[0] == "Bearer":
            token = token[1]
        return token
    except Exception as e:
        return e

@app.route('/login', methods=['POST'])
def login():
    try:
        payload = request.get_json()
        username = payload["username"]
        
        dbHelper = DBHelper()
    
        new_user = False

        password_hash = dbHelper.get_player_password_hash(username)
        if password_hash is None:
            new_user = True
        else:
            password_hash = password_hash.encode()
        password = payload["password"]
        
        if new_user:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            dbHelper.add_player(username, password_hash.decode())

        if bcrypt.checkpw(password.encode(), password_hash):
            token = jwt_utils.build_token(username)
            return {"token": token}, 200
    except Exception as e:
        return '', 401
    return '', 401

@app.route('/is-logged/<username>', methods=['GET'])
def is_logged(username):
    if username == 'null':
        return {"isLogged": False}, 401
    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
    except AttributeError as e:
        return {"isLogged": False}, 401
    try:
        # check if the token is valid
        if jwt_utils.decode_token(token) == username:
            return {"isLogged": True}, 200
        else:
            return {"isLogged": False}, 401
    except jwt_utils.JwtError as e:
        return {"isLogged": False}, 401
    except Exception as e:
        return '', 401


###
# QUESTIONS
###

@app.route('/questions', methods=['POST'])
def add_question():
    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
        # check if the token is valid
        payload = request.get_json()
        if jwt_utils.decode_token(token) == "admin":

            question = Question(
                payload['title'], payload['text'], payload['image'], payload['position'])

            dbHelper = DBHelper()
            dbHelper.insert_question(question, payload['possibleAnswers'])
            return '', 200
        else:
            return '', 401
    except jwt_utils.JwtError as e:
        return e.message, 401

@app.route('/questions/<position>', methods=['GET'])
def get_question(position):
    try:
        dbHelper = DBHelper()
        question = dbHelper.get_question(position)

        if question is None:
            return '', 404

        ret = question.convertToJson()
        return ret, 200

    except ObjectNotExistException as e_custom:
        return e_custom.message, 404
    except Exception as e_base:
        return e_base.message, 404

@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        dbHelper = DBHelper()
        questions = dbHelper.get_questions()

        if questions is None:
            return '', 404
        return {"questions": questions}, 200

    except ObjectNotExistException as e_custom:
        return e_custom.message, 404
    except Exception as e_base:
        return e_base.message, 404

@app.route('/questions/<position>', methods=['DELETE'])
def delete_quetion(position):

    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
        if jwt_utils.decode_token(token) == "admin":

            dbHelper = DBHelper()
            dbHelper.delete_question(int(position))
            return '', 204
        else:
            return '', 401
    except jwt_utils.JwtError as e:
        return e.message, 401
    except ObjectNotExistException as e_custom:
        return e_custom.message, 404
    except Exception as e_base:
        return e_base.message, 404

@app.route('/questions/<position>', methods=['PUT'])
def update_question(position):
    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
        # check if the token is valid
        if jwt_utils.decode_token(token) == "admin":

            payload = request.get_json()
            new_position = int(payload['position'])
            question = Question(
                payload['title'], payload['text'], payload['image'], int(position))
            dbHelper = DBHelper()

            dbHelper.update_question(
                new_position, question, payload['possibleAnswers'])

            return '', 200
        else:
            return '', 401
    except ObjectNotExistException as e_custom:
        return e_custom.message, 404
    except jwt_utils.JwtError as e:
        return e.message, 401


###
# PARTICIPATIONS
###

@app.route('/participations', methods=['POST'])
def set_participation():
    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
        payload = request.get_json()
        username = payload['username']
        answersId = payload['answers']
        # check if the token is valid

        if jwt_utils.decode_token(token) == username:

            dbHelper = DBHelper()

            question_count = dbHelper.get_question_count()

            if (question_count != len(answersId)):
                return "Bad request", 400

            correct_participation = dbHelper.get_correct_participation()
            if correct_participation is None:
                return "Bad request", 400
                
            score = 0

            for i in range(question_count):
                if correct_participation[i] == answersId[i]:
                    score += 1

            dbHelper.set_score(username, score)

            result = {"username": username, "score": score}

            return result, 200
        else:
            return '', 401
    except jwt_utils.JwtError as e:
        return e.message, 401

@app.route('/participations', methods=['DELETE'])
def delete_participations():

    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
        if jwt_utils.decode_token(token) == "admin":

            dbHelper = DBHelper()
            dbHelper.delete_participations()
            return 'ok deleted', 204
        else:
            return '', 401

    except jwt_utils.JwtError as e:
        return e.message, 401
    except Exception as e:
        return e.message, 401


###
# GET INFO
###

@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    try:
        dbHelper = DBHelper()
        scores = dbHelper.get_players_score()
        numberQuestions = dbHelper.get_question_count()

        return {"size": numberQuestions, "scores": scores}, 200
    except Exception as e:
        return e.message, 401

@app.route('/questions-count', methods=['GET'])
def get_question_count():
    try:
        dbHelper = DBHelper()
        count = dbHelper.get_question_count()
        return {"count": count}, 200
    except Exception as e:
        return e.message, 401

@app.route('/get-last-score/<username>', methods=['GET'])
def get_last_score(username):

    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
        if jwt_utils.decode_token(token) == username:
            dbHelper = DBHelper()
            score = dbHelper.get_last_score(username)
            if score == -1:
                return '', 404
            return {"score": score}, 200
        else:
            return '', 401
    except jwt_utils.JwtError as e:
        return e.message, 401
    except Exception as e:
        return e.message, 401

@app.route('/get-best-score/<username>', methods=['GET'])
def get_best_score(username):
    try:
        token = request.headers.get('Authorization')
        token = check_token(token)
        if jwt_utils.decode_token(token) == username:
            dbHelper = DBHelper()
            score = dbHelper.get_best_score(username)
            if score == -1:
                return '', 404
            return {"score": score}, 200
        else:
            return '', 401
    except jwt_utils.JwtError as e:
        return e.message, 401
    except Exception as e:
        return e.message, 401

@app.route('/questions/<position>/answers', methods=['GET'])
def get_answer(position):
    try:
        dbHelper = DBHelper()
        answers = dbHelper.get_answer(position)
        if answers is None:
            return '', 404
            
        for key in answers:
            answers[key].pop('questionID', None)
            answers[key].pop('isCorrect', None)
        return {"answers", answers}, 200
    except Exception as e:
        return e.message, 401
    
if __name__ == "__main__":
    app.run()
