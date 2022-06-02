<template>
  <h1>Question Display</h1>
  <img v-if="question.image" :src="question.image" />
  <h2>{{ question.title }}</h2>
  <p>{{ question.text }}</p>
  <a @click="$emit('answer-selected', 1)" v-if="question.possibleAnswers">La réponse A: {{question.possibleAnswers[0].text}}</a>
  <a @click="$emit('answer-selected', 2)" v-if="question.possibleAnswers">La réponse B: {{question.possibleAnswers[1].text}}</a>
  <a @click="$emit('answer-selected', 3)" v-if="question.possibleAnswers">La réponse C: {{question.possibleAnswers[2].text}}</a>
  <a @click="$emit('answer-selected', 4)" v-if="question.possibleAnswers">La réponse D: {{question.possibleAnswers[3].text}}</a>
</template>

<script>

export default {
  emits: ["answer-selected"],
  props: {
    question: {
      type: Object
    }
  },
  async created(){
    //console.log(this.question, "display question");
    //console.log(this.answers, "display answers");
  }
};
</script>

<style>
</style>
