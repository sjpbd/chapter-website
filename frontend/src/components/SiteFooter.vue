<script setup>
import { RouterLink } from 'vue-router'
import { MapPin, Phone, Globe, Heart } from 'lucide-vue-next'
import { useConfigStore } from '../store/configStore'

const configStore = useConfigStore()
</script>

<template>
  <footer class="site-footer">
    <div class="footer-wave"></div>
    <div class="footer-body">
      <div class="container footer-grid">
        <!-- Brand -->
        <div class="f-col brand-col">
          <div class="f-logo">
            <div class="f-logo-icon" :class="{ 'has-logo': configStore.logo }">
              <img v-if="configStore.logo" :src="configStore.logo" :alt="configStore.siteName" class="dynamic-logo" />
            </div>
            <span>{{ configStore.siteName }}</span>
          </div>
          <p class="f-desc">
            {{ configStore.footerText || 'The official digital repository for St. Joseph Province chapter documents, provincial records, and legislative materials.' }}
          </p>
        </div>

        <!-- Navigation -->
        <div class="f-col">
          <h4 class="f-heading">Navigation</h4>
          <ul class="f-links">
            <li><RouterLink to="/">Home</RouterLink></li>
            <li><RouterLink to="/repository">Repository</RouterLink></li>
            <li><RouterLink to="/about">About</RouterLink></li>
          </ul>
        </div>

        <!-- Contact -->
        <div class="f-col">
          <h4 class="f-heading">Contact</h4>
          <ul class="f-info">
            <li><MapPin :size="15" /> St. Joseph Province</li>
            <li><Globe :size="15" /> Dhaka, Bangladesh</li>
          </ul>
        </div>
      </div>

      <div class="container footer-bottom">
        <p>© {{ new Date().getFullYear() }} St. Joseph Province. All rights reserved.</p>

      </div>
    </div>
  </footer>
</template>

<style scoped>
.site-footer { background: #0d1b2a; color: rgba(255,255,255,0.7); }

.footer-wave {
  width: 100%;
  height: 60px;
  background: linear-gradient(to bottom right, var(--bg-color) 50%, transparent 50%);
}

.footer-body { padding: 3rem 0 2rem; }

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 3rem;
  margin-bottom: 3rem;
}

.f-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 1.2rem;
  font-weight: 800;
  font-size: 1.25rem;
  color: white;
}

.f-logo-icon {
  width: 48px; height: 48px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: all 0.3s ease;
}

.f-logo-icon.has-logo {
  background: none;
  border-radius: 0;
}

.dynamic-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.f-desc { font-size: 0.9rem; line-height: 1.7; max-width: 320px; }

.f-heading {
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 1.2rem;
}

.f-links { list-style: none; display: flex; flex-direction: column; gap: 0.7rem; }
.f-links a { font-size: 0.9rem; transition: var(--transition-smooth); }
.f-links a:hover { color: white; padding-left: 4px; }

.f-info { list-style: none; display: flex; flex-direction: column; gap: 0.8rem; }
.f-info li { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; }

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255,255,255,0.08);
  font-size: 0.82rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.made-with { display: flex; align-items: center; gap: 6px; }

@media (max-width: 768px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .brand-col { grid-column: 1 / -1; }
  .footer-bottom { flex-direction: column; text-align: center; }
}

@media (max-width: 480px) {
  .footer-grid { grid-template-columns: 1fr; }
}
</style>
