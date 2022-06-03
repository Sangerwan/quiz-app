import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
      "Authorization" : ""
    };
    if (token != null) {
      headers.authorization = token;
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
  getAnswersOfQuestion(id) {
    return this.call("get", `questions/${id}/answers`);
  },
  login(passwordTest,username) {
    return this.call("post","login", {password : passwordTest, username : username});
  },
  isLogged(username,token){
    if (username==""){
      return {"isLogged": False}, 200
    }
    return this.call("get",`is-logged/${username}`,null,token);
  },
  setParticipation(username,answers, token){
    return this.call("post","participations",{username : username, answers : answers},token)
  },
  getScoreOfUser(username,token){
    return this.call("get",`get-score/${username}`,null,token)
  },
  getQuestionCount(){
    return this.call("get", `questions-count`);
  }

};