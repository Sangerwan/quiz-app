import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
      "Authorization" : token
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
  getAnswersOfQuestion(id) {
    return this.call("get", `questions/${id}/answers`);
  },
  login(passwordTest,username) {
    return this.call("post","login", {password : passwordTest, username : username});
  },
  isLogged(token){
    return this.call("get","is-logged",{},token);
  },
  setParticipation(playerName,answers, token){
    return this.call("post","participations",{playerName : playerName, answers : answers}, null,token)
  }

};