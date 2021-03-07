import Vue from 'vue'
import VueRouter from 'vue-router'
import Mashes from '../views/Mashes.vue'
import Pics from '../views/Pics.vue'
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
  },
  {
    path: '/pics/:id',
    name: 'Pics',
    component: Pics
  }
]

const router = new VueRouter({
  routes
})

export default router
