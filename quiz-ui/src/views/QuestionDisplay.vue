<template>
  
  <div class="question">
    <div class="answer">
      <p>{{ question.text }}</p>
      <a @click="$emit('answer-selected', 1)" v-if="question.possibleAnswers">La réponse A: {{question.possibleAnswers[0].text}}</a>
      <a @click="$emit('answer-selected', 2)" v-if="question.possibleAnswers">La réponse B: {{question.possibleAnswers[1].text}}</a>
      <a @click="$emit('answer-selected', 3)" v-if="question.possibleAnswers">La réponse C: {{question.possibleAnswers[2].text}}</a>
      <a @click="$emit('answer-selected', 4)" v-if="question.possibleAnswers">La réponse D: {{question.possibleAnswers[3].text}}</a>
    </div>
    <div class="data">
      <h3>{{ question.title }}</h3>
      <div class="image_question">
        <img v-if="question.image" :src="question.image" />
      </div>           
    </div>
  </div>
</template>

<script>

export default {
  emits: ["answer-selected"],
  props: {
    question: {
      type: Object
    }
  },
};
</script>

<style>
.answer {
  display: flex;
  justify-content: start;   
  flex-direction: column;
  background-color: rgb(224, 193, 114);
  width: 50%;
}
.data {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;  
  width: 50%;
  height: 100%;
}

a:hover {
  background-color: chartreuse;
}

a:after {
  background-color: rgb(24, 45, 4);
}

.question{
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
}

img{
  height : auto;
  max-width : 300px;
  max-Height : 300px;
}
</style>
