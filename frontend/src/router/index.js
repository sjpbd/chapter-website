import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Repository from '../views/Repository.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/',           name: 'Home',        component: Home, meta: { title: 'Home' } },
  { path: '/repository', name: 'Repository',  component: Repository, meta: { title: 'Document Repository' } },
  { path: '/about',      name: 'About',       component: About, meta: { title: 'About Us' } },
  { path: '/prayer',     name: 'Prayer',      component: () => import('../views/PrayerCard.vue'), meta: { title: 'Chapter Prayer' } },
  { path: '/schedule',   name: 'Schedule',    component: () => import('../views/Schedule.vue'), meta: { title: 'Daily Programme Schedule' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.afterEach((to) => {
  const baseTitle = 'SJP Chapter Hub'
  document.title = to.meta.title ? `${to.meta.title} - ${baseTitle}` : baseTitle
})

export default router

