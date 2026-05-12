<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDocumentStore } from '../store/documentStore'
import { useRoute, useRouter } from 'vue-router'
import DocumentCard from '../components/DocumentCard.vue'
import { Search, SlidersHorizontal, Loader2, FolderOpen, LayoutGrid, List, X } from 'lucide-vue-next'

const store    = useDocumentStore()
const route    = useRoute()
const router   = useRouter()

const searchQuery      = ref(route.query.search ?? '')
const selectedCategory = ref(null)
const viewMode         = ref('grid')
let debounceTimer      = null

onMounted(() => {
  store.fetchCategories()
  loadDocuments()
})

// Re-run search when URL query param changes (e.g., user clicks "See all results")
watch(() => route.query.search, (val) => {
  searchQuery.value = val ?? ''
  loadDocuments()
})

const loadDocuments = () => {
  const params = {}
  if (selectedCategory.value) params.category = selectedCategory.value
  if (searchQuery.value.trim()) params.search = searchQuery.value.trim()
  store.fetchDocuments(params)
}

const onSearch = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    router.replace({ query: searchQuery.value ? { search: searchQuery.value } : {} })
    loadDocuments()
  }, 350)
}

watch(selectedCategory, loadDocuments)

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = null
  router.replace({ query: {} })
  loadDocuments()
}

const hasFilters = computed(() => searchQuery.value || selectedCategory.value !== null)
</script>


<template>
  <div class="repository-page">
    <!-- Page Hero -->
    <header class="repo-hero">
      <div class="container">
        <span class="section-eyebrow">St. Joseph Province</span>
        <h1 class="section-title">Document Repository</h1>
        <p class="section-subtitle">
          Browse, preview, and download official chapter documents, provincial records, and legislative materials.
        </p>
      </div>
      <div class="hero-shapes">
        <div class="shape s1"></div>
        <div class="shape s2"></div>
        <div class="shape s3"></div>
      </div>
    </header>

    <!-- Toolbar -->
    <div class="toolbar glass">
      <div class="container toolbar-inner">
        <!-- Search -->
        <div class="toolbar-search">
          <Search :size="17" class="ts-icon" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search documents by title or description…"
            @input="onSearch"
          />
          <button v-if="searchQuery" class="clear-search" @click="searchQuery = ''; loadDocuments()">
            <X :size="16" />
          </button>
        </div>

        <!-- View Toggle -->
        <div class="view-toggle">
          <button :class="['vt-btn', { active: viewMode === 'grid' }]" @click="viewMode = 'grid'" title="Grid View">
            <LayoutGrid :size="18" />
          </button>
          <button :class="['vt-btn', { active: viewMode === 'list' }]" @click="viewMode = 'list'" title="List View">
            <List :size="18" />
          </button>
        </div>
      </div>
    </div>

    <!-- Main Layout -->
    <div class="container repo-layout">
      <!-- Sidebar -->
      <aside class="sidebar glass">
        <div class="sidebar-header">
          <SlidersHorizontal :size="18" />
          <span>Filter by Category</span>
          <button v-if="hasFilters" class="clear-all" @click="clearFilters">Clear</button>
        </div>

        <ul class="cat-list">
          <li
            :class="['cat-item', { active: selectedCategory === null }]"
            @click="selectedCategory = null"
          >
            <FolderOpen :size="16" />
            <span>All Documents</span>
            <span class="count">{{ store.documents.length }}</span>
          </li>
          <li
            v-for="cat in store.categories"
            :key="cat.id"
            :class="['cat-item', { active: selectedCategory === cat.id }]"
            @click="selectedCategory = cat.id"
          >
            <FolderOpen :size="16" />
            <span>{{ cat.name }}</span>
          </li>
        </ul>
      </aside>

      <!-- Documents Area -->
      <main class="docs-area">
        <!-- Loading -->
        <div v-if="store.loading" class="state-box">
          <Loader2 :size="52" class="animate-spin" />
          <p>Loading documents…</p>
        </div>

        <!-- Empty -->
        <div v-else-if="store.documents.length === 0" class="state-box empty">
          <FolderOpen :size="72" />
          <h2>No documents found</h2>
          <p>Try a different search term or category.</p>
          <button class="btn-primary" @click="clearFilters">Clear Filters</button>
        </div>

        <!-- Grid / List -->
        <div v-else :class="['docs-grid', viewMode]">
          <DocumentCard
            v-for="doc in store.documents"
            :key="doc.id"
            :doc="doc"
            :list-mode="viewMode === 'list'"
          />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Hero */
.repo-hero {
  position: relative;
  overflow: hidden;
  padding: 7rem 2rem 6rem;
  background: var(--bg-dark);
}

.repo-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary-dark) 0%, #1e1b4b 100%);
  z-index: 0;
}

.repo-hero .container { position: relative; z-index: 2; }
.repo-hero .section-eyebrow { color: var(--accent-teal); letter-spacing: 0.2em; }
.repo-hero .section-title   { color: white; font-size: clamp(2.5rem, 5vw, 3.8rem); margin-bottom: 1.2rem; text-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.repo-hero .section-subtitle { color: rgba(255,255,255,0.8); max-width: 600px; font-size: 1.1rem; }

/* Aurora Shapes */
.hero-shapes { position: absolute; inset: 0; z-index: 1; pointer-events: none; overflow: hidden; }
.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 10s ease-in-out infinite alternate;
}
.s1 { background: var(--primary-color); width: 500px; height: 500px; top: -150px; right: -100px; animation-delay: 0s; }
.s2 { background: var(--secondary-color); width: 400px; height: 400px; bottom: -100px; right: 25%; animation-delay: -3s; }
.s3 { background: var(--accent-teal); width: 300px; height: 300px; top: 20%; right: 45%; animation-delay: -5s; opacity: 0.4; }

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-30px, 30px) scale(1.1); }
}

/* Toolbar */
.toolbar {
  position: sticky;
  top: 90px;
  z-index: 100;
  max-width: 900px;
  margin: -2.2rem auto 3rem;
  border-radius: 50px;
  padding: 0.6rem 1rem;
  box-shadow: 0 16px 40px rgba(0,0,0,0.12), 0 0 0 1px rgba(255,255,255,0.4) inset;
  backdrop-filter: blur(30px) saturate(200%);
  -webkit-backdrop-filter: blur(30px) saturate(200%);
  background: rgba(255,255,255,0.85);
}

.toolbar-inner {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toolbar-search {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.toolbar-search input {
  width: 100%;
  padding: 12px 42px;
  border: none;
  border-radius: 50px;
  font-family: inherit;
  font-size: 0.95rem;
  background: transparent;
  color: var(--text-main);
  transition: var(--transition-smooth);
}

.toolbar-search input:focus {
  outline: none;
}

.ts-icon {
  position: absolute;
  left: 15px;
  color: var(--text-secondary);
  pointer-events: none;
}

.clear-search {
  position: absolute;
  right: 14px;
  background: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
}

.view-toggle {
  display: flex;
  gap: 4px;
  background: rgba(0,0,0,0.04);
  border-radius: 50px;
  padding: 4px;
}

.vt-btn {
  background: transparent;
  color: var(--text-secondary);
  width: 38px; height: 38px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  transition: var(--transition-smooth);
}

.vt-btn.active {
  background: white;
  color: var(--primary-color);
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

/* Layout */
.repo-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2rem;
  padding-top: 2rem;
  padding-bottom: 4rem;
  align-items: start;
}

/* Sidebar */
.sidebar {
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  position: sticky;
  top: 140px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--text-main);
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-subtle);
}

.clear-all {
  margin-left: auto;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--primary-color);
  background: none;
  text-decoration: underline;
}

.cat-list { list-style: none; display: flex; flex-direction: column; gap: 3px; }

.cat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-smooth);
  border-left: 3px solid transparent;
}

.cat-item:hover {
  background: rgba(0,120,212,0.06);
  color: var(--primary-color);
}

.cat-item.active {
  background: linear-gradient(90deg, rgba(0,106,220,0.08) 0%, transparent 100%);
  color: var(--primary-color);
  font-weight: 700;
  border-left-color: var(--primary-color);
}

.cat-item .count {
  margin-left: auto;
  font-size: 0.75rem;
  background: rgba(0,0,0,0.05);
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 600;
}

.cat-item.active .count {
  background: rgba(0,106,220,0.15);
  color: var(--primary-color);
}

/* Docs grid */
.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.docs-grid.list {
  grid-template-columns: 1fr;
}

/* States */
.state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem;
  text-align: center;
  color: var(--text-secondary);
  gap: 1.2rem;
  background: rgba(255,255,255,0.5);
  border-radius: var(--border-radius-lg);
  border: 1px dashed var(--border-subtle);
}

.state-box.empty svg {
  color: var(--primary-light);
  filter: drop-shadow(0 10px 20px rgba(0,106,220,0.2));
  animation: float 6s ease-in-out infinite;
}

.state-box .animate-spin { color: var(--primary-color); }
.state-box h2 { font-size: 1.8rem; color: var(--text-main); }

@media (max-width: 900px) {
  .repo-layout { grid-template-columns: 1fr; }
  .sidebar { position: static; }
}

@media (max-width: 560px) {
  .view-toggle { display: none; }
}
</style>
