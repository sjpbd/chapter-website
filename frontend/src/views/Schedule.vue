<script setup>
import { ref, onMounted, computed } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api'

const days = ref([])
const loading = ref(true)
const error = ref(null)
const activeDay = ref(null)

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/schedule/`)
    if (!res.ok) throw new Error('Could not load schedule.')
    const data = await res.json()
    // DRF router returns paginated or plain list
    days.value = Array.isArray(data) ? data : (data.results || [])
    if (days.value.length) activeDay.value = days.value[0].id
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const activeEvents = computed(() => {
  const day = days.value.find(d => d.id === activeDay.value)
  return day ? day.events.filter(e => e) : []
})

const activeDayObj = computed(() => days.value.find(d => d.id === activeDay.value) || null)

// Colour palette per category
const categoryMeta = {
  liturgy: { color: '#7c3aed', bg: 'rgba(124,58,237,0.1)', border: 'rgba(124,58,237,0.3)', emoji: '🙏' },
  session: { color: '#0078d4', bg: 'rgba(0,120,212,0.1)', border: 'rgba(0,120,212,0.3)', emoji: '📋' },
  keynote: { color: '#d97706', bg: 'rgba(217,119,6,0.1)', border: 'rgba(217,119,6,0.3)', emoji: '🎤' },
  meal:    { color: '#059669', bg: 'rgba(5,150,105,0.1)', border: 'rgba(5,150,105,0.3)', emoji: '🍽️' },
  break:   { color: '#0891b2', bg: 'rgba(8,145,178,0.1)', border: 'rgba(8,145,178,0.3)', emoji: '☕' },
  social:  { color: '#db2777', bg: 'rgba(219,39,119,0.1)', border: 'rgba(219,39,119,0.3)', emoji: '🤝' },
  travel:  { color: '#64748b', bg: 'rgba(100,116,139,0.1)', border: 'rgba(100,116,139,0.3)', emoji: '🚌' },
  other:   { color: '#475569', bg: 'rgba(71,85,105,0.1)', border: 'rgba(71,85,105,0.3)', emoji: '📌' },
}

function getMeta(cat) {
  return categoryMeta[cat] || categoryMeta.other
}
</script>

<template>
  <main class="schedule-page">
    <!-- Ambient orbs -->
    <div class="orb orb-blue" aria-hidden="true"></div>
    <div class="orb orb-purple" aria-hidden="true"></div>

    <!-- ─── HERO ─────────────────────────────────────────── -->
    <header class="sched-hero">
      <span class="eyebrow">Chapter 2027 · St. Joseph Province</span>
      <h1 class="sched-title">Daily Programme Schedule</h1>
      <p class="sched-subtitle">
        Full timetable of sessions, liturgies, meals, and activities for the Chapter 2027.
      </p>
    </header>

    <!-- ─── LOADING ───────────────────────────────────────── -->
    <div v-if="loading" class="state-center">
      <div class="spinner"></div>
      <p>Loading schedule…</p>
    </div>

    <!-- ─── ERROR ────────────────────────────────────────── -->
    <div v-else-if="error" class="state-center state-error">
      <span class="state-icon">⚠️</span>
      <p>{{ error }}</p>
    </div>

    <!-- ─── EMPTY ────────────────────────────────────────── -->
    <div v-else-if="!days.length" class="state-center">
      <span class="state-icon">📅</span>
      <p>No schedule has been published yet.<br/>Check back soon.</p>
    </div>

    <!-- ─── SCHEDULE ─────────────────────────────────────── -->
    <div v-else class="sched-layout">

      <!-- Day Tabs -->
      <nav class="day-tabs" role="tablist" aria-label="Chapter days">
        <button
          v-for="day in days"
          :key="day.id"
          role="tab"
          :aria-selected="activeDay === day.id"
          :class="['day-tab', { active: activeDay === day.id }]"
          @click="activeDay = day.id"
        >
          <span class="tab-weekday">{{ day.weekday }}</span>
          <span class="tab-date">{{ day.date_fmt }}</span>
          <span class="tab-label">{{ day.day_label }}</span>
          <span class="tab-count">{{ day.events.length }} events</span>
        </button>
      </nav>

      <!-- Day content -->
      <section class="day-panel" role="tabpanel" v-if="activeDayObj">

        <!-- Day header -->
        <div class="day-header">
          <div class="day-header-left">
            <div class="day-badge">
              <span class="day-badge-weekday">{{ activeDayObj.weekday }}</span>
              <span class="day-badge-num">{{ activeDayObj.date.split('-')[2] }}</span>
            </div>
            <div>
              <h2 class="day-title">{{ activeDayObj.day_label }}</h2>
              <p class="day-date-full">{{ activeDayObj.date_fmt }}</p>
              <p class="day-theme" v-if="activeDayObj.theme">{{ activeDayObj.theme }}</p>
            </div>
          </div>
          <div class="day-event-pill">{{ activeDayObj.events.length }} programme items</div>
        </div>

        <!-- Empty day -->
        <div class="day-empty" v-if="!activeEvents.length">
          <span>📋</span>
          <p>No events scheduled for this day yet.</p>
        </div>

        <!-- Timeline -->
        <div class="timeline" v-else>
          <div
            v-for="(event, idx) in activeEvents"
            :key="event.id"
            :class="['event-row', { highlighted: event.is_highlighted }]"
          >
            <!-- Time column -->
            <div class="event-time">
              <span class="time-start">{{ event.time_start_fmt }}</span>
              <span class="time-end" v-if="event.time_end_fmt">→ {{ event.time_end_fmt }}</span>
            </div>

            <!-- Connector dot -->
            <div class="event-dot-wrap">
              <div
                class="event-dot"
                :style="{ background: getMeta(event.category).color }"
              ></div>
              <div class="event-line" v-if="idx < activeEvents.length - 1"></div>
            </div>

            <!-- Card -->
            <div
              class="event-card"
              :style="{
                background: getMeta(event.category).bg,
                borderColor: getMeta(event.category).border,
              }"
            >
              <!-- Highlighted ribbon -->
              <div class="highlight-ribbon" v-if="event.is_highlighted">⭐ Featured</div>

              <div class="event-card-top">
                <span
                  class="category-chip"
                  :style="{ color: getMeta(event.category).color, borderColor: getMeta(event.category).border }"
                >
                  {{ getMeta(event.category).emoji }} {{ event.category_display.replace(/^[^\s]+\s/, '') }}
                </span>
              </div>

              <h3 class="event-title">{{ event.title }}</h3>

              <p class="event-desc" v-if="event.description">{{ event.description }}</p>

              <div class="event-meta-row">
                <span class="event-meta" v-if="event.location">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  {{ event.location }}
                </span>
                <span class="event-meta" v-if="event.speaker">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  {{ event.speaker }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
/* ─── PAGE ───────────────────────────────────────────────── */
.schedule-page {
  min-height: 100vh;
  padding-top: 72px;
  background:
    radial-gradient(ellipse 70% 50% at 20% 0%, rgba(0,120,212,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 80% 80%, rgba(99,46,155,0.1) 0%, transparent 60%),
    #f8fafc;
  position: relative;
  overflow: hidden;
}

/* Ambient orbs */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.4;
  pointer-events: none;
}
.orb-blue   { width: 400px; height: 400px; top: -80px; left: -100px; background: radial-gradient(circle, #60a5fa, #2563eb); }
.orb-purple { width: 300px; height: 300px; bottom: 10%; right: -80px; background: radial-gradient(circle, #a78bfa, #7c3aed); }

/* ─── HERO ───────────────────────────────────────────────── */
.sched-hero {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 3.5rem 2rem 2.5rem;
}

.eyebrow {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--primary-color);
  background: rgba(0,120,212,0.08);
  border: 1px solid rgba(0,120,212,0.2);
  padding: 5px 18px;
  border-radius: 50px;
  margin-bottom: 1rem;
}

.sched-title {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
  margin-bottom: 0.7rem;
}

.sched-subtitle {
  font-size: 1.05rem;
  color: var(--text-secondary);
  max-width: 560px;
  margin: 0 auto;
  line-height: 1.7;
}

/* ─── STATES ─────────────────────────────────────────────── */
.state-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  padding: 6rem 2rem;
  color: var(--text-secondary);
  text-align: center;
}
.state-icon { font-size: 3rem; }
.state-error { color: #dc2626; }

.spinner {
  width: 44px; height: 44px;
  border: 4px solid rgba(0,120,212,0.15);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.85s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── LAYOUT ─────────────────────────────────────────────── */
.sched-layout {
  position: relative;
  z-index: 2;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.5rem 4rem;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
  align-items: start;
}

/* ─── DAY TABS (left sidebar) ───────────────────────────── */
.day-tabs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: sticky;
  top: 90px;
}

.day-tab {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  padding: 1rem 1.2rem;
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(15,23,42,0.07);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
  text-align: left;
  width: 100%;
}

.day-tab:hover {
  background: rgba(0,120,212,0.06);
  border-color: rgba(0,120,212,0.2);
  transform: translateX(3px);
}

.day-tab.active {
  background: linear-gradient(135deg, rgba(0,120,212,0.12), rgba(0,80,168,0.08));
  border-color: rgba(0,120,212,0.4);
  box-shadow: 0 4px 16px rgba(0,120,212,0.12);
  transform: translateX(4px);
}

.tab-weekday {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--primary-color);
}

.tab-date {
  font-size: 0.78rem;
  color: var(--text-secondary);
}

.tab-label {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.3;
}

.tab-count {
  font-size: 0.7rem;
  color: var(--text-light);
  margin-top: 2px;
}

/* ─── DAY PANEL (right content) ─────────────────────────── */
.day-panel {
  min-width: 0;
}

.day-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem 2rem;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(15,23,42,0.07);
  border-radius: 20px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.05);
}

.day-header-left {
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.day-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 58px;
  height: 58px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 14px;
  flex-shrink: 0;
  box-shadow: 0 6px 18px rgba(0,120,212,0.3);
}

.day-badge-weekday {
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.8);
}

.day-badge-num {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  line-height: 1;
}

.day-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 2px;
}

.day-date-full {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.day-theme {
  font-size: 0.82rem;
  color: var(--primary-color);
  font-style: italic;
  margin-top: 3px;
}

.day-event-pill {
  background: rgba(0,120,212,0.08);
  color: var(--primary-color);
  border: 1px solid rgba(0,120,212,0.2);
  border-radius: 50px;
  padding: 5px 14px;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
}

.day-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  padding: 4rem 2rem;
  color: var(--text-light);
  font-size: 1.05rem;
  text-align: center;
}
.day-empty span { font-size: 2.5rem; }

/* ─── TIMELINE ───────────────────────────────────────────── */
.timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.event-row {
  display: grid;
  grid-template-columns: 100px 28px 1fr;
  gap: 0 0.8rem;
  align-items: start;
  animation: fadeInUp 0.4s ease both;
}

.event-row:nth-child(1)  { animation-delay: 0.05s; }
.event-row:nth-child(2)  { animation-delay: 0.1s; }
.event-row:nth-child(3)  { animation-delay: 0.15s; }
.event-row:nth-child(4)  { animation-delay: 0.2s; }
.event-row:nth-child(5)  { animation-delay: 0.25s; }
.event-row:nth-child(6)  { animation-delay: 0.3s; }
.event-row:nth-child(7)  { animation-delay: 0.35s; }
.event-row:nth-child(8)  { animation-delay: 0.4s; }
.event-row:nth-child(9)  { animation-delay: 0.45s; }
.event-row:nth-child(10) { animation-delay: 0.5s; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Time column */
.event-time {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding-top: 1rem;
  gap: 2px;
}

.time-start {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-main);
  font-family: 'Outfit', sans-serif;
  white-space: nowrap;
}

.time-end {
  font-size: 0.72rem;
  color: var(--text-light);
  white-space: nowrap;
}

/* Connector */
.event-dot-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 1.1rem;
}

.event-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.9), 0 0 0 5px rgba(0,0,0,0.06);
  z-index: 1;
}

.event-line {
  width: 2px;
  flex: 1;
  min-height: 24px;
  background: linear-gradient(to bottom, rgba(15,23,42,0.12), rgba(15,23,42,0.04));
  margin-top: 4px;
}

/* Event card */
.event-card {
  margin-bottom: 1.2rem;
  padding: 1.1rem 1.4rem;
  border: 1px solid;
  border-radius: 16px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.event-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.highlighted .event-card {
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.highlight-ribbon {
  position: absolute;
  top: 0;
  right: 0;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 3px 10px;
  border-radius: 0 16px 0 10px;
}

.event-card-top {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.5rem;
}

.category-chip {
  font-size: 0.7rem;
  font-weight: 700;
  border: 1px solid;
  border-radius: 50px;
  padding: 2px 10px;
  letter-spacing: 0.03em;
}

.event-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.35rem;
  line-height: 1.3;
}

.event-desc {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 0.6rem;
}

.event-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  margin-top: 0.5rem;
}

.event-meta {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.78rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* ─── RESPONSIVE ─────────────────────────────────────────── */
@media (max-width: 768px) {
  .sched-layout {
    grid-template-columns: 1fr;
  }
  .day-tabs {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    position: static;
  }
  .day-tab { transform: none !important; }
  .event-row { grid-template-columns: 84px 20px 1fr; }
  .time-start { font-size: 0.8rem; }
}

@media (max-width: 480px) {
  .day-header { flex-direction: column; }
  .event-time { align-items: flex-start; }
}
</style>
