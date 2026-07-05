<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useConfigStore } from './store/configStore'
import Navbar from './components/Navbar.vue'
import SiteFooter from './components/SiteFooter.vue'
import WelcomeTour from './components/WelcomeTour.vue'
import { Compass, Home, FolderOpen, HandHeart, CalendarDays, X, Vote } from 'lucide-vue-next'

const configStore = useConfigStore()
const isFabMenuOpen = ref(false)
const route = useRoute()

const isVoteWidgetClosed = ref(localStorage.getItem('sjp_vote_widget_dismissed') === 'true')
const dismissVoteWidget = () => {
  isVoteWidgetClosed.value = true
  localStorage.setItem('sjp_vote_widget_dismissed', 'true')
}

onMounted(() => {
  configStore.fetchConfig()
})
</script>

<template>
  <div id="app-shell">
    <Navbar />
    <WelcomeTour />
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
        <a 
          href="https://vote.sjp.org.bd" 
          target="_blank" 
          rel="noopener noreferrer" 
          class="fab-action-item" 
          @click="isFabMenuOpen = false"
        >
          <span class="fab-label">Vote Now</span>
          <div class="fab-icon-btn red"><Vote :size="20" /></div>
        </a>
      </div>

      <!-- Trigger Button -->
      <button class="fab-trigger" @click="isFabMenuOpen = !isFabMenuOpen" aria-label="Toggle Quick Navigation">
        <X v-if="isFabMenuOpen" :size="24" class="icon-close" />
        <Compass v-else :size="24" class="icon-compass" />
      </button>
    </div>

    <!-- Floating Voting Widget (Desktop/Tablet) -->
    <Transition name="slide-up">
      <div v-if="!isVoteWidgetClosed" class="vote-floating-widget glass">
        <button class="close-widget-btn" @click="dismissVoteWidget" aria-label="Dismiss voting widget">
          <X :size="14" />
        </button>
        <div class="widget-header">
          <span class="pulse-indicator"></span>
          <span class="widget-badge">Election Live</span>
        </div>
        <div class="widget-body">
          <h4 class="widget-title">SJP Election 2026</h4>
          <p class="widget-text">Cast your vote online in the official St. Joseph Province voting portal.</p>
        </div>
        <a 
          href="https://vote.sjp.org.bd" 
          target="_blank" 
          rel="noopener noreferrer" 
          class="widget-action-btn"
        >
          <span>Vote Now</span>
          <Vote :size="16" />
        </a>
      </div>
    </Transition>
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
.fab-action-item:nth-child(1) { transition-delay: 0.24s; }
.fab-action-item:nth-child(2) { transition-delay: 0.18s; }
.fab-action-item:nth-child(3) { transition-delay: 0.12s; }
.fab-action-item:nth-child(4) { transition-delay: 0.06s; }
.fab-action-item:nth-child(5) { transition-delay: 0s; }

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

.fab-icon-btn.red {
  color: #ef4444;
  background: #fef2f2;
  border-color: rgba(239, 68, 68, 0.2);
}

/* Floating Widget Styles */
.vote-floating-widget {
  position: fixed;
  left: 32px;
  bottom: 32px;
  z-index: 1500;
  width: 320px;
  padding: 1.5rem;
  border-radius: 20px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  background: rgba(255, 255, 255, 0.75);
}

@media (max-width: 768px) {
  .vote-floating-widget {
    display: none; /* Hide on mobile to avoid UI clutter */
  }
}

.close-widget-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-smooth);
}

.close-widget-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pulse-indicator {
  width: 8px;
  height: 8px;
  background-color: #22c55e;
  border-radius: 50%;
  position: relative;
}

.pulse-indicator::after {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  border-radius: 50%;
  background-color: #22c55e;
  animation: ripple 1.6s infinite ease-out;
}

.widget-badge {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #15803d;
  letter-spacing: 0.05em;
}

.widget-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 2px;
  color: var(--text-main);
}

.widget-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.widget-action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px;
  background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
  color: white !important;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9rem;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  margin-top: 4px;
}

.widget-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(239, 68, 68, 0.35);
  background: linear-gradient(135deg, #f43f5e 0%, #fb7185 100%);
}

/* Widget slide transition */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(40px) scale(0.9);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(40px) scale(0.9);
}
</style>
