<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Home, FolderOpen, Info, Menu, X, FileText } from 'lucide-vue-next'
import GlobalSearch from './GlobalSearch.vue'

const isScrolled = ref(false)
const isMenuOpen = ref(false)

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
          <FileText :size="22" color="white" />
        </div>
        <div class="logo-text">
          <span class="brand">SJP</span>
          <span class="tagline">Chapter Hub</span>
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
      </div>

      <!-- Global Search (desktop) -->
      <div class="nav-search-area">
        <GlobalSearch />
      </div>

      <!-- Mobile burger -->
      <button class="burger" @click="isMenuOpen = !isMenuOpen" aria-label="Toggle menu">
        <component :is="isMenuOpen ? X : Menu" :size="24" />
      </button>
    </div>

    <!-- Mobile Drawer -->
    <Transition name="drawer">
      <div v-if="isMenuOpen" class="mobile-menu">
        <RouterLink to="/" class="mob-item" @click="isMenuOpen = false">
          <Home :size="20" /> Home
        </RouterLink>
        <RouterLink to="/repository" class="mob-item" @click="isMenuOpen = false">
          <FolderOpen :size="20" /> Repository
        </RouterLink>
        <RouterLink to="/about" class="mob-item" @click="isMenuOpen = false">
          <Info :size="20" /> About
        </RouterLink>
        <div class="mob-search">
          <GlobalSearch />
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
  transition: var(--transition-smooth);
}

.navbar.scrolled {
  background: rgba(255,255,255,0.88);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  box-shadow: 0 2px 20px rgba(0,0,0,0.07);
}

.nav-inner {
  max-width: 1440px;
  margin: 0 auto;
  height: 100%;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.logo-icon {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6px 18px rgba(0,120,212,0.35);
  flex-shrink: 0;
}

.logo-text { display: flex; flex-direction: column; line-height: 1.1; }
.brand    { font-size: 1.1rem; font-weight: 800; letter-spacing: 1.5px; color: var(--primary-color); }
.tagline  { font-size: 0.7rem; font-weight: 500; color: var(--text-secondary); }

/* Nav links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  flex-shrink: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-secondary);
  transition: var(--transition-smooth);
  white-space: nowrap;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: var(--primary-color);
  background: rgba(0,120,212,0.07);
}

/* Search area */
.nav-search-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

/* Burger */
.burger {
  display: none;
  background: none;
  color: var(--text-main);
  padding: 8px;
  border-radius: 8px;
  transition: var(--transition-smooth);
  flex-shrink: 0;
}
.burger:hover { background: rgba(0,0,0,0.05); }

/* Mobile menu */
.mobile-menu {
  background: rgba(255,255,255,0.97);
  backdrop-filter: blur(24px);
  border-top: 1px solid var(--border-subtle);
  padding: 1rem 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.mob-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 16px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-secondary);
  transition: var(--transition-smooth);
}

.mob-item:hover, .mob-item.router-link-active {
  color: var(--primary-color);
  background: rgba(0,120,212,0.07);
}

.mob-search {
  margin-top: 0.8rem;
  width: 100%;
}

/* Drawer animation */
.drawer-enter-active, .drawer-leave-active {
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
  overflow: hidden;
}
.drawer-enter-from, .drawer-leave-to { max-height: 0; opacity: 0; }
.drawer-enter-to, .drawer-leave-from { max-height: 600px; opacity: 1; }

@media (max-width: 900px) {
  .nav-links { display: none; }
  .nav-search-area { display: none; }
  .burger { display: flex; }
}
</style>
