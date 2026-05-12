<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
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
const wrapperRef   = ref(null)
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
  if (e.key === 'ArrowDown') { e.preventDefault(); activeIndex.value = Math.min(activeIndex.value + 1, results.value.length - 1) }
  else if (e.key === 'ArrowUp') { e.preventDefault(); activeIndex.value = Math.max(activeIndex.value - 1, -1) }
  else if (e.key === 'Escape') close()
  else if (e.key === 'Enter') {
    if (activeIndex.value >= 0) navigate(results.value[activeIndex.value])
    else submitSearch()
  }
}

// ── open / close ──────────────────────────────────────────────────────────────
const open  = () => { isOpen.value = true }
const close = () => { isOpen.value = false; activeIndex.value = -1 }

const onClickOutside = (e) => {
  if (wrapperRef.value && !wrapperRef.value.contains(e.target)) close()
}

// ── global Ctrl/Cmd+K shortcut ─────────────────────────────────────────────
const onGlobalKey = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    inputRef.value?.focus()
    open()
  }
}

onMounted(() => {
  document.addEventListener('mousedown', onClickOutside)
  document.addEventListener('keydown', onGlobalKey)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onClickOutside)
  document.removeEventListener('keydown', onGlobalKey)
  clearTimeout(debounce)
})
</script>

<template>
  <div class="gs-wrap" ref="wrapperRef">
    <!-- ── Input ── -->
    <div :class="['gs-box', { active: isOpen }]">
      <Search :size="16" class="gs-left-icon" />

      <input
        ref="inputRef"
        v-model="query"
        type="text"
        placeholder="Search documents…"
        autocomplete="off"
        spellcheck="false"
        @focus="open"
        @keydown="onKeydown"
        aria-label="Search chapter materials"
        aria-autocomplete="list"
      />

      <button v-if="query" class="gs-clear" @click.stop="query = ''; results = []; inputRef?.focus()" tabindex="-1" aria-label="Clear search">
        <X :size="15" />
      </button>

      <Loader2 v-if="loading" :size="15" class="gs-spin" />

      <kbd v-if="!isOpen && !query" class="gs-kbd">⌘K</kbd>
    </div>

    <!-- ── Dropdown ── -->
    <Transition name="dropdown">
      <div v-if="isOpen" class="gs-dropdown" role="listbox">

        <!-- Searching state (empty results so far) -->
        <div v-if="query.trim() && loading && results.length === 0" class="gs-state">
          <Loader2 :size="22" class="animate-spin" style="color:var(--primary-color)" />
          <span>Searching…</span>
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
            <Search :size="14" />
            See all results for <strong>"{{ query }}"</strong>
          </div>
        </template>

        <!-- No results -->
        <div v-else-if="query.trim() && !loading && results.length === 0" class="gs-state">
          <Search :size="30" style="opacity:0.3" />
          <p>No documents match <strong>"{{ query }}"</strong></p>
        </div>

        <!-- Idle: recent searches -->
        <template v-else-if="!query.trim() && recentSearches.length">
          <div class="gs-section-label between">
            <span style="display:flex;align-items:center;gap:6px"><Clock :size="13" /> Recent</span>
            <button class="gs-clear-recent" @click.stop="clearRecent">Clear all</button>
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
        <div v-else class="gs-state">
          <TrendingUp :size="30" style="color:var(--primary-color);opacity:0.5" />
          <p style="color:var(--text-secondary)">Type to search all chapter materials…</p>
        </div>

      </div>
    </Transition>
  </div>
</template>

<style scoped>
/* ── wrapper ── */
.gs-wrap {
  position: relative;
  flex: 1;
  max-width: 420px;
}

/* ── input box ── */
.gs-box {
  display: flex;
  align-items: center;
  height: 42px;
  padding: 0 14px;
  gap: 0;
  border: 1.5px solid #e0e0e0;
  border-radius: 50px;
  background: rgba(255,255,255,0.85);
  transition: all 0.25s ease;
  cursor: text;
}

.gs-box.active {
  border-color: var(--primary-color);
  background: white;
  border-radius: 14px 14px 0 0;
  box-shadow: 0 0 0 4px rgba(0,120,212,0.1);
  border-bottom-color: transparent;
}

.gs-left-icon {
  color: var(--text-secondary);
  flex-shrink: 0;
  margin-right: 10px;
}

.gs-box input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: inherit;
  font-size: 0.9rem;
  color: var(--text-main);
  outline: none;
  min-width: 0;
}

.gs-box input::placeholder { color: var(--text-light); }

.gs-clear {
  background: none;
  color: var(--text-secondary);
  width: 22px; height: 22px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  transition: var(--transition-smooth);
}
.gs-clear:hover { background: #f0f0f0; color: var(--text-main); }

.gs-kbd {
  font-size: 0.68rem;
  background: #f3f3f3;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 2px 7px;
  color: var(--text-secondary);
  margin-left: 8px;
  white-space: nowrap;
  font-family: inherit;
}

.gs-spin {
  color: var(--primary-color);
  flex-shrink: 0;
  margin-left: 8px;
  animation: spin 0.8s linear infinite;
}

/* ── dropdown ── */
.gs-dropdown {
  position: absolute;
  top: calc(100% - 1px);
  left: 0; right: 0;
  background: white;
  border: 1.5px solid var(--primary-color);
  border-top: none;
  border-radius: 0 0 16px 16px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.14);
  z-index: 3000;
  overflow: hidden;
  max-height: 500px;
  overflow-y: auto;
}

/* scrollbar */
.gs-dropdown::-webkit-scrollbar { width: 4px; }
.gs-dropdown::-webkit-scrollbar-thumb { background: rgba(0,120,212,0.25); border-radius: 4px; }

/* section label */
.gs-section-label {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px 6px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-secondary);
}
.gs-section-label.between { justify-content: space-between; }
.gs-clear-recent { font-size: 0.72rem; font-weight: 700; color: var(--primary-color); background: none; cursor: pointer; }

/* result row */
.gs-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.12s;
}
.gs-row:hover, .gs-row.active { background: rgba(0,120,212,0.06); }

.gs-file-icon {
  width: 34px; height: 34px;
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.gs-row-body { flex: 1; min-width: 0; }

.gs-row-title {
  font-size: 0.88rem;
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
  font-size: 0.73rem;
  color: var(--text-secondary);
  margin-top: 1px;
}

.gs-row-arrow {
  color: var(--text-light);
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.12s, transform 0.12s;
}
.gs-row:hover .gs-row-arrow,
.gs-row.active .gs-row-arrow { opacity: 1; transform: translateX(3px); }

/* recent */
.gs-recent { color: var(--text-secondary); font-size: 0.9rem; }

/* see all */
.gs-see-all {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--primary-color);
  cursor: pointer;
  border-top: 1px solid #f4f4f4;
  transition: background 0.12s;
}
.gs-see-all:hover { background: rgba(0,120,212,0.05); }

/* state (loading, empty, hint) */
.gs-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 3rem 1.5rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* ── animation ── */
.dropdown-enter-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.dropdown-leave-active { transition: opacity 0.15s ease; }
.dropdown-enter-from   { opacity: 0; transform: translateY(-6px); }
.dropdown-leave-to     { opacity: 0; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>
