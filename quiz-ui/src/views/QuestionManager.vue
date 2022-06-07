<template>
  <h3>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h3>
  <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
  <h3>{{errorMessage}}</h3>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import ParticipationStorageService from "../services/ParticipationStorageService";
import QuestionDisplay from "@/views/QuestionDisplay.vue";
export default {
  components: {
    QuestionDisplay
  },
  data() {
    return {//rertourne des données réactives
      currentQuestion: [],
      //possibleAnswers: [],
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      participation:[],
      errorMessage:""
    };
  },
  async created() {
    try {       
        const response =  await quizApiService.isLogged(
                                ParticipationStorageService.getPlayerName(),
                                ParticipationStorageService.getToken());
        if (!response.data.isLogged) {
          return this.$router.push('/');
        }
        const responseCount = await quizApiService.getQuestionCount()
        if(responseCount && responseCount.data && responseCount.data.count)
          this.totalNumberOfQuestion = responseCount.data.count
        if (this.totalNumberOfQuestion==0){
          this.errorMessage="There are no questions for the moment, please come back later"
        }else{
          await this.loadQuestionByPosition(this.currentQuestionPosition);
        }    
    } catch (e) {
      return this.$router.push('/');
    }  

  },

  methods: {
    async loadQuestionByPosition(position){
      const question = await quizApiService.getQuestion(position);
      this.currentQuestion = question.data;
    },

    async answerClickedHandler(answerId) {
      this.participation.push(answerId);
      if(this.currentQuestionPosition< this.totalNumberOfQuestion){
        await this.loadQuestionByPosition(++this.currentQuestionPosition);
      }
      else{
        await this.endQuiz();
      }
    },  

    async endQuiz() {
      await quizApiService.setParticipation(ParticipationStorageService.getPlayerName(), this.participation, ParticipationStorageService.getToken());
      return this.$router.push('/Result');
    }

  }
};

</script>

<style>
</style>
