<template>
  <div class="newQuiz">
    <h1>Connection / New User</h1>

    <h3>If your are a new user type the password you want to save</h3>
    <form>
      <div class="horizontalDiv">
        <label for="fname">Username</label>
        <input type="text" id="fname" name="firstname" placeholder="Unknown" v-model="username">
      </div>

      <div class="horizontalDiv">
        <label for="fpassword">Password</label>
        <input type="password" id="fpassword" name="password" placeholder="" v-model="password">
      </div>     
    </form>

    <div class="horizontalDiv">
       <button @click="connect" class="buttonSimple">Connect</button>
      <p>{{ errorDetails }}</p> 
    </div>   
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",
  data() {
    return {//rertourne des données réactives
      username: participationStorageService.getPlayerName(),
      password: "",
      errorDetails: "",
    };
  },  
  methods: {
    async connect() {
      try {        
        this.errorDetails="";
        const response = await quizApiService.login(this.password,this.username);
        if(response && response.data && response.data.token){
          this.errorDetails="Good password";
          participationStorageService.saveToken(response.data.token);
          participationStorageService.savePlayerName(this.username);
          return this.$router.push('/home-page-logged');   
        }
     
      } catch (e) {
        this.errorDetails="Wrong password";
        this.password= "";
      }
      
    },
  },
  async created(){    
    try {       
        const response =  await quizApiService.isLogged(
          participationStorageService.getPlayerName(),
          participationStorageService.getToken());
        if (response && response.data && response.data.isLogged) {
          return this.$router.push('/home-page-logged');
        }           
      } catch (e) {
        return this.$router.push('/');
      }  
  }

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

  input[type=text],input[type=password],
  select {
    width: 50%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  .buttonSimple {
    width: 100%;
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

  .horizontalDiv {
    display: flex;
    align-items: center;
  }

  label {
    margin-right: 15px;
    width: 30%;
    font-family: Papyrus, Helvetica, sans-serif;
    font-size: 30px;
  }

  div {
    border-radius: 5px;
    padding: 20px;
  }

  p{
    font-family: "Times New Roman", Times, serif;
    font-size: 20px;
  }

}
</style>
