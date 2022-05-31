<template>
  <div class="newQuiz">
    <h1>New Quiz</h1>

    <h3>Saisissez votre nom :</h3>
    <form>
      <label for="fname">Username</label>
      <input type="text" id="fname" name="firstname" placeholder="Unknown" v-model="username">
    </form>

    <Button @click="launchNewQuiz" class="buttonSimple">Go!</Button>

  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",
  data() {
    return {//rertourne des données réactives
      username: participationStorageService.getPlayerName()
    };
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  },
  
};

</script>



<style>
@media (min-width: 1024px) {
  .newQuiz {
    min-height: 100vh;
    vertical-align: middle;
  }

  .buttonSpecial {
    display: inline-block;
    padding: 15px 25px;
    font-size: 24px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: #fff;
    background-color: #4CAF50;
    border: none;
    border-radius: 15px;
    box-shadow: 0 9px #999;
  }

  .buttonSpecial:hover {
    background-color: #3e8e41
  }

  .buttonSpecial:active {
    background-color: #3e8e41;
    box-shadow: 0 5px #666;
    transform: translateY(4px);
  }

  input[type=text],
  select {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  .buttonSimple {
    width: 30%;
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    border-radius: 4px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    cursor: pointer;
  }

  .buttonSimple:hover {
    background-color: #45a049;
  }

  div {
    border-radius: 5px;
    padding: 20px;
  }

}
</style>
