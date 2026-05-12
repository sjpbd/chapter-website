<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { Home, FolderOpen, Info, Menu, X, FileText, HandHeart, CalendarDays } from 'lucide-vue-next'
import { useConfigStore } from '../store/configStore'
import GlobalSearch from './GlobalSearch.vue'

const configStore = useConfigStore()

const isScrolled = ref(false)
const isMenuOpen = ref(false)
const route = useRoute()

const handleScroll = () => { isScrolled.value = window.scrollY > 30 }
onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<template>
  <nav :class="['navbar', { scrolled: isScrolled }]">
    <div class="nav-inner">
      <!-- Logo -->
      <RouterLink to="/" class="logo">
        <div class="logo-icon">
          <img v-if="configStore.logo" :src="configStore.logo" :alt="configStore.siteName" class="dynamic-logo" />
          <FileText v-else :size="22" color="white" />
        </div>
        <div class="logo-text">
          <span class="brand">{{ configStore.siteName.split(' ')[0] }}</span>
          <span class="tagline">{{ configStore.siteName.split(' ').slice(1).join(' ') }}</span>
        </div>
      </RouterLink>

      <!-- Desktop Nav Links -->
      <div class="nav-links">
        <RouterLink to="/" class="nav-item">
          <Home :size="17" /><span>Home</span>
        </RouterLink>
        <RouterLink to="/repository" class="nav-item">
          <FolderOpen :size="17" /><span>Repository</span>
        </RouterLink>
        <RouterLink to="/about" class="nav-item">
          <Info :size="17" /><span>About</span>
        </RouterLink>
        <RouterLink to="/prayer" class="nav-item nav-prayer">
          <HandHeart :size="17" /><span>Prayer</span>
        </RouterLink>
        <RouterLink to="/schedule" class="nav-item nav-schedule">
          <CalendarDays :size="17" /><span>Schedule</span>
        </RouterLink>
      </div>

      <!-- Global Search (desktop) -->
      <div v-if="route.path !== '/repository'" class="nav-search-area">
        <GlobalSearch />
      </div>

      <!-- Mobile burger -->
      <div class="nav-mobile-toggle">
        <button 
          class="burger-btn" 
          :class="{ active: isMenuOpen }"
          @click="isMenuOpen = !isMenuOpen" 
          aria-label="Toggle menu"
        >
          <div class="burger-lines">
            <span class="line line-1"></span>
            <span class="line line-2"></span>
            <span class="line line-3"></span>
          </div>
        </button>
      </div>
    </div>

    <!-- Mobile Drawer -->
    <Transition name="drawer">
      <div v-if="isMenuOpen" class="mobile-menu-wrapper">
        <div class="mobile-menu">
          <RouterLink to="/" class="mob-item" @click="isMenuOpen = false">
            <div class="mob-icon"><Home :size="20" /></div>
            <span>Home</span>
          </RouterLink>
          <RouterLink to="/repository" class="mob-item" @click="isMenuOpen = false">
            <div class="mob-icon"><FolderOpen :size="20" /></div>
            <span>Repository</span>
          </RouterLink>
          <RouterLink to="/about" class="mob-item" @click="isMenuOpen = false">
            <div class="mob-icon"><Info :size="20" /></div>
            <span>About</span>
          </RouterLink>
          <RouterLink to="/prayer" class="mob-item mob-prayer" @click="isMenuOpen = false">
            <div class="mob-icon"><HandHeart :size="20" /></div>
            <span>Prayer</span>
          </RouterLink>
          <RouterLink to="/schedule" class="mob-item mob-schedule" @click="isMenuOpen = false">
            <div class="mob-icon"><CalendarDays :size="20" /></div>
            <span>Schedule</span>
          </RouterLink>
          <div v-if="route.path !== '/repository'" class="mob-search">
            <GlobalSearch />
          </div>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  height: 72px;
  background-color: transparent;
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  border-bottom: 1px solid transparent;
}

.navbar.scrolled {
  background-color: rgba(255,255,255,0.85);
  box-shadow: 0 4px 30px rgba(0,0,0,0.04);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.nav-inner {
  max-width: 1440px;
  margin: 0 auto;
  height: 100%;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  margin-right: 1.5rem;
}

.logo-icon {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6px 18px rgba(0,120,212,0.25);
  flex-shrink: 0;
  overflow: hidden;
}

.dynamic-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logo-text { display: flex; flex-direction: column; line-height: 1.1; }
.brand    { font-size: 1.1rem; font-weight: 800; letter-spacing: 1px; color: var(--text-main); }
.tagline  { font-size: 0.7rem; font-weight: 500; color: var(--text-secondary); opacity: 0.8; }

/* Nav links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-secondary);
  transition: all 0.25s ease;
  white-space: nowrap;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: var(--primary-color);
  background: rgba(0,120,212,0.06);
}

/* Specific nav item highlights */
.nav-prayer {
  color: #8a5e00;
  background: rgba(245,200,66,0.08);
  border: 1px solid rgba(245,200,66,0.15);
}
.nav-prayer:hover, .nav-prayer.router-link-active {
  color: #7a4e00;
  background: rgba(245,200,66,0.15);
  border-color: rgba(245,200,66,0.3);
}

.nav-schedule {
  color: #0369a1;
  background: rgba(14,165,233,0.06);
  border: 1px solid rgba(14,165,233,0.15);
}
.nav-schedule:hover, .nav-schedule.router-link-active {
  color: #075985;
  background: rgba(14,165,233,0.12);
  border-color: rgba(14,165,233,0.3);
}

/* Search area - pushes burger to right on mobile when hidden */
.nav-search-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

/* Burger Button Upgrade */
.nav-mobile-toggle {
  display: none;
  margin-left: auto; /* This pushes it to the far right */
}

.burger-btn {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.burger-btn:hover {
  background: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0,120,212,0.1);
}

.burger-btn.active {
  background: white;
  border-color: #fee2e2;
}

.burger-lines {
  width: 22px;
  height: 16px;
  position: relative;
}

.line {
  display: block;
  position: absolute;
  height: 2.5px;
  width: 100%;
  background: var(--text-main);
  border-radius: 9px;
  opacity: 1;
  left: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.line-1 { top: 0px; }
.line-2 { top: 7px; width: 80%; } /* Middle line slightly shorter */
.line-3 { top: 14px; }

.burger-btn:hover .line-2 { width: 100%; }

.active .line-1 {
  top: 7px;
  transform: rotate(135deg);
  background: #dc2626;
}

.active .line-2 {
  opacity: 0;
  left: -20px;
}

.active .line-3 {
  top: 7px;
  transform: rotate(-135deg);
  background: #dc2626;
}

/* Mobile Drawer */
.mobile-menu-wrapper {
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(0,0,0,0.06);
  overflow: hidden;
}

.mobile-menu {
  padding: 1.5rem 1.5rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  max-width: 600px;
  margin: 0 auto;
}

.mob-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
  border-radius: 16px;
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--text-secondary);
  transition: all 0.25s ease;
  background: rgba(0,0,0,0.02);
}

.mob-icon {
  width: 38px; height: 38px;
  background: white;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: var(--primary-color);
  box-shadow: 0 4px 10px rgba(0,0,0,0.04);
}

.mob-item:hover, .mob-item.router-link-active {
  color: var(--primary-color);
  background: white;
  box-shadow: 0 10px 20px rgba(0,120,212,0.08);
  transform: translateX(4px);
}

/* Mobile Accents */
.mob-prayer { color: #8a5e00; }
.mob-prayer .mob-icon { color: #d97706; }
.mob-prayer:hover, .mob-prayer.router-link-active { background: #fffbeb; }

.mob-schedule { color: #0369a1; }
.mob-schedule .mob-icon { color: #0ea5e9; }
.mob-schedule:hover, .mob-schedule.router-link-active { background: #f0f9ff; }

.mob-search {
  margin-top: 1rem;
  padding: 0 10px;
}

/* Drawer animation upgrade */
.drawer-enter-active, .drawer-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.drawer-enter-from, .drawer-leave-to { 
  max-height: 0; 
  opacity: 0;
  transform: translateY(-10px);
}
.drawer-enter-to, .drawer-leave-from { 
  max-height: 800px; 
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 1024px) {
  .nav-links { display: none; }
  .nav-search-area { display: none; }
  .nav-mobile-toggle { display: block; }
  .nav-inner { padding: 0 1.2rem; }
  .logo { margin-right: 0; }
}
</style>
