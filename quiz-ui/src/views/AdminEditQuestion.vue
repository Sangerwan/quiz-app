<template>
  <div class="head">
    <h1>Admin</h1>
    <div>
      <button @click="disconnect" class="buttonSimple">Disconnect</button>
      <button @click="back" class="buttonSimple">Back</button>
    </div>
  </div>

  <div class="body"> 
    <h1>Edit question {{errorMessage}}</h1>

    <div class="preview">
      <h1>Preview</h1>
      <QuestionDisplay :question="currentQuestion"/>
    </div>


    <div class="edit">

      <div class="title">
        <h1>Title</h1>
        <input v-model="currentQuestion.title">
      </div>

      <div class="text">
        <h1>Text</h1>
        <textarea v-model="currentQuestion.text">
        </textarea>
      </div>

      <div class="image">
        <h1>Image</h1>
        <img v-if="currentQuestion.image" :src="currentQuestion.image" />
        <input v-model="currentQuestion.image">
        <input type="file" accept="image/*" @change="uploadImage">
      </div>

      <div class="answers">
        <h1>Answers</h1>
        <ul v-for="(answer,index) in currentQuestion.possibleAnswers">
          <div class="answersbox">
            <input type="checkbox" v-model="answer.isCorrect" @change="checkCheckbox(index)">
            <input v-model="answer.text">
          </div>
        </ul>
      </div>

      <div class="position">
        <h1>Position</h1>
        <input v-model="currentQuestion.position">
        
      </div>
        
    </div>

    <div class="buttons">
      <div>
        <button @click="deleteQuestion" class="buttonRed">Delete question</button>
      </div>
      <div>
        <button @click="revert" class="buttonSimple">Revert</button>
      </div>
      <div>
        <button @click="save" class="buttonSimple">Save</button>
      </div>
    </div>

</div>
</template>



<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import QuestionDisplay from "@/views/QuestionDisplay.vue";
import QuizApiService from "../services/QuizApiService";
export default {
  components: {
    QuestionDisplay
  },
  name: "AdminEditQuestion",
  data() {
    return {//rertourne des données réactives
      currentQuestion: [],
      errorMessage: "",
      currentQuestionPosition: 0,
    };
  },
  
  async created() {

      try {       
        const response =  await quizApiService.isLogged(
        participationStorageService.getPlayerName(),
        participationStorageService.getToken());
          if (!response.data.isLogged) 
            this.disconnect();
      } 
      catch (e) {
          this.disconnect();
      }  
      this.currentQuestionPosition = parseInt( this.$route.params.id);

      if( this.currentQuestionPosition === 0)
      {
        try{
          var response = await quizApiService.getQuestionCount()
          if(response.data.count)
            this.currentQuestionPosition = response.data.count
        }
        catch (e) {
          console.log(e)
        }
        this.currentQuestion = {
          title: "",
          text: "",
          image: "",
          possibleAnswers: [
            {
              text: "",
              isCorrect: true
            },
            {
              text: "",
              isCorrect: false
            },
            {
              text: "",
              isCorrect: false
            },
            {
              text: "",
              isCorrect: false
            }
          ],
          position: this.currentQuestionPosition + 1
        };
      }
      else
      {
        try{
          const question = await quizApiService.getQuestion(this.currentQuestionPosition);
          this.currentQuestion = question.data;
        }
        catch (e) {
          console.log(e)
        }      
      }
      this.testimg = this.currentQuestion.image;
    },
  methods: {
    disconnect() {
      participationStorageService.disconnect();
      return this.$router.push('/');
    },

    back() {
      return this.$router.push('/AdminQuestionManager');
    },
    async save() {
      if(this.checkQuestion()){
        if(parseInt( this.$route.params.id) === 0)
        await quizApiService.addQuestion(this.currentQuestion, participationStorageService.getToken());
        else
          await quizApiService.updateQuestion(this.currentQuestionPosition, JSON.stringify( this.currentQuestion), participationStorageService.getToken());
        return this.$router.push('/AdminQuestionManager');
      }
    },
    revert() {
      return this.$router.go();
    },
    async deleteQuestion() {
      await QuizApiService.deleteQuestion(this.currentQuestionPosition, participationStorageService.getToken());
      return this.$router.push('/AdminQuestionManager');
    },
    checkCheckbox(index) {
      this.currentQuestion.possibleAnswers.forEach(answer => {
        answer.isCorrect = false;
      });
      this.currentQuestion.possibleAnswers[index].isCorrect = true;
    },
    checkQuestion(){
      if(this.currentQuestion.title === "")
        this.errorMessage = "Title is empty";
      else if(this.currentQuestion.text === "")
        this.errorMessage = "Text is empty";
      else if(this.currentQuestion.possibleAnswers.some(answer => answer.text === ""))
        this.errorMessage = "Answers are empty";
      else
        return true
      return false
    },
    uploadImage(e) {
      const image = e.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = e =>{
          this.currentQuestion.image = e.target.result;
      };
    }
  }
};
</script>

<style>

.buttonRed{
    width: 100%;
    background-color: red;
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

.buttons {
  display: flex;
  justify-content: space-around;
  flex-direction: row;
}

.answersbox {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
}

input {
  display: flex;
  width: 100%;
}

textarea {
  width: 100%;
  height: 100%;
}


.title {
  align-items: center;
  width: 100%;
}


.text {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.preview {
  background-color: rgba(0, 110, 255, 0.363);
}

.edit {
  width: auto;
  background-color: rgba(255, 187, 0, 0.363);
}

.body{
  width: 100%;
}
</style>
