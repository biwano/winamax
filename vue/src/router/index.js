import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/:sport_id/:category_id/:tournament_id',
    name: 'Tournament',
    component: Home
  },
  {
    path: '/:sport_id/:category_id/:tournament_id/:match_id',
    name: 'Match',
    component: Home
  },
]

const router = new VueRouter({
  routes
})

export default router
