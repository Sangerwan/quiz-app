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


    ###
    # QUESTIONS
    ###

    def insert_question(self, question: question.Question, answers: list):
        question_json = question.convertToJson()
        for idx, key in enumerate(question_json):
            if isinstance(question_json[key], str):
                question_json[key] = question_json[key].replace("'", "''")                

        position = question_json['position']

        if self.get_question(position):
            self.increase_question_position_from_position(position)

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
            self.insert_answer_json(answer)

    def get_question(self, position):
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
        questionWithAnswers.possibleAnswers = self.get_answer(questionWithAnswers.id)

        return questionWithAnswers
    
    def delete_question(self,position):
        querySel = (
            f"SELECT id FROM questions WHERE position={position}"
        )

        curr = self.db_connection.cursor()
        try :
            curr.execute("begin")
            curr.execute(querySel)
            id=curr.fetchone()		
            curr.execute("commit")
        except Exception as e:
            print(e)
            curr.execute('rollback')
            return

        if id is None:
            raise ObjectNotExistException

        id = id[0]
        
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
            return


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
            return

        self.decrease_question_position_from_position(position)          

    def update_question(self, new_position :int ,question: question.Question, answers: list):
        
        questionID = self.get_question_id(question.position)
        if questionID is None:
            raise ObjectNotExistException("Question not found")
            
        old_position = question.position
        if new_position > old_position:
            self.decrease_question_position(old_position, new_position)
        else:
            self.increase_question_position(new_position, old_position)
        
        question_json = question.convertToJson()
        for idx, key in enumerate(question_json):
            if isinstance(question_json[key], str):
                question_json[key] = question_json[key].replace("'", "''")

        query = (
            f"UPDATE questions SET "
            f"title='{question_json['title']}', text='{question_json['text']}', image='{question_json['image']}', position={new_position} "
            f"WHERE id={questionID}"
        )
        try:
            curr = self.db_connection.cursor()
            curr.execute("begin")
            curr.execute(query)
            curr.execute("commit")
        except Exception as e:
            print(e)
            curr.execute('rollback')

        self.delete_answer(questionID)

        for answer in answers:
            answer['questionID'] = questionID
            self.insert_answer_json(answer)

    def get_question_count(self):
        query = (
            f"SELECT id FROM questions"
        )
        curr = self.db_connection.cursor()
        try:
            questionsID=[]
            curr.execute("begin")
            curr.execute(query)
            questionsID = curr.fetchall()
            curr.execute("commit")
            if questionsID is None:
                return 0
            return len(questionsID)

        except Exception as e:
            print(e)
            curr.execute('rollback')
            return 0
        
    def get_questions_id(self):
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

    def get_question_id(self, position):
        query = (
            f"SELECT id FROM questions WHERE position={position}"
        )
        curr = self.db_connection.cursor()
        try:
            curr.execute("begin")
            curr.execute(query)
            question_id = curr.fetchone()
            if question_id is None:
                return None
            question_id = question_id[0]
            curr.execute("commit")
            return question_id

        except Exception as e:
            print(e)
            curr.execute('rollback')

    def increase_question_position_from_position(self, position):
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

    def increase_question_position(self, start_position, end_position):
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
            
    def decrease_question_position_from_position(self, position):
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

    def decrease_question_position(self, start_position, end_position):
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



    ###
    # ANSWERS
    ### 

    def insert_answer_json(self, answer_json: dict):
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
            
    def get_answer(self, id):
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
            
    def delete_answer(self,id_question):
        query = (
            f"DELETE FROM answers WHERE questionID="+str(id_question)
        )
        curr = self.db_connection.cursor()
        try :
            curr.execute("begin")
            curr.execute(query)
            curr.execute("commit")
        except Exception as e:
            print(e)
            curr.execute('rollback')
        
    def get_correct_answer_index(self, id_question):
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

        
    ###
    # SCORE
    ###

    def set_score(self, player_name,score):
        query = (
            f"UPDATE PLAYERS SET Score={score} WHERE Name='{player_name}'"
        )
        curr = self.db_connection.cursor()
        try :
            curr.execute("begin")
            curr.execute(query)
            curr.execute("commit")
        except Exception as e:
            print(e)
            curr.execute('rollback')

    def get_score(self, player_name):
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

    ###
    # PARTICIPATION
    ###
            
    def add_participation(self, participation: participation.Participation):
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
    
    def get_participations(self, player_name):
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

    def delete_participation(self, player_name):
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

    def delete_participations(self):
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

        query = (
            f"DELETE FROM PLAYERS"
        )

        try:
            curr.execute("begin")
            curr.execute(query)
            curr.execute("commit")
        except Exception as e:
            print(e)
            curr.execute('rollback')
            

    ###
    # PLAYER
    ###

    def add_player(self,username, password):				
        query = (
            f"INSERT INTO PLAYERS (Name,Score,Password) VALUES"
            f"('{username}','-1', '{password}')"
        )
        curr = self.db_connection.cursor()
        try :
            curr.execute("begin")
            curr.execute(query)
            curr.execute("commit")
        except Exception as e:
            print(e)
            curr.execute('rollback')
    
    def get_player_password_hash(self, username):
        query = (
            f"SELECT Password FROM PLAYERS WHERE Name='{username}'"
        )
        curr = self.db_connection.cursor()
        try :
            curr.execute("begin")
            curr.execute(query)
            password = curr.fetchone()
            curr.execute("commit")
            if password is None:
                return None
            password = password[0]
            
            return password
        except Exception as e:
            print(e)
            curr.execute('rollback')
            return None

    def get_players_name(self):
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

    def get_players_score(self):
        query = (
            f"SELECT Name, Score FROM PLAYERS WHERE Score>=0 ORDER BY Score DESC"
        )
        curr = self.db_connection.cursor()
        try :
            result = []
            curr.execute("begin")
            curr.execute(query)
            for (player_name, score) in curr :
                result.append({'playerName':player_name, 'score':score})
            curr.execute("commit")
            return result

        except Exception as e:
            print(e)
            curr.execute('rollback')
            return []
