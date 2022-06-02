<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />

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
      totalNumberOfQuestion: 10,
      participation:[]
    };
  },
  async created() {
    await this.loadQuestionByPosition(this.currentQuestionPosition);
  },

  methods: {
    async loadQuestionByPosition(position){
      const question = await quizApiService.getQuestion(position);
      this.currentQuestion = question.data;
      console.log(this.currentQuestion);
      console.log(this.currentQuestion.possibleAnswers[0].text);
      //const possibleAnswers = await quizApiService.getAnswersOfQuestion(this.currentQuestion.id);
      //this.possibleAnswers = possibleAnswers.data;
      //console.log(this.possibleAnswers, "possibleAnswers");
    },

    async answerClickedHandler(answerId) {
      console.log("answer clicked", answerId);
      //check if selected answer is correct
      //console.log(this.possibleAnswers[answerId]);
      //const isCorrect = this.possibleAnswers[answerId].isCorrect;
      //console.log("selected answer", this.possibleAnswers[answerId].text, "is", isCorrect);
      this.participation.push(answerId);
      if(this.currentQuestionPosition< this.totalNumberOfQuestion){
        await this.loadQuestionByPosition(++this.currentQuestionPosition);
      }
      else{
        await this.endQuiz();
      }
    },  

    async endQuiz() {
      console.log(this.participation, "participation");
      quizApiService.setParticipation(ParticipationStorageService.getPlayerName(), this.participation, ParticipationStorageService.getToken());
      console.log("end quiz");
    }

  }
};

</script>

<style>
</style>
