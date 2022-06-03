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
      totalNumberOfQuestion: 10,
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
          this.$router.push('/');
        }
    } catch (e) {
      this.$router.push('/');
    }  
    const responseCount = await quizApiService.getQuestionCount()
    this.totalNumberOfQuestion = responseCount.data.count
    if (this.totalNumberOfQuestion==0){
      this.errorMessage="There are no questions for the moment, please come back later"
    }else{
      await this.loadQuestionByPosition(this.currentQuestionPosition);
    }    
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
        this.$router.push('/home-page-logged');
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
