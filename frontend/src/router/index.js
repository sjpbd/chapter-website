import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Repository from '../views/Repository.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/',           name: 'Home',        component: Home },
  { path: '/repository', name: 'Repository',  component: Repository },
  { path: '/about',      name: 'About',       component: About },
  { path: '/prayer',     name: 'Prayer',      component: () => import('../views/PrayerCard.vue') },
  { path: '/schedule',   name: 'Schedule',    component: () => import('../views/Schedule.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router

