<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useConfigStore } from './store/configStore'
import Navbar from './components/Navbar.vue'
import SiteFooter from './components/SiteFooter.vue'
import { Compass, Home, FolderOpen, HandHeart, CalendarDays, X } from 'lucide-vue-next'

const configStore = useConfigStore()
const isFabMenuOpen = ref(false)
const route = useRoute()

onMounted(() => {
  configStore.fetchConfig()
})
</script>

<template>
  <div id="app-shell">
    <Navbar />
    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    <SiteFooter />

    <!-- Floating Action Menu (Mobile FAB) -->
    <div v-if="route.path !== '/repository'" class="fab-container" :class="{ active: isFabMenuOpen }">
      <!-- Backdrop overlay -->
      <div class="fab-backdrop" @click="isFabMenuOpen = false"></div>

      <!-- Floating actions menu -->
      <div class="fab-menu">
        <RouterLink to="/" class="fab-action-item" @click="isFabMenuOpen = false">
          <span class="fab-label">Home</span>
          <div class="fab-icon-btn"><Home :size="20" /></div>
        </RouterLink>
        <RouterLink to="/repository" class="fab-action-item" @click="isFabMenuOpen = false">
          <span class="fab-label">Repository</span>
          <div class="fab-icon-btn"><FolderOpen :size="20" /></div>
        </RouterLink>
        <RouterLink to="/prayer" class="fab-action-item" @click="isFabMenuOpen = false">
          <span class="fab-label">Chapter Prayer</span>
          <div class="fab-icon-btn gold"><HandHeart :size="20" /></div>
        </RouterLink>
        <RouterLink to="/schedule" class="fab-action-item" @click="isFabMenuOpen = false">
          <span class="fab-label">Schedule</span>
          <div class="fab-icon-btn blue"><CalendarDays :size="20" /></div>
        </RouterLink>
      </div>

      <!-- Trigger Button -->
      <button class="fab-trigger" @click="isFabMenuOpen = !isFabMenuOpen" aria-label="Toggle Quick Navigation">
        <X v-if="isFabMenuOpen" :size="24" class="icon-close" />
        <Compass v-else :size="24" class="icon-compass" />
      </button>
    </div>
  </div>
</template>

<style>
#app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding-top: 84px; /* height of fixed navbar */
}

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.page-enter-from { opacity: 0; transform: translateY(14px); }
.page-leave-to   { opacity: 0; transform: translateY(-8px); }

/* Floating Action Button (FAB) Navigation */
.fab-container {
  display: none; /* Hidden on desktop screens */
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 2000;
  pointer-events: none;
}

@media (max-width: 1024px) {
  .fab-container {
    display: block; /* Show on mobile/tablet */
  }
}

.fab-trigger {
  pointer-events: auto;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 120, 212, 0.4);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  z-index: 2002;
}

.fab-trigger:active {
  transform: scale(0.92);
}

.fab-container.active .fab-trigger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
  transform: rotate(90deg);
}

.icon-compass {
  animation: compassPulse 6s linear infinite;
}

@keyframes compassPulse {
  0% { transform: rotate(0deg); }
  50% { transform: rotate(15deg); }
  100% { transform: rotate(0deg); }
}

/* Backdrop */
.fab-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.25);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  opacity: 0;
  pointer-events: none;
  z-index: 2000;
  transition: opacity 0.35s ease;
}

.fab-container.active .fab-backdrop {
  opacity: 1;
  pointer-events: auto;
}

/* Floating Actions Menu */
.fab-menu {
  position: absolute;
  bottom: 76px;
  right: 6px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.8rem;
  z-index: 2001;
}

.fab-action-item {
  display: flex;
  align-items: center;
  gap: 12px;
  pointer-events: none;
  opacity: 0;
  transform: scale(0.8) translateY(20px);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  text-decoration: none;
}

.fab-container.active .fab-action-item {
  pointer-events: auto;
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Staggered Delay */
.fab-action-item:nth-child(1) { transition-delay: 0.18s; }
.fab-action-item:nth-child(2) { transition-delay: 0.12s; }
.fab-action-item:nth-child(3) { transition-delay: 0.06s; }
.fab-action-item:nth-child(4) { transition-delay: 0s; }

.fab-label {
  background: white;
  color: var(--text-main);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.88rem;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.fab-icon-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.fab-action-item:active .fab-icon-btn {
  transform: scale(0.9);
}

/* Special Button Styles */
.fab-icon-btn.gold {
  color: #b4821e;
  background: #fffdf9;
  border-color: rgba(212, 175, 55, 0.2);
}
.fab-icon-btn.blue {
  color: #0ea5e9;
  background: #f0f9ff;
  border-color: rgba(14, 165, 233, 0.2);
}
</style>
