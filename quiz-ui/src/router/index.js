import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import LoginPage from '../views/LoginPage.vue'
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
      path: '/login-page',
      name: 'LoginPage',
      component: LoginPage
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
    },
    {
      path: '/Leaderboard',
      name: 'Leaderboard',
      component: () => import('../views/Leaderboard.vue')
    },
    {
      path: '/Admin',
      name: 'Admin',
      component: () => import('../views/Admin.vue')
    },
    {
      path: '/AdminQuestionManager',
      name: 'AdminQuestionManager',
      component: () => import('../views/AdminQuestionManager.vue')
    },
    {
      path: '/AdminEditQuestion/:id',
      name: 'AdminEditQuestion',
      component: () => import('../views/AdminEditQuestion.vue'),
    },
    {
      path: '/Result',
      name: 'Result',
      component: () => import('../views/Result.vue')
    }
  ]
})

export default router
