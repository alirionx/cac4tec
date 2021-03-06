import Vue from 'vue'
import VueRouter from 'vue-router'
import Mashes from '../views/Mashes.vue'
import Admin from '../views/Admin.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Mashes',
    component: Mashes
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }
]

const router = new VueRouter({
  routes
})

export default router
