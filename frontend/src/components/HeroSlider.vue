<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { ChevronLeft, ChevronRight, ArrowRight } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'

const props = defineProps({
  slides: { type: Array, default: () => [] }
})

// Fallback slides if none from API yet
const defaultSlides = [
  {
    id: 's1',
    title: 'Welcome to SJP Chapter Hub',
    subtitle: 'Your trusted digital repository for St. Joseph Province official chapter materials and records.',
    image: 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=2000&q=80',
    link: '/repository',
    accent: '#0078d4'
  },
  {
    id: 's2',
    title: 'Preserving Our History',
    subtitle: 'Access decades of provincial wisdom, legislative records, and community milestones.',
    image: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=2000&q=80',
    link: '/repository',
    accent: '#5c2d91'
  },
  {
    id: 's3',
    title: 'Download Official Documents',
    subtitle: 'PDFs, DOC files and more — all organized, searchable, and securely available.',
    image: 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=2000&q=80',
    link: '/repository',
    accent: '#107c10'
  }
]

const activeSlides = computed(() => props.slides.length ? props.slides : defaultSlides)
const current = ref(0)
const isTransitioning = ref(false)
let timer = null

const go = (idx) => {
  if (isTransitioning.value) return
  isTransitioning.value = true
  current.value = (idx + activeSlides.value.length) % activeSlides.value.length
  setTimeout(() => { isTransitioning.value = false }, 900)
}

const next = () => go(current.value + 1)
const prev = () => go(current.value - 1)
const resetTimer = () => { clearInterval(timer); timer = setInterval(next, 6000) }

watch(current, resetTimer)
onMounted(resetTimer)
onUnmounted(() => clearInterval(timer))
</script>

<template>
  <section class="hero-slider">
    <div class="slides-wrapper">
      <div
        v-for="(slide, i) in activeSlides"
        :key="slide.id"
        :class="['slide', { active: i === current }]"
        :style="{ backgroundImage: `url(${slide.image})` }"
      >
        <div class="slide-overlay" :style="{ background: `linear-gradient(135deg, ${slide.accent || '#0078d4'}cc 0%, rgba(0,0,0,0.65) 100%)` }"></div>
        <div class="slide-content">
          <p class="slide-eyebrow">St. Joseph Province · Official</p>
          <h1 class="slide-title">{{ slide.title }}</h1>
          <p class="slide-subtitle">{{ slide.subtitle }}</p>
          <div class="slide-actions">
            <RouterLink :to="slide.link || '/repository'" class="btn-hero-primary">
              Explore Now <ArrowRight :size="18" />
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Arrows -->
    <button class="arrow arrow-prev" @click="prev" aria-label="Previous slide">
      <ChevronLeft :size="28" />
    </button>
    <button class="arrow arrow-next" @click="next" aria-label="Next slide">
      <ChevronRight :size="28" />
    </button>

    <!-- Dots -->
    <div class="dots" role="tablist">
      <button
        v-for="(_, i) in activeSlides"
        :key="i"
        :class="['dot', { active: i === current }]"
        @click="go(i)"
        :aria-label="`Go to slide ${i + 1}`"
        role="tab"
      ></button>
    </div>

    <!-- Progress bar -->
    <div class="progress-bar">
      <div :key="current" class="progress-fill"></div>
    </div>
  </section>
</template>

<style scoped>
.hero-slider {
  position: relative;
  width: 100%;
  height: calc(100vh - 72px);
  min-height: 520px;
  max-height: 900px;
  overflow: hidden;
  background: #0d1b2a;
}

.slides-wrapper {
  position: relative;
  width: 100%; height: 100%;
}

.slide {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity 1s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.slide.active { opacity: 1; }

.slide-overlay {
  position: absolute;
  inset: 0;
}

.slide-content {
  position: relative;
  z-index: 10;
  max-width: 680px;
  padding: 3rem 4rem;
  animation: fadeInUp 0.9s cubic-bezier(0.4,0,0.2,1) both;
}

.slide-eyebrow {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.75);
  margin-bottom: 1.2rem;
}

.slide-title {
  font-size: clamp(2.2rem, 5vw, 4rem);
  font-weight: 800;
  color: white;
  line-height: 1.1;
  margin-bottom: 1.4rem;
  text-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.slide-subtitle {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: rgba(255,255,255,0.88);
  line-height: 1.7;
  margin-bottom: 2.5rem;
  max-width: 520px;
}

.slide-actions { display: flex; gap: 1rem; flex-wrap: wrap; }

.btn-hero-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 1rem 2.2rem;
  background: white;
  color: var(--primary-dark);
  border-radius: 50px;
  font-weight: 800;
  font-size: 1rem;
  box-shadow: 0 12px 32px rgba(0,0,0,0.25);
  transition: var(--transition-spring);
}

.btn-hero-primary:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

/* Arrows */
.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 50;
  width: 56px; height: 56px;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
  border: 1.5px solid rgba(255,255,255,0.25);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(12px);
  transition: var(--transition-smooth);
}

.arrow:hover {
  background: rgba(255,255,255,0.25);
  transform: translateY(-50%) scale(1.1);
}

.arrow-prev { left: 2rem; }
.arrow-next { right: 2rem; }

/* Dots */
.dots {
  position: absolute;
  bottom: 2.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 50;
}

.dot {
  height: 8px;
  border-radius: 50px;
  background: rgba(255,255,255,0.4);
  transition: var(--transition-smooth);
  width: 8px;
  border: none;
  cursor: pointer;
}

.dot.active {
  background: white;
  width: 32px;
}

/* Progress */
.progress-bar {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 3px;
  background: rgba(255,255,255,0.15);
  z-index: 50;
}

.progress-fill {
  height: 100%;
  background: white;
  animation: progress 6s linear;
}

@keyframes progress {
  from { width: 0; }
  to   { width: 100%; }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(32px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .slide-content { padding: 2rem 1.5rem; }
  .arrow { display: none; }
}
</style>
