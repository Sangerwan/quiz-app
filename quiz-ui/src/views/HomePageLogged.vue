<template>

  <div class="all">
    <div class="right">
      <p>User: {{username}}</p>
      <p>Score: {{score}}</p>
      <button @click="disconnect" class="buttonSimple">Disconnect</button>
    </div>
    <div class="center">  
      <div class="title">
        <h1> {{ welcome_description }}</h1>

        <h3>{{ score_description }}</h3>
      </div>
      
      <div>
        <div>
          <button @click="beginQuiz" class="buttonSimple">Begin quiz !</button>
        </div>

        <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
          {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
        </div>        
      </div>    
    </div>
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
        participationStorageService.disconnect();
        this.$router.push('/');        
      } catch (e) {
        console.log(e)
      }      
    },async beginQuiz() {
      try {        
        this.$router.push('/question-manager');        
      } catch (e) {
        console.log(e)
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
            this.score = 0
            this.score_description="Play your first game now !"
            this.welcome_description="Welcome "+this.username
          }
        }          
      } catch (e) {
        this.$router.push('/');
      }  
  }
};
</script>

<style>

.title{
  display: flex;
  flex-direction: column;
}
.right {
  display: flex;
  justify-content: start;   
  flex-direction: column;
  background-color: goldenrod;
  width: 20%;
}
.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;  
  width: 80%;
  height: 100%;
}

.all{
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
}


</style>
