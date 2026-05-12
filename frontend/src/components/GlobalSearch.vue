<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Search, FileText, X, Clock, ArrowRight, Loader2, TrendingUp } from 'lucide-vue-next'

// ── helpers ──────────────────────────────────────────────────────────────────
const EXT_COLORS = { PDF: '#d13438', DOCX: '#0078d4', DOC: '#0078d4', XLSX: '#107c10' }
const extColor = (filename) => {
  const e = filename?.split('.').pop().toUpperCase()
  return EXT_COLORS[e] ?? '#5c2d91'
}

const highlight = (text, q) => {
  if (!q || !text) return text
  const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return text.replace(new RegExp(`(${esc})`, 'gi'), '<mark>$1</mark>')
}

// ── state ─────────────────────────────────────────────────────────────────────
const router       = useRouter()
const query        = ref('')
const results      = ref([])
const loading      = ref(false)
const isOpen       = ref(false)
const activeIndex  = ref(-1)
const inputRef     = ref(null)
let   debounce     = null

// ── recent searches ───────────────────────────────────────────────────────────
const RECENT_KEY     = 'sjp_recent'
const recentSearches = ref(JSON.parse(localStorage.getItem(RECENT_KEY) ?? '[]'))

const saveRecent = (term) => {
  if (!term) return
  recentSearches.value = [term, ...recentSearches.value.filter(s => s !== term)].slice(0, 6)
  localStorage.setItem(RECENT_KEY, JSON.stringify(recentSearches.value))
}

const clearRecent = () => {
  recentSearches.value = []
  localStorage.removeItem(RECENT_KEY)
}

// ── search ────────────────────────────────────────────────────────────────────
const doSearch = async (q) => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/documents/', { params: { search: q } })
    results.value = Array.isArray(data) ? data.slice(0, 8) : (data.results ?? []).slice(0, 8)
  } catch { results.value = [] }
  finally { loading.value = false }
}

watch(query, (val) => {
  activeIndex.value = -1
  clearTimeout(debounce)
  if (!val.trim()) { results.value = []; loading.value = false; return }
  loading.value = true
  debounce = setTimeout(() => doSearch(val), 280)
})

// ── navigation ────────────────────────────────────────────────────────────────
const navigate = (doc) => {
  saveRecent(query.value.trim() || doc.title)
  close()
  router.push({ path: '/repository', query: { search: doc.title } })
}

const submitSearch = () => {
  const q = query.value.trim()
  if (!q) return
  saveRecent(q)
  close()
  router.push({ path: '/repository', query: { search: q } })
}

const useRecent = (term) => {
  query.value = term
  setTimeout(submitSearch, 0)
}

// ── keyboard ──────────────────────────────────────────────────────────────────
const onKeydown = (e) => {
  if (!isOpen.value) return
  if (e.key === 'ArrowDown') { 
    e.preventDefault(); 
    activeIndex.value = Math.min(activeIndex.value + 1, results.value.length - 1) 
    scrollToActive()
  }
  else if (e.key === 'ArrowUp') { 
    e.preventDefault(); 
    activeIndex.value = Math.max(activeIndex.value - 1, -1) 
    scrollToActive()
  }
  else if (e.key === 'Escape') close()
  else if (e.key === 'Enter') {
    if (activeIndex.value >= 0) navigate(results.value[activeIndex.value])
    else submitSearch()
  }
}

const scrollToActive = () => {
  nextTick(() => {
    const activeEl = document.querySelector('.gs-row.active')
    if (activeEl) activeEl.scrollIntoView({ block: 'nearest' })
  })
}

// ── open / close ──────────────────────────────────────────────────────────────
const open = () => { 
  isOpen.value = true 
  document.body.style.overflow = 'hidden' // prevent background scrolling
  nextTick(() => inputRef.value?.focus())
}

const close = () => { 
  isOpen.value = false
  activeIndex.value = -1 
  document.body.style.overflow = ''
}

// ── global Ctrl/Cmd+K shortcut ─────────────────────────────────────────────
const onGlobalKey = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    isOpen.value ? close() : open()
  }
}

onMounted(() => {
  document.addEventListener('keydown', onGlobalKey)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onGlobalKey)
  clearTimeout(debounce)
  document.body.style.overflow = ''
})
</script>

<template>
  <div class="gs-wrap">
    <!-- ── Trigger Button ── -->
    <button class="gs-trigger" @click="open">
      <div class="trigger-left">
        <Search :size="16" class="gs-left-icon" />
        <span class="gs-trigger-text">Search documents…</span>
      </div>
      <kbd class="gs-kbd">⌘K</kbd>
    </button>

    <!-- ── Command Palette Modal ── -->
    <Teleport to="body">
      <Transition name="palette-fade">
        <div v-if="isOpen" class="palette-overlay" @mousedown.self="close">
          <div class="palette-container">
            
            <!-- Header / Input -->
            <header class="palette-header">
              <Search :size="22" class="ph-icon" />
              <input
                ref="inputRef"
                v-model="query"
                type="text"
                placeholder="Search all chapter materials…"
                autocomplete="off"
                spellcheck="false"
                @keydown="onKeydown"
              />
              <Loader2 v-if="loading" :size="18" class="gs-spin" />
              <button v-else-if="query" class="ph-clear" @click="query = ''; inputRef?.focus()">
                <X :size="18" />
              </button>
              <kbd class="ph-esc" @click="close">ESC</kbd>
            </header>

            <!-- Body / Results -->
            <div class="palette-body" role="listbox">
              <!-- Searching state -->
              <div v-if="query.trim() && loading && results.length === 0" class="gs-state">
                <Loader2 :size="26" class="animate-spin" style="color:var(--primary-color)" />
                <span>Searching archives…</span>
              </div>

              <!-- Results -->
              <template v-else-if="query.trim() && results.length">
                <p class="gs-section-label"><FileText :size="13" /> Matching Documents</p>
                <div
                  v-for="(doc, i) in results"
                  :key="doc.id"
                  :class="['gs-row', { active: activeIndex === i }]"
                  role="option"
                  @mouseenter="activeIndex = i"
                  @click="navigate(doc)"
                >
                  <div class="gs-file-icon" :style="{ background: extColor(doc.file) }">
                    <FileText :size="15" color="white" />
                  </div>
                  <div class="gs-row-body">
                    <p class="gs-row-title" v-html="highlight(doc.title, query)" />
                    <p class="gs-row-cat">{{ doc.category_name }}</p>
                  </div>
                  <ArrowRight :size="15" class="gs-row-arrow" />
                </div>
                
                <div class="gs-see-all" @click="submitSearch">
                  <Search :size="15" />
                  <span>See all results for <strong>"{{ query }}"</strong></span>
                </div>
              </template>

              <!-- No results -->
              <div v-else-if="query.trim() && !loading && results.length === 0" class="gs-state">
                <Search :size="40" style="opacity:0.2; margin-bottom: 10px;" />
                <p>No documents found for <strong>"{{ query }}"</strong></p>
                <span style="font-size: 0.8rem; opacity: 0.7">Try searching by a different keyword or category.</span>
              </div>

              <!-- Idle: recent searches -->
              <template v-else-if="!query.trim() && recentSearches.length">
                <div class="gs-section-label between">
                  <span style="display:flex;align-items:center;gap:6px"><Clock :size="13" /> Recent Searches</span>
                  <button class="gs-clear-recent" @click.stop="clearRecent">Clear History</button>
                </div>
                <div
                  v-for="term in recentSearches"
                  :key="term"
                  class="gs-row gs-recent"
                  @click="useRecent(term)"
                >
                  <Clock :size="15" style="color:var(--text-light);flex-shrink:0" />
                  <span>{{ term }}</span>
                </div>
              </template>

              <!-- Idle: empty state -->
              <div v-else class="gs-state idle">
                <TrendingUp :size="36" style="color:var(--primary-color);opacity:0.4; margin-bottom: 10px;" />
                <p>Search the St. Joseph Province Repository</p>
                <span style="font-size: 0.85rem; opacity: 0.6">Find constitutions, circulars, meeting minutes, and more.</span>
              </div>
            </div>
            
            <footer class="palette-footer">
              <div class="pf-hint"><span>↑↓</span> to navigate</div>
              <div class="pf-hint"><span>Enter</span> to select</div>
              <div class="pf-hint"><span>ESC</span> to close</div>
            </footer>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
/* ── Trigger Button ── */
.gs-wrap {
  width: 100%;
  max-width: 320px;
}

.gs-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 40px;
  padding: 0 12px;
  background: rgba(255,255,255,0.85);
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.gs-trigger:hover {
  background: white;
  border-color: rgba(0,120,212,0.3);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.trigger-left {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
}

.gs-trigger-text {
  font-size: 0.9rem;
}

.gs-kbd {
  font-size: 0.65rem;
  background: rgba(0,0,0,0.05);
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: 4px;
  padding: 2px 6px;
  color: var(--text-secondary);
  font-family: inherit;
  font-weight: 600;
}

/* ── Command Palette Modal ── */
.palette-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 9999;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 12vh;
}

.palette-container {
  width: 100%;
  max-width: 640px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(0,0,0,0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: palette-slide-down 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  margin: 0 1rem;
}

/* ── Header / Input ── */
.palette-header {
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  height: 68px;
  border-bottom: 1px solid var(--border-subtle);
  gap: 1rem;
}

.ph-icon {
  color: var(--primary-color);
  flex-shrink: 0;
}

.palette-header input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 1.25rem;
  color: var(--text-main);
  outline: none;
  min-width: 0;
}

.palette-header input::placeholder {
  color: var(--text-light);
}

.ph-clear {
  background: rgba(0,0,0,0.05);
  color: var(--text-secondary);
  width: 26px; height: 26px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}
.ph-clear:hover { background: #fee2e2; color: #dc2626; }

.ph-esc {
  font-size: 0.65rem;
  background: rgba(0,0,0,0.05);
  border-radius: 4px;
  padding: 4px 8px;
  color: var(--text-secondary);
  font-weight: 700;
  cursor: pointer;
}

/* ── Body ── */
.palette-body {
  max-height: 400px;
  overflow-y: auto;
  padding: 0.5rem 0;
}
.palette-body::-webkit-scrollbar { width: 6px; }
.palette-body::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 6px; }

/* section label */
.gs-section-label {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 1.5rem 6px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-secondary);
}
.gs-section-label.between { justify-content: space-between; }
.gs-clear-recent { font-size: 0.72rem; font-weight: 700; color: var(--primary-color); background: none; cursor: pointer; border: none;}

/* result row */
.gs-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 1.5rem;
  cursor: pointer;
  border-left: 3px solid transparent;
}
.gs-row.active { 
  background: rgba(0,120,212,0.04); 
  border-left-color: var(--primary-color);
}

.gs-file-icon {
  width: 38px; height: 38px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.gs-row-body { flex: 1; min-width: 0; }

.gs-row-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* highlight */
:deep(mark) {
  background: rgba(0,120,212,0.14);
  color: var(--primary-color);
  font-weight: 800;
  border-radius: 3px;
  padding: 0 2px;
}

.gs-row-cat {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 2px;
}

.gs-row-arrow {
  color: var(--primary-color);
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.12s, transform 0.12s;
}
.gs-row.active .gs-row-arrow { opacity: 1; transform: translateX(4px); }

/* recent */
.gs-recent { color: var(--text-secondary); font-size: 0.95rem; padding: 10px 1.5rem;}
.gs-recent.active { background: rgba(0,0,0,0.03); color: var(--text-main); }

/* see all */
.gs-see-all {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 1.5rem;
  font-size: 0.9rem;
  color: var(--primary-color);
  cursor: pointer;
  border-top: 1px solid var(--border-subtle);
  background: rgba(0,120,212,0.02);
}
.gs-see-all:hover { background: rgba(0,120,212,0.06); }

/* state */
.gs-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: var(--text-main);
  font-weight: 500;
}

.gs-spin {
  color: var(--primary-color);
  flex-shrink: 0;
  animation: spin 0.8s linear infinite;
}

/* ── Footer ── */
.palette-footer {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: #f9fafb;
  border-top: 1px solid var(--border-subtle);
}

.pf-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--text-light);
  font-weight: 500;
}

.pf-hint span {
  background: white;
  border: 1px solid #e5e7eb;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  color: var(--text-secondary);
  font-family: inherit;
  font-weight: 600;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* ── animation ── */
.palette-fade-enter-active,
.palette-fade-leave-active {
  transition: opacity 0.2s ease;
}
.palette-fade-enter-from,
.palette-fade-leave-to {
  opacity: 0;
}

@keyframes palette-slide-down {
  from { opacity: 0; transform: scale(0.98) translateY(-20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .palette-overlay { padding-top: 2vh; }
  .palette-container { max-height: 96vh; }
  .palette-body { max-height: calc(96vh - 68px - 40px); }
  .palette-footer { display: none; }
}
</style>
