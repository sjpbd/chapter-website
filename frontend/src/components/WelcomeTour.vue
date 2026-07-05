<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Sparkles, X, ArrowRight, ArrowLeft, CheckCircle2 } from 'lucide-vue-next'

const isOpen = ref(false)
const currentStep = ref(0) // 0: Welcome, 1: Repository, 2: Prayer
const spotlightRect = ref({ x: 0, y: 0, w: 0, h: 0 })
const cardStyle = ref({ top: '50%', left: '50%', transform: 'translate(-50%, -50%)', position: 'fixed' })
const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 1024
}

// Dynamic steps based on screen size (desktop vs. mobile text)
const steps = computed(() => [
  {
    title: "Welcome to SJP Chapter Hub",
    description: "The official digital gateway for St. Joseph Province records. Let us show you where to find the key sections of our hub.",
    target: null
  },
  {
    title: "📂 Document Repository",
    description: isMobile.value 
      ? "Tap the menu button in the header (or the floating compass at the bottom right) and select 'Repository' to search, filter, and view all official province documents."
      : "Click here to browse, search, and download official chapter documents, legislative records, and provincial materials.",
    target: {
      desktop: "#tour-nav-repository",
      mobile: ".burger-btn"
    }
  },
  {
    title: "🙏 Chapter Prayer",
    description: isMobile.value
      ? "Tap the menu button in the header (or the floating compass at the bottom right) and select 'Prayer' to access and view the official Chapter Prayer."
      : "Click here to access, download, or read the official Chapter Prayer of the Province, beautifully formatted for reflection.",
    target: {
      desktop: "#tour-nav-prayer",
      mobile: ".burger-btn"
    }
  },
  {
    title: "📅 Daily Schedule",
    description: isMobile.value
      ? "Tap the menu button in the header (or the floating compass at the bottom right) and select 'Schedule' to view the daily program timetable of the Chapter."
      : "Click here to view the full timetable of sessions, liturgies, meals, and social activities for the Provincial Chapter.",
    target: {
      desktop: "#tour-nav-schedule",
      mobile: ".burger-btn"
    }
  }
])

const updateSpotlight = () => {
  if (currentStep.value === 0) {
    // Welcome step has no spotlight
    spotlightRect.value = { x: 0, y: 0, w: 0, h: 0 }
    cardStyle.value = {
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: 'calc(100vw - 32px)',
      maxWidth: '340px',
      zIndex: 2001
    }
    return
  }

  const step = steps.value[currentStep.value]
  const selector = isMobile.value ? step.target.mobile : step.target.desktop
  const el = document.querySelector(selector)

  if (el) {
    const rect = el.getBoundingClientRect()
    const padding = 8
    
    spotlightRect.value = {
      x: rect.left - padding,
      y: rect.top - padding,
      w: rect.width + padding * 2,
      h: rect.height + padding * 2
    }

    const cardWidth = Math.min(340, window.innerWidth - 32)
    let leftPos = rect.left + rect.width / 2 - cardWidth / 2
    const screenPadding = 16

    // Prevent popover from clipping past left/right viewport boundaries
    if (leftPos < screenPadding) {
      leftPos = screenPadding
    } else if (leftPos + cardWidth > window.innerWidth - screenPadding) {
      leftPos = window.innerWidth - cardWidth - screenPadding
    }

    // Position popover below target on desktop, or adjusted for mobile viewports
    const topPos = rect.bottom + 16
    
    cardStyle.value = {
      position: 'fixed',
      top: `${topPos}px`,
      left: `${leftPos}px`,
      width: `${cardWidth}px`,
      zIndex: 2001,
      transform: 'none'
    }
  } else {
    // Fallback if target element is not found
    spotlightRect.value = { x: 0, y: 0, w: 0, h: 0 }
    cardStyle.value = {
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      zIndex: 2001
    }
  }
}

const nextStep = () => {
  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++
  } else {
    finishTour()
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const finishTour = () => {
  isOpen.value = false
  localStorage.setItem('sjp_guide_completed', 'true')
}

const startTour = () => {
  checkMobile()
  currentStep.value = 0
  isOpen.value = true
  nextTick(() => {
    updateSpotlight()
  })
}

// Listener for manual tour replay (e.g. from navbar or drawer)
const handleStartTourEvent = () => {
  startTour()
}

onMounted(() => {
  window.addEventListener('start-sjp-tour', handleStartTourEvent)
  window.addEventListener('resize', () => {
    checkMobile()
    if (isOpen.value) updateSpotlight()
  })
  
  // Recalculate spotlight dynamically on scroll to handle sticky navigation transitions
  window.addEventListener('scroll', () => {
    if (isOpen.value) updateSpotlight()
  }, { passive: true })

  // Auto-trigger on first visit after a slight delay for loading aesthetic elements
  const completed = localStorage.getItem('sjp_guide_completed')
  if (!completed) {
    setTimeout(() => {
      startTour()
    }, 1800)
  }
})

onUnmounted(() => {
  window.removeEventListener('start-sjp-tour', handleStartTourEvent)
})

watch(currentStep, () => {
  updateSpotlight()
})
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="tour-overlay-container">
      <!-- SVG Spotlight Overlay -->
      <svg class="tour-svg-overlay">
        <defs>
          <mask id="tour-spotlight-mask">
            <!-- White reveals overlay backdrop -->
            <rect x="0" y="0" width="100%" height="100%" fill="white" />
            <!-- Black cuts hole to spotlight active element -->
            <rect 
              :x="spotlightRect.x" 
              :y="spotlightRect.y" 
              :width="spotlightRect.w" 
              :height="spotlightRect.h" 
              rx="12" 
              ry="12" 
              fill="black" 
              class="spotlight-rect"
            />
          </mask>
        </defs>
        <!-- Overlay background applying mask -->
        <rect 
          x="0" 
          y="0" 
          width="100%" 
          height="100%" 
          fill="rgba(10, 18, 30, 0.65)" 
          mask="url(#tour-spotlight-mask)"
          @click="finishTour"
        />
      </svg>

      <!-- Pulse Effect Around Spotlight -->
      <div 
        v-if="currentStep > 0 && spotlightRect.w > 0"
        class="spotlight-pulse"
        :style="{
          top: `${spotlightRect.y}px`,
          left: `${spotlightRect.x}px`,
          width: `${spotlightRect.w}px`,
          height: `${spotlightRect.h}px`
        }"
      ></div>

      <!-- Tour Content Card -->
      <div class="tour-card-positioner" :style="cardStyle">
        <div class="tour-card glass">
          <!-- Close button -->
          <button class="tour-close-btn" @click="finishTour" aria-label="Close guide">
            <X :size="16" />
          </button>

          <!-- Card Content -->
          <div class="tour-card-body">
            <div class="tour-step-badge">
              <Sparkles :size="12" class="spark-icon" />
              <span>{{ currentStep === 0 ? 'Quick Guide' : `Step ${currentStep} of ${steps.length - 1}` }}</span>
            </div>

            <h3 class="tour-title">
              <span v-if="currentStep === 0" class="gradient-text-tour">{{ steps[currentStep].title }}</span>
              <span v-else>{{ steps[currentStep].title }}</span>
            </h3>
            
            <p class="tour-description">{{ steps[currentStep].description }}</p>
          </div>

          <!-- Actions Footer -->
          <div class="tour-actions">
            <button 
              v-if="currentStep > 0" 
              class="tour-btn btn-secondary" 
              @click="prevStep"
            >
              <ArrowLeft :size="15" />
              <span>Back</span>
            </button>
            <button 
              v-else 
              class="tour-btn btn-text" 
              @click="finishTour"
            >
              Skip Guide
            </button>

            <button 
              class="tour-btn btn-primary-tour" 
              @click="nextStep"
            >
              <span>{{ currentStep === steps.length - 1 ? 'Finish' : (currentStep === 0 ? 'Start Tour' : 'Next') }}</span>
              <ArrowRight v-if="currentStep < steps.length - 1" :size="15" />
              <CheckCircle2 v-else :size="15" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.tour-overlay-container {
  position: fixed;
  inset: 0;
  z-index: 1999;
  pointer-events: auto;
}

.tour-svg-overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.spotlight-rect {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Dynamic pulse ring around active menu spotlight */
.spotlight-pulse {
  position: fixed;
  pointer-events: none;
  border: 2px solid #2b88d8;
  border-radius: 14px;
  z-index: 2000;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  animation: pulse-ring 2s infinite;
}

@keyframes pulse-ring {
  0% {
    box-shadow: 0 0 0 0px rgba(0, 106, 220, 0.55), 0 0 10px rgba(0, 106, 220, 0.3);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(0, 106, 220, 0), 0 0 15px rgba(0, 106, 220, 0);
  }
  100% {
    box-shadow: 0 0 0 0px rgba(0, 106, 220, 0), 0 0 0px rgba(0, 106, 220, 0);
  }
}

.tour-card-positioner {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Onboarding Card styling */
.tour-card {
  position: relative;
  width: 100%;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(24px) saturate(190%);
  -webkit-backdrop-filter: blur(24px) saturate(190%);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 24px;
  padding: 1.6rem;
  box-shadow: 0 20px 50px rgba(0, 106, 220, 0.12),
              0 6px 18px rgba(0, 0, 0, 0.04);
}

.tour-close-btn {
  position: absolute;
  top: 1.1rem;
  right: 1.1rem;
  background: rgba(15, 23, 42, 0.05);
  color: var(--text-secondary);
  border-radius: 50%;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.tour-close-btn:hover {
  background: #fee2e2;
  color: #dc2626;
  transform: rotate(90deg);
}

.tour-card-body {
  margin-top: 0.2rem;
}

.tour-step-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  background: linear-gradient(135deg, rgba(0, 106, 220, 0.08) 0%, rgba(99, 46, 155, 0.08) 100%);
  border: 1px solid rgba(0, 106, 220, 0.15);
  border-radius: 50px;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.spark-icon {
  animation: spark-float 3s ease-in-out infinite;
}

@keyframes spark-float {
  0% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-2px) scale(1.1); }
  100% { transform: translateY(0) scale(1); }
}

.tour-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 0.6rem;
  color: var(--text-main);
  line-height: 1.3;
}

.gradient-text-tour {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.tour-description {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1.4rem;
}

.tour-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-top: 1px solid rgba(15, 23, 42, 0.06);
  padding-top: 1rem;
}

.tour-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
  font-size: 0.85rem;
  border-radius: 50px;
  padding: 0.55rem 1.15rem;
  transition: all 0.2s ease;
}

.btn-primary-tour {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  box-shadow: 0 4px 12px rgba(0, 106, 220, 0.2);
  margin-left: auto;
}
.btn-primary-tour:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 106, 220, 0.3);
}

.btn-secondary {
  background: rgba(15, 23, 42, 0.03);
  color: var(--text-secondary);
  border: 1px solid rgba(15, 23, 42, 0.08);
}
.btn-secondary:hover {
  background: rgba(15, 23, 42, 0.06);
}

.btn-text {
  background: transparent;
  color: var(--text-light);
  padding-left: 0;
  padding-right: 0;
}
.btn-text:hover {
  color: var(--text-secondary);
}

/* Fade Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.fade-enter-active .tour-card {
  animation: card-scale-up 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.fade-leave-active .tour-card {
  animation: card-scale-down 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes card-scale-up {
  from { opacity: 0; transform: scale(0.92) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes card-scale-down {
  from { opacity: 1; transform: scale(1) translateY(0); }
  to { opacity: 0; transform: scale(0.92) translateY(10px); }
}
</style>
