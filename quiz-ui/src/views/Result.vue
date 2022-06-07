<template>
  <h1>Result: {{nbGoodAnswers}} / {{nbQuestions}}</h1>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import ParticipationStorageService from "../services/ParticipationStorageService";

export default {
  data() {
    return {
      nbGoodAnswers: 0,
      nbQuestions: 0
    };
  },
  async created() {
    console.log("created");
    try {       
        const score =  await quizApiService.getLastScore(
          ParticipationStorageService.getPlayerName(),
          ParticipationStorageService.getToken());
        if (score && score.data) 
          this.nbGoodAnswers = score.data.score
        else 
          this.$router.push('/');
    } catch (e) {
      this.$router.push('/');
    }  
    try{
      const responseCount = await quizApiService.getQuestionCount()
      if(responseCount && responseCount.data && responseCount.data.count)
        this.nbQuestions = responseCount.data.count
      else
        this.$router.push('/');
    }
    catch(e){
      this.$router.push('/');
    }
  }
};

</script>

<style>
</style>
