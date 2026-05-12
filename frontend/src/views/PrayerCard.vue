<script setup>
import { ref, onMounted, computed } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api'

const prayer = ref(null)
const loading = ref(true)
const error = ref(null)

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

    <!-- ─── PRAYER BODY CARD ─────────────────────────────────── -->
    <section class="prayer-card-wrap">
      <article class="prayer-card" v-if="!loading && !error && prayer">

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

/* ─── PRAYER CARD ─────────────────────────────────────────────── */
.prayer-card-wrap {
  position: relative;
  z-index: 2;
  max-width: 780px;
  margin: 3rem auto 2rem;
  padding: 0 1.5rem;
}

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

/* Corner ornament */
.prayer-card::before {
  content: '✝';
  position: absolute;
  top: 1.5rem;
  right: 2rem;
  font-size: 1.2rem;
  color: rgba(180, 130, 30, 0.25);
  font-family: serif;
}
.prayer-card::after {
  content: '✝';
  position: absolute;
  bottom: 1.5rem;
  left: 2rem;
  font-size: 1.2rem;
  color: rgba(180, 130, 30, 0.25);
  font-family: serif;
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
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.96) translateY(20px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
