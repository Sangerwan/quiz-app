<template>

  
  <div class="head">
    <h1>Admin</h1>
    <div>
      <button @click="disconnect" class="buttonSimple">Disconnect</button>
    </div>
  </div>


  <div class="body"> 
      <div>
        <button @click="manageQuestion" class="buttonSimple">Manage question</button>
      </div>           
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  components: {
  },
  name: "Admin",
  async created() {
    try {       
        const response =  await quizApiService.isLogged(
          participationStorageService.getPlayerName(),
          participationStorageService.getToken());
        if (!response.data.isLogged) 
          this.$router.push('/');
      } catch (e) {
        this.disconnect();
      }  
  },
  methods: {
    manageQuestion() {
      this.$router.push('/AdminQuestionManager');
    },
    async disconnect() {
      try {        
        participationStorageService.disconnect();
        this.$router.push('/');        
      } catch (e) {
        console.log(e)
      }      
    },
  }
};
</script>

<style>

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
