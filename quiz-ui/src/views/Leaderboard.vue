<template>
  <div class="head">
    <h1>Leaderboard</h1>
  </div>
  <div class="body"> 

      <h1>Leaderboard</h1>
      <ul v-for="score in QuizInfo.scores">
        {{score.playerName}} - {{score.score}}
      </ul>
      
  </div>
</template>



<script>
import quizApiService from "@/services/quizApiService";

export default {
  components: {
  },
  name: "Leaderboard",
  data() {
    return {//rertourne des données réactives
      QuizInfo: [],
    };
  },
  async created() {
    try{
      const quizInfo = await quizApiService.getQuizInfo()
      if(quizInfo && quizInfo.data)
        this.QuizInfo = quizInfo.data
    }
    catch(e){
      console.log(e)
    }
  },
  methods: {
  }
};
</script>

<style>

.buttonQuestion{
  width: 100%;
  padding: 0%;
  border-color: black;
}

.question{
  display: flex;
  flex-direction: column;
  background-color: bisque;
}

.incorrect{
  background-color: rgba(255, 0, 0, 0.5);
}

.correct{
  background-color: rgba(0, 128, 0, 0.5);
}

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
