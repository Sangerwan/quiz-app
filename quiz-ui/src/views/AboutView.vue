<template>
  <div class="about">
    <div class="horizontal">
      <h2>Projet de dev web Fullstack ESIEE Paris</h2>
      <img src="https://upload.wikimedia.org/wikipedia/fr/thumb/7/71/Logo_ESIEE_Paris.svg/2560px-Logo_ESIEE_Paris.svg.png" />
    </div>
    <h3>Olivier Troissant</h3>
    <h3>Erwan Sangchanmahola</h3>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    height: 100%;
    width:100%;
    display: flex;
    justify-content: space-between;
    flex-direction: column;
  }
}

.horizontal{
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
}
</style>
