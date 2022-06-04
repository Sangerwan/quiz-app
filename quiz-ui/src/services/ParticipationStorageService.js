import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  saveToken(token){
    window.localStorage.setItem("token", token);
  },
  getToken(){
    return window.localStorage.getItem("token");
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
    return window.localStorage.getItem("participationScore");
  },
  disconnect() {
    window.localStorage.removeItem("playerName");
    window.localStorage.removeItem("token");
    window.localStorage.removeItem("participationScore");
  }
};
