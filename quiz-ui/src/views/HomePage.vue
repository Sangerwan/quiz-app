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
          this.$router.push('/login-page');
       }
        const response =  await quizApiService.isLogged(
          participationStorageService.getPlayerName(),
          participationStorageService.getToken());
        if (response.data.isLogged) {
          this.$router.push('/home-page-logged');
          this.errorDetails=participationStorageService.getPlayerName()+" is logged";
        }else{
          this.$router.push('/login-page');
          this.errorDetails=participationStorageService.getPlayerName()+" need to log again";
        }          
      } catch (e) {
        this.errorDetails=participationStorageService.getPlayerName()+" need to log again";
      }  


    //console.log("Composant Home page 'created' ", this.registeredScores.length);
  }
};

</script>

<style>
</style>
