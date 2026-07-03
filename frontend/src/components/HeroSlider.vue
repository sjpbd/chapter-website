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
    accent: '#0078d4',
    media_type: 'image'
  },
  {
    id: 's2',
    title: 'Preserving Our History',
    subtitle: 'Access decades of provincial wisdom, legislative records, and community milestones.',
    image: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=2000&q=80',
    link: '/repository',
    accent: '#5c2d91',
    media_type: 'image'
  },
  {
    id: 's3',
    title: 'Download Official Documents',
    subtitle: 'PDFs, DOC files and more — all organized, searchable, and securely available.',
    image: 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=2000&q=80',
    link: '/repository',
    accent: '#107c10',
    media_type: 'image'
  }
]

const activeSlides = computed(() => {
  const rawSlides = props.slides.length ? props.slides : defaultSlides
  return rawSlides.map(slide => ({
    ...slide,
    media_type: slide.media_type || 'image'
  }))
})

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
        :key="slide.id || i"
        :class="['slide', { active: i === current }]"
      >
        <!-- Background Media Container -->
        <div class="media-container">
          <!-- Video slide -->
          <video
            v-if="slide.media_type === 'video' && slide.video"
            :src="slide.video"
            :poster="slide.image"
            autoplay
            loop
            muted
            playsinline
            class="slide-media slide-video"
          ></video>
          <!-- Image slide -->
          <div
            v-else
            class="slide-media slide-image"
            :style="{ backgroundImage: `url(${slide.image})` }"
          ></div>
        </div>

        <!-- Dynamic Overlay -->
        <div 
          class="slide-overlay" 
          :style="{ 
            background: `linear-gradient(135deg, ${(slide.accent || '#0078d4')}44 0%, rgba(10, 18, 30, 0.85) 100%)` 
          }"
        ></div>

        <!-- Slide content with staggered animations -->
        <div class="slide-content-wrapper">
          <div class="slide-card glass">
            <p class="slide-eyebrow">St. Joseph Province · Official</p>
            <h1 class="slide-title">
              <span class="gradient-text" :style="{ '--accent-color': slide.accent || '#0078d4' }">
                {{ slide.title }}
              </span>
            </h1>
            <p class="slide-subtitle">{{ slide.subtitle }}</p>
            <div class="slide-actions">
              <RouterLink 
                :to="slide.link || '/repository'" 
                class="btn-hero-primary"
                :style="{ '--accent-color': slide.accent || '#0078d4' }"
              >
                <span>Explore Now</span>
                <ArrowRight :size="18" />
              </RouterLink>
            </div>
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

    <!-- Sleek bottom progress bar -->
    <div class="progress-bar">
      <div :key="current" class="progress-fill" :style="{ background: activeSlides[current]?.accent || '#0078d4' }"></div>
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
  background: #0a121e;
}

.slides-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 1.2s cubic-bezier(0.25, 1, 0.5, 1);
  display: flex;
  align-items: center;
  z-index: 1;
}

.slide.active {
  opacity: 1;
  z-index: 2;
}

/* Background Media Container */
.media-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 1;
}

.slide-media {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 8s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-image {
  background-size: cover;
  background-position: center;
  transform: scale(1.05);
}

/* Ken Burns effect: subtle slow zoom on the active slide */
.slide.active .slide-image {
  transform: scale(1.12);
}

.slide-video {
  pointer-events: none;
}

/* Gradient Overlay */
.slide-overlay {
  position: absolute;
  inset: 0;
  z-index: 2;
  transition: background 1.2s ease;
}

/* Content Container */
.slide-content-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 4rem;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

/* Glassmorphism Card styling */
.slide-card {
  max-width: 620px;
  background: rgba(10, 18, 30, 0.45);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 3.5rem;
  border-radius: 24px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.45),
              inset 0 1px 1px rgba(255, 255, 255, 0.1);
  transform: translateY(40px);
  opacity: 0;
  transition: all 0.9s cubic-bezier(0.34, 1.3, 0.64, 1);
}

.slide.active .slide-card {
  transform: translateY(0);
  opacity: 1;
}

.slide-eyebrow {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 1.2rem;
}

.slide-title {
  font-size: clamp(2rem, 4.5vw, 3.6rem);
  font-weight: 800;
  line-height: 1.15;
  margin-bottom: 1.4rem;
  color: white;
}

.gradient-text {
  background: linear-gradient(
    135deg, 
    #ffffff 0%, 
    #f3f4f6 40%, 
    var(--accent-color, #0078d4) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.slide-subtitle {
  font-size: clamp(0.95rem, 1.8vw, 1.15rem);
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.7;
  margin-bottom: 2.2rem;
}

.slide-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Staggered entrance animations */
.slide-eyebrow,
.slide-title,
.slide-subtitle,
.slide-actions {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide.active .slide-eyebrow {
  opacity: 0.75;
  transform: translateY(0);
  transition-delay: 0.2s;
}

.slide.active .slide-title {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.35s;
}

.slide.active .slide-subtitle {
  opacity: 0.85;
  transform: translateY(0);
  transition-delay: 0.5s;
}

.slide.active .slide-actions {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.65s;
}

/* Premium Button styling */
.btn-hero-primary {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 1rem 2.2rem;
  background: white;
  color: #0a121e;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.btn-hero-primary span,
.btn-hero-primary svg {
  position: relative;
  z-index: 2;
}

.btn-hero-primary::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--accent-color, #0078d4) 0%, rgba(10, 18, 30, 0.8) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: 1;
}

.btn-hero-primary:hover {
  transform: translateY(-3px) scale(1.02);
  color: white;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35),
              0 0 20px rgba(255, 255, 255, 0.15);
}

.btn-hero-primary:hover::before {
  opacity: 1;
}

/* Navigation Arrows */
.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 20;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(10, 18, 30, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.arrow:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}

.arrow-prev { left: 2rem; }
.arrow-next { right: 2rem; }

/* Navigation Dots */
.dots {
  position: absolute;
  bottom: 2.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  z-index: 20;
}

.dot {
  height: 10px;
  width: 10px;
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.25);
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  border: none;
  cursor: pointer;
  padding: 0;
}

.dot:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: scale(1.2);
}

.dot.active {
  background: white;
  width: 36px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

/* Progress fill animation */
.progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  z-index: 20;
}

.progress-fill {
  height: 100%;
  animation: progress 6s linear;
  transform-origin: left;
}

@keyframes progress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

@media (max-width: 900px) {
  .slide-content-wrapper { padding: 0 2rem; }
  .slide-card { padding: 2.5rem; }
}

@media (max-width: 768px) {
  .slide-card { padding: 2rem 1.5rem; border-radius: 16px; margin: 0 1rem; }
  .arrow { display: none; }
  .slide-content-wrapper { padding: 0 1rem; }
}
</style>
