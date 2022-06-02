<template>
  <h1> {{ welcome_description }}</h1>

  <h3>{{ score_description }}</h3>
  <div>
    <div>
      <router-link to="/question-manager">Begin quiz !</router-link>
    </div>

    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>

    <button @click="disconnect" class="buttonSimple">Disconnect</button>

  </div>
  
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "HomePageLogged",
  data() {
    return {//rertourne des données réactives
      registeredScores : [],
      username : "",
      score :-1,
      score_description : "",
      welcome_description : ""
    };
  },
  methods: {
    async disconnect() {
      try {        
        participationStorageService.saveToken("");
        participationStorageService.savePlayerName(this.username);
        this.$router.push('/');        
      } catch (e) {

      }
      
    },
  },
  async created() {
    const instance = await quizApiService.getQuizInfo();   
     try {       
        const response =  await quizApiService.isLogged(
          participationStorageService.getPlayerName(),
          participationStorageService.getToken());
        if (!response.data.isLogged) {
          this.$router.push('/');
        }else{
          this.username=participationStorageService.getPlayerName();
          const result = await quizApiService.getScoreOfUser(this.username,participationStorageService.getToken())
          this.score = result.data.score
          if (this.score!=-1){
            this.score_description="Your last score was "+this.score
            this.welcome_description="Welcome back "+this.username+" !"
          } else{
            this.score_description="Play your first game now !"
            this.welcome_description="Welcome "+this.username+" !"
          }
        }          
      } catch (e) {
        this.$router.push('/');
      }  
  }
};
</script>

<style>
</style>
