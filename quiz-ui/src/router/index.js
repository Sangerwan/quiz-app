import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import Question from '../views/NewQuizPage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import LogginPage from '../views/LogginPage.vue'
import HomePageLogged from '../views/HomePageLogged.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/home-page-logged',
      name: 'HomePageLogged',
      component: HomePageLogged
    },
    {
      path: '/loggin-page',
      name: 'LogginPage',
      component: LogginPage
    },
    {
      path: '/start-new-quiz-page',
      name: 'NewQuizPage',
      component: NewQuizPage
    },
    {
      path: '/questions',
      name: 'Questions',
      component: Question
    },
    {
      path: '/question-manager',
      name: 'QuestionManager',
      component: QuestionManager
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
