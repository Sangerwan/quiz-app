<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div  class="main">
    <div class="head">
        <h1>Super Quizz</h1>
        <div class="wrapper">
          <RouterLink to="/">Home</RouterLink>
        </div>
        <div class="wrapper">
          <RouterLink to="/about">About</RouterLink>
        </div>
    </div>
    <div  class="mainFrame">

        <RouterView />
    </div>
  </div>
</template>

<style>
 nav li.router-link-active {
   background-color: indianred;
   cursor: pointer;
 }

.wrapper {
  display: flex;
  justify-content: space-around;   
  flex-direction: row;
  width: 10%;
}

h1{
  width: 90%;
}

.head {
  display: flex;
  justify-content: space-around;
  background-color: rgb(114, 166, 219);
  width: 100%;
  height: 20%;
}

.main{
  background-color: rgb(249, 237, 223);
  height: 100%;
  width: 100%;
}

.mainFrame {
  background-color: rgb(176, 162, 188);
  display: flex;
  flex-direction: column;
  padding: 0 1rem;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
}

#app{
  height: 100%;
  width: 100%;
}

.logo {
  margin: 0 2rem 0 0;
}

nav {
  text-align: left;
  margin-left: -1rem;
  font-size: 1rem;

  padding: 1rem 0;
  margin-top: 1rem;
}
</style>
