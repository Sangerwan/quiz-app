<template>
  <h1>WELCOME</h1>
  
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "HomePage",
  data() {
    return {//rertourne des données réactives
      registeredScores: []
    };
  },
  async created() {
    const instance = await quizApiService.getQuizInfo();   
    try {    
      const username =   participationStorageService.getPlayerName()
      if (!username){
        return this.$router.push('/login-page');
      }
      const response =  await quizApiService.isLogged(
                        participationStorageService.getPlayerName(),
                        participationStorageService.getToken());

      if (!response.data.isLogged) 
      {
        return this.$router.push('/login-page');
      }
      else
      {
        return this.$router.push('/home-page-logged');
      }          
    } 
    catch (e) 
    {
      return this.$router.push('/login-page');
    }  
  }
};

</script>

<style>
</style>
