<template>
  <div class="head">
    <h1>Admin</h1>
    <div>
      <button @click="disconnect" class="buttonSimple">Disconnect</button>
      <button @click="addQuestion" class="buttonSimple">Add Question</button>
    </div>
  </div>
  <div class="body"> 

    <h1>Manage question</h1>

    <ul>
      <template v-for="item in Questions">
      <ul v-for="(question,index) in item">
        <button @click="editQuestion(question.position)" class="buttonQuestion" >
          <div class="question">
            <div>
              <h1><img v-if="question.image" :src="question.image" />  {{question.position}} - {{question.title}}</h1>
              {{question.text}} 
            </div>
            <ul v-for="answer in question.possibleAnswers"
              :class="answer.isCorrect ? 'correct' : 'incorrect'">
              {{answer.text}}
            </ul>
          </div>
        </button>        
      </ul>
      </template>
    </ul>

  </div>
</template>



<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  components: {
  },
  name: "AdminQuestionManager",
  data() {
    return {//rertourne des données réactives
      Questions: [],
    };
  },
  async created() {
      try {       
        const response =  await quizApiService.isLogged(
        participationStorageService.getPlayerName(),
        participationStorageService.getToken());
          if (!response.data.isLogged) 
            this.$router.push('/');
      } 
      catch (e) {
          this.disconnect();
      }  
      try{
        const questions = await quizApiService.getQuestions()
        if(questions && questions.data)
          this.Questions = questions.data
      }
      catch(e){
        console.log(e)
      }
    },
  methods: {
    async disconnect() {
      try {        
        participationStorageService.disconnect();
        this.$router.push('/');        
      } catch (e) {
        console.log(e)
      }      
    },
    async editQuestion(index) {
      console.log("editQuestion", index)
      this.$router.push({ name: "AdminEditQuestion", params: { id: index } });
    },
    async addQuestion() {
      console.log("addQuestion")
      this.$router.push({ name: "AdminEditQuestion" , params: { id: 0 } });
    },
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
