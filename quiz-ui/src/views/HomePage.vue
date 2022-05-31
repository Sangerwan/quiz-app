<template>
  <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
</template>

<script>
import quizApiService from "@/services/quizApiService";

export default {
  name: "HomePage",
  data() {
    return {//rertourne des données réactives
      registeredScores: []
    };
  },
  async created() {
    const instance = await quizApiService.getQuizInfo();      
    console.log("after init ", instance.data);
    console.log("scores:", instance.data.scores);


    //console.log("Composant Home page 'created' ", this.registeredScores.length);
  }
};

</script>

<style>
</style>
