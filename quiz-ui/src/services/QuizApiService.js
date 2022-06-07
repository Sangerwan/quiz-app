import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    return this.call("get", `questions/${position}`);
  },
  getQuestions() {
    return this.call("get", "questions");
  },
  updateQuestion(id, data, token) {
    return this.call("put", `/questions/${id}`, data, token);
  },
  deleteQuestion(id, token) {
    return this.call("delete", `/questions/${id}`, null, token);
  },
  getAnswersOfQuestion(id) {
    return this.call("get", `questions/${id}/answers`);
  },
  login(passwordTest,username) {
    return this.call("post","login", {password : passwordTest, username : username});
  },
  isLogged(username,token){
    return this.call("get",`is-logged/${username}`,null,token);
  },
  setParticipation(username,answers, token){
    return this.call("post","participations",{username : username, answers : answers},token)
  },
  getLastScore(username,token){
    return this.call("get",`get-last-score/${username}`,null,token)
  },
  getBestScore(username,token){
    return this.call("get",`get-best-score/${username}`,null,token)
  },
  getQuestionCount(){
    return this.call("get", `questions-count`);
  },
  addQuestion(data, token){
    return this.call("post", "questions", data, token);
  }

};