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
        <div class="logo-icon" :class="{ 'has-logo': configStore.logo }">
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
  height: 84px;
  background-color: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  border-bottom: 1px solid transparent;
}

.navbar.scrolled {
  background-color: rgba(255, 255, 255, 0.88);
  box-shadow: 0 8px 32px rgba(0, 106, 220, 0.04);
  border-bottom: 1px solid rgba(0, 106, 220, 0.08);
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
  width: 64px; height: 64px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6px 18px rgba(0,120,212,0.25);
  flex-shrink: 0;
  overflow: hidden;
  transition: all 0.3s ease;
}

.logo-icon.has-logo {
  background: none;
  box-shadow: none;
  border-radius: 0;
}

.dynamic-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.logo-text { display: flex; flex-direction: column; line-height: 1.1; }
.brand    { font-size: 1.25rem; font-weight: 800; letter-spacing: 0.5px; color: var(--text-main); }
.tagline  { font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); opacity: 0.85; text-transform: uppercase; letter-spacing: 0.5px; }

/* Nav links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.92rem;
  color: var(--text-secondary);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  white-space: nowrap;
}

/* Icon micro-animations */
.nav-item svg {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  color: inherit;
}

.nav-item:hover svg {
  transform: scale(1.15) translateY(-1px);
}

/* Slide underline for standard items */
.nav-item:not(.nav-prayer):not(.nav-schedule)::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 18px;
  height: 3px;
  background-color: var(--primary-color);
  border-radius: 2px;
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.3s ease;
  opacity: 0;
}

.nav-item:not(.nav-prayer):not(.nav-schedule):hover::after,
.nav-item:not(.nav-prayer):not(.nav-schedule).router-link-active::after {
  transform: translateX(-50%) scaleX(1);
  opacity: 1;
}

.nav-item:not(.nav-prayer):not(.nav-schedule):hover {
  color: var(--primary-color);
  background: rgba(0, 120, 212, 0.04);
}

.nav-item:not(.nav-prayer):not(.nav-schedule).router-link-active {
  color: var(--primary-color);
  background: rgba(0, 120, 212, 0.07);
}

/* Specific nav item highlights */
.nav-prayer {
  color: #7a4e00;
  background: rgba(212, 175, 55, 0.05);
  border: 1px solid rgba(212, 175, 55, 0.2);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.04);
}
.nav-prayer:hover, .nav-prayer.router-link-active {
  color: #fff;
  background: linear-gradient(135deg, #b4821e 0%, #d4af37 100%);
  border-color: #b4821e;
  box-shadow: 0 6px 16px rgba(212, 175, 55, 0.25);
  transform: translateY(-1px);
}

.nav-schedule {
  color: #0369a1;
  background: rgba(14, 165, 233, 0.05);
  border: 1px solid rgba(14, 165, 233, 0.2);
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.04);
}
.nav-schedule:hover, .nav-schedule.router-link-active {
  color: #fff;
  background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 100%);
  border-color: #0284c7;
  box-shadow: 0 6px 16px rgba(14, 165, 233, 0.25);
  transform: translateY(-1px);
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
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-top: 1px solid rgba(0, 106, 220, 0.08);
  overflow: hidden;
}

.mobile-menu {
  padding: 2rem 1.2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8rem;
  max-width: 500px;
  margin: 0 auto;
}

.mob-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 1.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-secondary);
  transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.03);
  text-align: center;
}

/* Home button takes full width */
.mob-item:first-of-type {
  grid-column: span 2;
  flex-direction: row;
  padding: 1.1rem 1.5rem;
  justify-content: flex-start;
  gap: 16px;
}

.mob-icon {
  width: 44px; height: 44px;
  background: white;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: var(--primary-color);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
  transition: all 0.25s ease;
  flex-shrink: 0;
}

.mob-item:hover, .mob-item.router-link-active {
  color: var(--primary-color);
  background: white;
  box-shadow: 0 10px 25px rgba(0, 106, 220, 0.06);
  transform: translateY(-2px);
  border-color: rgba(0, 106, 220, 0.12);
}

.mob-item:hover .mob-icon,
.mob-item.router-link-active .mob-icon {
  background: rgba(0, 106, 220, 0.06);
  color: var(--primary-color);
  transform: scale(1.05);
}

/* Mobile Accents */
.mob-prayer {
  color: #7a4e00;
  border-color: rgba(212, 175, 55, 0.1);
  background: rgba(212, 175, 55, 0.03);
}
.mob-prayer .mob-icon {
  color: #b4821e;
}
.mob-prayer:hover, .mob-prayer.router-link-active {
  background: #fffdf9;
  border-color: rgba(212, 175, 55, 0.25);
  color: #b4821e;
}
.mob-prayer:hover .mob-icon,
.mob-prayer.router-link-active .mob-icon {
  background: rgba(212, 175, 55, 0.08);
  color: #b4821e;
}

.mob-schedule {
  color: #0369a1;
  border-color: rgba(14, 165, 233, 0.1);
  background: rgba(14, 165, 233, 0.03);
}
.mob-schedule .mob-icon {
  color: #0ea5e9;
}
.mob-schedule:hover, .mob-schedule.router-link-active {
  background: #f0f9ff;
  border-color: rgba(14, 165, 233, 0.25);
  color: #0284c7;
}
.mob-schedule:hover .mob-icon,
.mob-schedule.router-link-active .mob-icon {
  background: rgba(14, 165, 233, 0.08);
  color: #0ea5e9;
}

.mob-search {
  grid-column: span 2;
  margin-top: 0.5rem;
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
