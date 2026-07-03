<script setup>
import { ref, onMounted, computed } from 'vue'
import { RefreshCw, Download } from 'lucide-vue-next'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const prayer = ref(null)
const loading = ref(true)
const error = ref(null)
const isFlipped = ref(false)

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/prayer/`)
    if (!res.ok) throw new Error('Could not load prayer.')
    prayer.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

// Split body on blank lines to render as distinct stanzas
const stanzas = computed(() => {
  if (!prayer.value?.body) return []
  return prayer.value.body.split(/\n\s*\n/).map(s => s.trim()).filter(Boolean)
})

const hasFrontImage = computed(() => !!prayer.value?.front_image)
const hasBackImage = computed(() => !!prayer.value?.back_image)

const toggleFlip = () => {
  isFlipped.value = !isFlipped.value
}
</script>

<template>
  <main class="prayer-page">

    <!-- Ambient background elements -->
    <div class="ambient-orb orb-gold"></div>
    <div class="ambient-orb orb-purple"></div>
    <div class="ambient-orb orb-blue"></div>

    <!-- Decorative crosses -->
    <div class="deco-cross cross-tl" aria-hidden="true">✝</div>
    <div class="deco-cross cross-br" aria-hidden="true">✝</div>

    <!-- ─── HERO HEADER ─────────────────────────────────────── -->
    <header class="prayer-hero">
      <!-- Title block -->
      <div class="hero-text">
        <span class="eyebrow-label">Spiritual Reflection</span>
        <h1 class="hero-title" v-if="prayer">{{ prayer.title }}</h1>
        <h1 class="hero-title" v-else-if="loading">Loading Prayer…</h1>
        <h1 class="hero-title" v-else>Prayer for the Chapter 2027</h1>
        <p class="hero-subtitle" v-if="prayer">{{ prayer.subtitle }}</p>
      </div>

      <!-- Gold divider -->
      <div class="gold-divider">
        <span class="divider-ornament">❧</span>
      </div>
    </header>

    <!-- ─── PRAYER CONTENT SECTION ───────────────────────────── -->
    <section class="prayer-content-wrap">
      
      <!-- Interactive 3D Flipping Card -->
      <div v-if="!loading && !error && prayer && hasFrontImage" class="interactive-card-wrapper">
        <div class="flip-card-container" @click="toggleFlip">
          <div :class="['flip-card-inner', { 'is-flipped': isFlipped }]">
            
            <!-- FRONT SIDE -->
            <div class="card-face card-face-front">
              <div class="gilded-border"></div>
              <img :src="prayer.front_image" class="card-media-file" alt="Prayer Card Front Cover" />
              <div class="card-hint">
                <span>Click to Flip Card</span>
                <RefreshCw :size="14" class="hint-icon" />
              </div>
            </div>

            <!-- BACK SIDE -->
            <div class="card-face card-face-back">
              <div class="gilded-border"></div>
              
              <!-- Back Side Image -->
              <img v-if="hasBackImage" :src="prayer.back_image" class="card-media-file" alt="Prayer Card Back" />
              
              <!-- Back Side Text Fallback -->
              <div v-else class="card-text-fallback">
                <div class="scroll-area">
                  <div class="opening-verse">
                    <em>"Ask and it shall be given to you; seek and you shall find;
                    knock and the door shall be opened to you."</em>
                    <span class="verse-ref">— Matthew 7:7</span>
                  </div>
                  
                  <div class="prayer-body">
                    <p
                      v-for="(stanza, i) in stanzas"
                      :key="i"
                      class="stanza"
                      :class="{ 'stanza-amen': stanza.toLowerCase() === 'amen.' }"
                      v-html="stanza.replace(/\n/g, '<br/>')"
                    ></p>
                  </div>

                  <footer class="prayer-footer">
                    <div class="footer-cross">✝</div>
                    <p class="attribution">{{ prayer.author_attribution }}</p>
                    <p class="chapter-year">Chapter · 2027</p>
                  </footer>
                </div>
              </div>

            </div>

          </div>
        </div>

        <!-- Controls below 3D Card -->
        <div class="card-controls">
          <button class="btn-flip" @click="toggleFlip">
            <RefreshCw :size="18" />
            <span>Flip Card</span>
          </button>
          
          <div class="download-actions">
            <a :href="prayer.front_image" download target="_blank" class="btn-download">
              <Download :size="16" />
              <span>Download Front Image</span>
            </a>
            <a v-if="hasBackImage" :href="prayer.back_image" download target="_blank" class="btn-download">
              <Download :size="16" />
              <span>Download Back Image</span>
            </a>
          </div>
        </div>

      </div>

      <!-- Static Elegant Text Card (Fallback if no front image is uploaded) -->
      <article class="prayer-card static-card" v-else-if="!loading && !error && prayer">
        <!-- Opening verse -->
        <div class="opening-verse">
          <em>"Ask and it shall be given to you; seek and you shall find;
          knock and the door shall be opened to you."</em>
          <span class="verse-ref">— Matthew 7:7</span>
        </div>

        <!-- Prayer stanzas -->
        <div class="prayer-body">
          <p
            v-for="(stanza, i) in stanzas"
            :key="i"
            class="stanza"
            :class="{ 'stanza-amen': stanza.toLowerCase() === 'amen.' }"
            v-html="stanza.replace(/\n/g, '<br/>')"
          ></p>
        </div>

        <!-- Attribution / Footer -->
        <footer class="prayer-footer">
          <div class="footer-cross">✝</div>
          <p class="attribution">{{ prayer.author_attribution }}</p>
          <p class="chapter-year">Chapter · 2027</p>
        </footer>
      </article>

      <!-- Loading state -->
      <div v-else-if="loading" class="state-block">
        <div class="spinner"></div>
        <p>Loading the prayer…</p>
      </div>

      <!-- Error state -->
      <div v-else class="state-block state-error">
        <div class="error-icon">🕯️</div>
        <p>The prayer could not be loaded.<br/>Please try again shortly.</p>
      </div>

    </section>

    <!-- Rosary bead decoration row -->
    <div class="rosary-row" aria-hidden="true">
      <span v-for="n in 19" :key="n" class="bead" :class="{ 'bead-lg': n % 6 === 0 }"></span>
    </div>

  </main>
</template>

<style scoped>
/* ─── PAGE ──────────────────────────────────────────────────── */
.prayer-page {
  min-height: 100vh;
  padding-top: 72px; /* navbar height */
  background:
    radial-gradient(ellipse 80% 60% at 50% 0%, rgba(180, 130, 30, 0.18) 0%, transparent 65%),
    radial-gradient(ellipse 60% 50% at 10% 80%, rgba(99, 46, 155, 0.12) 0%, transparent 60%),
    radial-gradient(ellipse 70% 60% at 90% 70%, rgba(0, 106, 220, 0.08) 0%, transparent 60%),
    #f8f4ef;
  position: relative;
  overflow: hidden;
}

/* ─── AMBIENT ORBS ──────────────────────────────────────────── */
.ambient-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(80px);
  opacity: 0.45;
  animation: orbFloat 12s ease-in-out infinite;
}
.orb-gold   { width: 420px; height: 420px; top: -80px; left: 50%; transform: translateX(-50%); background: radial-gradient(circle, #f5c842, #e8920a); }
.orb-purple { width: 280px; height: 280px; bottom: 20%; left: -80px; background: radial-gradient(circle, #9b59b6, #6c3483); animation-delay: -4s; }
.orb-blue   { width: 220px; height: 220px; bottom: 10%; right: -60px; background: radial-gradient(circle, #3498db, #1a5276); animation-delay: -8s; }

@keyframes orbFloat {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50%       { transform: translateX(-50%) translateY(-30px); }
}
.orb-purple { animation-name: orbFloatL; }
.orb-blue   { animation-name: orbFloatR; }
@keyframes orbFloatL { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
@keyframes orbFloatR { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(20px); } }

/* ─── DECORATIVE CROSSES ─────────────────────────────────────── */
.deco-cross {
  position: absolute;
  font-size: 6rem;
  color: rgba(180, 130, 30, 0.08);
  font-family: serif;
  pointer-events: none;
  user-select: none;
}
.cross-tl { top: 80px; left: 2%; }
.cross-br { bottom: 100px; right: 2%; }

/* ─── HERO ───────────────────────────────────────────────────── */
.prayer-hero {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4rem 2rem 0;
  gap: 1.5rem;
}

/* Hero text */
.hero-text { position: relative; z-index: 1; }

.eyebrow-label {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #b07d12;
  background: linear-gradient(135deg, rgba(245,200,66,0.25), rgba(220,170,30,0.15));
  border: 1px solid rgba(180,130,30,0.3);
  padding: 6px 20px;
  border-radius: 50px;
  margin-bottom: 1.2rem;
}

.hero-title {
  font-family: 'Outfit', Georgia, serif;
  font-size: clamp(1.6rem, 4.5vw, 3rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #7a4e00, #c8860a, #7a4e00);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: goldShimmer 4s linear infinite;
  line-height: 1.2;
  max-width: 700px;
  margin: 0 auto 0.8rem;
}

@keyframes goldShimmer {
  0%   { background-position: 0% center; }
  100% { background-position: 200% center; }
}

.hero-subtitle {
  font-size: 1.05rem;
  color: #7a5c1e;
  font-style: italic;
  letter-spacing: 0.03em;
}

/* Divider */
.gold-divider {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 600px;
  gap: 1rem;
  margin: 0.5rem 0 0;
}
.gold-divider::before,
.gold-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, #c8860a, transparent);
}
.divider-ornament {
  font-size: 1.4rem;
  color: #b07d12;
  line-height: 1;
}

/* ─── PRAYER CONTENT SECTION ───────────────────────────── */
.prayer-content-wrap {
  position: relative;
  z-index: 2;
  max-width: 840px;
  margin: 3rem auto 2rem;
  padding: 0 1.5rem;
}

/* Static elegant card & general prayer card styles */
.prayer-card {
  background: rgba(255, 251, 242, 0.85);
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  border: 1px solid rgba(200, 160, 50, 0.3);
  border-radius: 28px;
  padding: 3rem 3.5rem;
  box-shadow:
    0 4px 6px -1px rgba(0,0,0,0.04),
    0 20px 50px rgba(180, 130, 30, 0.12),
    inset 0 1px 0 rgba(255,255,255,0.8);
  animation: scaleIn 0.7s cubic-bezier(0.16,1,0.3,1);
  position: relative;
  overflow: hidden;
}

.static-card::before {
  content: '✝';
  position: absolute;
  top: 1.5rem;
  right: 2rem;
  font-size: 1.2rem;
  color: rgba(180, 130, 30, 0.25);
  font-family: serif;
}
.static-card::after {
  content: '✝';
  position: absolute;
  bottom: 1.5rem;
  left: 2rem;
  font-size: 1.2rem;
  color: rgba(180, 130, 30, 0.25);
  font-family: serif;
}

/* 3D Flip Card Styles */
.interactive-card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2.5rem;
  animation: scaleIn 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}

.flip-card-container {
  width: 100%;
  max-width: 400px;
  aspect-ratio: 3 / 4.6;
  perspective: 1800px;
  cursor: pointer;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-style: preserve-3d;
}

.flip-card-inner.is-flipped {
  transform: rotateY(180deg);
}

.card-face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.15), 
    0 5px 15px rgba(180, 130, 30, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.35);
  background: #fbf8f3;
}

/* Gilded frame overlay for card face */
.gilded-border {
  position: absolute;
  inset: 12px;
  border: 2.5px double rgba(212, 175, 55, 0.45);
  border-radius: 14px;
  pointer-events: none;
  z-index: 5;
}

.card-face-front {
  z-index: 2;
  transform: rotateY(0deg);
}

.card-face-back {
  transform: rotateY(180deg);
  background: #f8f5ee;
}

.card-media-file {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Hover flip hint */
.card-hint {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 6;
  background: rgba(10, 18, 30, 0.65);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: white;
  padding: 8px 16px;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease, transform 0.3s ease;
  pointer-events: none;
}

.flip-card-container:hover .card-hint {
  opacity: 1;
  transform: translateX(-50%) translateY(-5px);
}

.hint-icon {
  animation: spinSlow 4s linear infinite;
}

@keyframes spinSlow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Backside Text content fallback */
.card-text-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #faf7f0;
}

.scroll-area {
  height: 100%;
  overflow-y: auto;
  padding: 2.5rem 2rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(200, 160, 50, 0.4) transparent;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Scroll area styling */
.scroll-area::-webkit-scrollbar {
  width: 5px;
}
.scroll-area::-webkit-scrollbar-track {
  background: transparent;
}
.scroll-area::-webkit-scrollbar-thumb {
  background-color: rgba(200, 160, 50, 0.3);
  border-radius: 20px;
}

/* Card Controls styling */
.card-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
  width: 100%;
}

.btn-flip {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0.9rem 2.2rem;
  background: linear-gradient(135deg, #7a4e00 0%, #c8860a 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 10px 25px rgba(200, 160, 50, 0.25);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.btn-flip:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(200, 160, 50, 0.35);
  background: linear-gradient(135deg, #8b5a00 0%, #d89614 100%);
}

.btn-flip svg {
  transition: transform 0.6s ease;
}

.btn-flip:hover svg {
  transform: rotate(180deg);
}

.download-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-download {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0.6rem 1.2rem;
  background: rgba(200, 160, 50, 0.08);
  color: #7a4e00;
  border: 1px solid rgba(200, 160, 50, 0.25);
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.btn-download:hover {
  background: rgba(200, 160, 50, 0.15);
  border-color: rgba(200, 160, 50, 0.4);
  transform: translateY(-1px);
}

/* Opening verse */
.opening-verse {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1.2rem 2rem;
  background: linear-gradient(135deg, rgba(245,200,66,0.12), rgba(200,160,50,0.08));
  border-left: 3px solid #c8860a;
  border-radius: 0 12px 12px 0;
}
.opening-verse em {
  display: block;
  font-style: italic;
  font-size: 0.98rem;
  color: #5a3e0a;
  line-height: 1.7;
  font-family: Georgia, serif;
}
.verse-ref {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #b07d12;
  text-transform: uppercase;
}

/* Prayer body */
.prayer-body {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1.05rem;
  line-height: 2;
  color: #2d1f00;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stanza {
  padding: 0;
  margin: 0;
}

.stanza-amen {
  text-align: center;
  font-size: 1.3rem;
  font-weight: 700;
  font-family: 'Outfit', Georgia, serif;
  color: #7a4e00;
  letter-spacing: 0.12em;
  margin-top: 0.5rem;
}

/* Footer */
.prayer-footer {
  text-align: center;
  margin-top: 2.5rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(180, 130, 30, 0.25);
}
.footer-cross {
  font-size: 1.8rem;
  color: #b07d12;
  margin-bottom: 0.8rem;
  animation: crossPulse 3s ease-in-out infinite;
}
@keyframes crossPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.7; transform: scale(0.95); }
}

.attribution {
  font-weight: 700;
  font-size: 0.95rem;
  color: #5a3e0a;
  letter-spacing: 0.04em;
  font-family: 'Outfit', sans-serif;
}
.chapter-year {
  font-size: 0.8rem;
  color: #b07d12;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-top: 4px;
}

/* ─── LOADING / ERROR ─────────────────────────────────────────── */
.state-block {
  text-align: center;
  padding: 5rem 2rem;
  color: #7a5c1e;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}
.state-error .error-icon { font-size: 3rem; }

.spinner {
  width: 48px; height: 48px;
  border: 4px solid rgba(200,160,50,0.2);
  border-top-color: #c8860a;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── ROSARY ROW ──────────────────────────────────────────────── */
.rosary-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 2rem 1rem 3rem;
  position: relative;
  z-index: 2;
}
.bead {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #c8860a, #f5c842);
  opacity: 0.5;
  flex-shrink: 0;
}
.bead-lg {
  width: 14px; height: 14px;
  opacity: 0.75;
  box-shadow: 0 2px 6px rgba(180,130,30,0.4);
}

/* ─── RESPONSIVE ─────────────────────────────────────────────── */
@media (max-width: 640px) {
  .prayer-card { padding: 2rem 1.5rem; }
  .prayer-body { font-size: 0.97rem; }
  .scroll-area { padding: 1.5rem 1rem; }
  .flip-card-container { max-width: 320px; }
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.96) translateY(20px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
