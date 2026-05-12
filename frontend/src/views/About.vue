<script setup>
import { RouterLink } from 'vue-router'
import { ArrowRight, Globe, Users, BookOpen, ShieldCheck } from 'lucide-vue-next'

const values = [
  { icon: Globe,       color: '#0078d4', title: 'Accessibility', desc: 'Documents are accessible from any device, anywhere in the world.' },
  { icon: Users,       color: '#5c2d91', title: 'Community',     desc: 'Built for and by the St. Joseph Province community.' },
  { icon: BookOpen,    color: '#107c10', title: 'Knowledge',     desc: 'Preserving decades of provincial wisdom and history.' },
  { icon: ShieldCheck, color: '#d13438', title: 'Integrity',     desc: 'Only verified, official documents are published here.' },
]
</script>

<template>
  <div class="about-page">
    <header class="about-hero">
      <div class="container">
        <span class="section-eyebrow">Our Mission</span>
        <h1 class="section-title">About SJP Chapter Hub</h1>
        <p class="section-subtitle">
          A digital archive dedicated to preserving and sharing the official documents of
          St. Joseph Province, making provincial knowledge accessible to all members.
        </p>
      </div>
      <div class="hero-shapes">
        <div class="shape s1"></div>
        <div class="shape s2"></div>
        <div class="shape s3"></div>
      </div>
    </header>

    <section class="about-content">
      <div class="container about-grid">
        <!-- Mission text -->
        <div class="about-text glass">
          <h2>What is the Chapter Hub?</h2>
          <p>
            The SJP Chapter Hub is the official digital repository for St. Joseph Province.
            It provides a centralized, accessible, and organized platform for all chapter-related
            documents — including legislative records, meeting minutes, provincial directories,
            and other official materials.
          </p>
          <p>
            This hub ensures that every member of the province has access to the information
            they need, when they need it — whether attending a chapter meeting, studying
            provincial history, or preparing for a new mission.
          </p>
          <RouterLink to="/repository" class="btn-primary">
            Browse Repository <ArrowRight :size="18" />
          </RouterLink>
        </div>

        <!-- Values cards -->
        <div class="values-grid">
          <div v-for="v in values" :key="v.title" class="value-card glass">
            <div class="val-icon-wrap" :style="{ background: v.color + '15', color: v.color, boxShadow: '0 4px 12px ' + v.color + '30' }">
              <component :is="v.icon" :size="28" />
            </div>
            <h3>{{ v.title }}</h3>
            <p>{{ v.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Hero */
.about-hero {
  position: relative;
  overflow: hidden;
  padding: 8rem 2rem 7rem;
  background: var(--bg-dark);
}

.about-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #022c22 0%, #0050a8 100%);
  z-index: 0;
}

.about-hero .container { position: relative; z-index: 2; }
.about-hero .section-eyebrow  { color: #34d399; letter-spacing: 0.2em; font-weight: 700; }
.about-hero .section-title     { color: white; font-size: clamp(2.5rem,5vw,4rem); margin-bottom: 1.2rem; text-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.about-hero .section-subtitle  { color: rgba(255,255,255,0.85); max-width: 650px; font-size: 1.15rem; line-height: 1.7; }

.hero-shapes { position: absolute; inset: 0; z-index: 1; pointer-events: none; overflow: hidden; }
.shape { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.55; animation: float 12s ease-in-out infinite alternate; }
.s1 { background: #10b981; width: 500px; height: 500px; top: -150px; left: -100px; animation-delay: 0s; }
.s2 { background: var(--primary-color); width: 450px; height: 450px; bottom: -150px; right: 10%; animation-delay: -4s; }
.s3 { background: #0ea5e9; width: 300px; height: 300px; top: 10%; right: 40%; animation-delay: -7s; opacity: 0.4; }

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(40px, -40px) scale(1.1); }
}

/* Content */
.about-content { padding: 6rem 2rem; position: relative; z-index: 5; }

.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

.about-text {
  padding: 3.5rem;
  border-radius: var(--border-radius-lg);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(255,255,255,0.7));
  border: 1px solid rgba(255,255,255,0.8);
  box-shadow: 0 20px 40px rgba(0,0,0,0.06);
}

.about-text h2 { font-size: 2.2rem; color: var(--primary-dark); margin-bottom: 0.5rem; }
.about-text p  { color: var(--text-secondary); line-height: 1.85; font-size: 1.05rem; }

/* Values */
.values-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.value-card {
  padding: 2.2rem 1.8rem;
  border-radius: var(--border-radius-lg);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  transition: var(--transition-smooth);
  border: 1px solid rgba(255,255,255,0.5);
  background: rgba(255,255,255,0.6);
}

.value-card:hover {
  transform: translateY(-8px);
  background: rgba(255,255,255,0.95);
  box-shadow: var(--card-shadow-hover);
  border-color: rgba(0,106,220,0.2);
}

.val-icon-wrap {
  width: 54px; height: 54px;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  transition: var(--transition-smooth);
}

.value-card:hover .val-icon-wrap {
  transform: scale(1.1) rotate(5deg);
}

.value-card h3 { font-size: 1.15rem; color: var(--text-main); }
.value-card p  { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.7; }

@media (max-width: 900px) {
  .about-grid { grid-template-columns: 1fr; }
}

@media (max-width: 560px) {
  .values-grid { grid-template-columns: 1fr; }
  .about-text { padding: 2rem 1.5rem; }
}
</style>
