<script setup>
import { onMounted } from 'vue'
import { useDocumentStore } from '../store/documentStore'
import HeroSlider from '../components/HeroSlider.vue'
import * as LucideIcons from 'lucide-vue-next'

const store = useDocumentStore()

onMounted(() => {
  store.fetchSliders()
  store.fetchCategories()
  store.fetchDocuments()
  store.fetchFeatures()
})

const getIcon = (name) => {
  return LucideIcons[name] || LucideIcons.HelpCircle
}
</script>

<template>
  <div class="home">
    <!-- HERO SLIDER -->
    <HeroSlider :slides="store.sliders" />

    <!-- FEATURES -->
    <section class="features-section">
      <div class="container">
        <div class="section-header">
          <span class="section-eyebrow">Why Chapter Hub?</span>
          <h2 class="section-title">Everything you need, in one place</h2>
          <p class="section-subtitle">A premium platform built for the Brothers and members of St. Joseph Province to access all official chapter materials with ease.</p>
        </div>
        <div class="features-grid">
          <div v-for="f in store.features" :key="f.title" class="feature-card glass">
            <div class="feat-icon" :style="{ background: f.color + '15', color: f.color }">
              <component :is="getIcon(f.icon)" :size="28" />
            </div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- RECENT DOCUMENTS PREVIEW -->
    <section class="recent-section" v-if="store.documents.length">
      <div class="container">
        <div class="section-header row">
          <div>
            <span class="section-eyebrow">Latest Additions</span>
            <h2 class="section-title">Recently Added</h2>
          </div>
          <RouterLink to="/repository" class="btn-outline">
            View All <component :is="LucideIcons.ArrowRight" :size="18" />
          </RouterLink>
        </div>
        <div class="recent-grid">
          <div v-for="doc in store.documents.slice(0, 3)" :key="doc.id" class="recent-card glass">
            <div class="rec-icon">
              <component :is="LucideIcons.FileText" :size="24" color="white" />
            </div>
            <div class="rec-info">
              <span class="rec-category">{{ doc.category_name }}</span>
              <h4 class="rec-title">{{ doc.title }}</h4>
            </div>
            <a :href="doc.file" download class="rec-download">
              <component :is="LucideIcons.Download" :size="18" />
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA BANNER -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-card">
          <div class="cta-bg"></div>
          <div class="cta-content">
            <component :is="LucideIcons.Star" :size="48" color="rgba(255,255,255,0.5)" />
            <h2>Ready to explore the repository?</h2>
            <p>All official chapter documents, records, and materials are just a click away.</p>
            <RouterLink to="/repository" class="btn-primary">
              Go to Repository <component :is="LucideIcons.ArrowRight" :size="20" />
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Features */
.features-section { padding: 7rem 2rem; }

.section-header { margin-bottom: 4rem; }
.section-header.row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2.5rem 2rem;
  border-radius: var(--border-radius-lg);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: var(--transition-smooth);
}

.feature-card:hover {
  transform: translateY(-8px);
  background: white;
  box-shadow: var(--card-shadow-hover);
}

.feat-icon {
  width: 60px; height: 60px;
  border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  transition: var(--transition-smooth);
}

.feature-card:hover .feat-icon { transform: scale(1.1) rotate(-5deg); }

.feature-card h3 { font-size: 1.15rem; }
.feature-card p  { color: var(--text-secondary); font-size: 0.95rem; line-height: 1.7; }

/* Recent */
.recent-section { padding: 4rem 2rem 7rem; background: white; }

.recent-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recent-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.2rem 1.5rem;
  border-radius: var(--border-radius);
  transition: var(--transition-smooth);
}

.recent-card:hover {
  transform: translateX(6px);
  box-shadow: var(--card-shadow-hover);
  background: white;
}

.rec-icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.rec-info { flex: 1; }
.rec-category {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--primary-color);
  display: block;
  margin-bottom: 2px;
}

.rec-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
}

.rec-download {
  width: 40px; height: 40px;
  border-radius: 10px;
  background: rgba(0,120,212,0.07);
  color: var(--primary-color);
  display: flex; align-items: center; justify-content: center;
  transition: var(--transition-smooth);
  flex-shrink: 0;
}

.rec-download:hover {
  background: var(--primary-color);
  color: white;
}

/* CTA */
.cta-section { padding: 5rem 2rem; }

.cta-card {
  position: relative;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  padding: 6rem 3rem;
  text-align: center;
}

.cta-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 50%, #00b4d8 100%);
}

.cta-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  color: white;
}

.cta-content h2 {
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 800;
  color: white;
}

.cta-content p { font-size: 1.15rem; opacity: 0.9; max-width: 520px; }

.cta-content .btn-primary {
  background: white;
  color: var(--primary-dark);
  font-size: 1.05rem;
  padding: 1.1rem 2.5rem;
}

@media (max-width: 900px) {
  .section-header.row { flex-direction: column; align-items: flex-start; gap: 1rem; }
}

@media (max-width: 480px) {
  .cta-card { padding: 4rem 1.5rem; }
}
</style>
