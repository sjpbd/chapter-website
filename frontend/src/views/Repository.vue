<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDocumentStore } from '../store/documentStore'
import { useRoute, useRouter } from 'vue-router'
import GlobalSearch from '../components/GlobalSearch.vue'
import DocumentCard from '../components/DocumentCard.vue'
import PDFModal from '../components/PDFModal.vue'
import { Search, SlidersHorizontal, Loader2, FolderOpen, LayoutGrid, List, X } from 'lucide-vue-next'

const store    = useDocumentStore()
const route    = useRoute()
const router   = useRouter()

const searchQuery      = ref(route.query.search ?? '')
const selectedCategory = ref(null)
const viewMode         = ref('grid')
let debounceTimer      = null

const selectedDoc = ref(null)
const isModalOpen = ref(false)

const openPreview = (doc) => {
  selectedDoc.value = doc
  isModalOpen.value = true
}

const closePreview = () => {
  isModalOpen.value = false
  setTimeout(() => { selectedDoc.value = null }, 300) // Clear after animation finishes
}

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
        <div class="toolbar-search" style="flex: 1; display: flex; max-width: 400px;">
          <GlobalSearch style="width: 100%; max-width: 100%;" />
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
        <div v-if="store.loading" :class="['docs-grid', viewMode]">
          <div v-for="n in 6" :key="n" :class="['skeleton-card glass', { 'list-mode': viewMode === 'list' }]">
            <div class="skeleton-badge shimmer"></div>
            <div class="skeleton-info">
              <div class="skeleton-line tag shimmer"></div>
              <div class="skeleton-line title shimmer"></div>
              <div class="skeleton-line desc shimmer" v-if="viewMode === 'grid'"></div>
            </div>
            <div class="skeleton-footer">
              <div class="skeleton-line meta shimmer"></div>
              <div class="skeleton-actions">
                <div class="skeleton-btn shimmer"></div>
                <div class="skeleton-btn shimmer"></div>
              </div>
            </div>
          </div>
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
            @preview="openPreview"
          />
        </div>
      </main>
    </div>

    <!-- PDF Preview Modal -->
    <PDFModal 
      v-if="selectedDoc" 
      :doc="selectedDoc" 
      :is-open="isModalOpen" 
      @close="closePreview" 
    />
  </div>
</template>

<style scoped>
.repository-page {
  width: 100%;
  overflow-x: hidden;
}

/* Hero */
.repo-hero {
  position: relative;
  overflow: hidden;
  padding: 8rem 2rem 6.5rem;
  background: var(--bg-dark);
}

.repo-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary-dark) 0%, #0f172a 100%);
  z-index: 0;
}

.repo-hero .container { position: relative; z-index: 2; }
.repo-hero .section-eyebrow { color: var(--accent-teal); letter-spacing: 0.25em; text-transform: uppercase; font-weight: 700; font-size: 0.85rem; }
.repo-hero .section-title   { color: white; font-size: clamp(2.5rem, 5vw, 3.8rem); font-weight: 800; margin-bottom: 1.2rem; text-shadow: 0 4px 20px rgba(0,0,0,0.35); }
.repo-hero .section-subtitle { color: rgba(255,255,255,0.85); max-width: 600px; font-size: 1.1rem; line-height: 1.6; }

/* Aurora Shapes */
.hero-shapes { position: absolute; inset: 0; z-index: 1; pointer-events: none; overflow: hidden; }
.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.5;
  animation: float 16s ease-in-out infinite alternate;
}
.s1 { background: var(--primary-color); width: 600px; height: 600px; top: -200px; right: -150px; animation-name: floatS1; }
.s2 { background: var(--secondary-color); width: 500px; height: 500px; bottom: -150px; right: 20%; animation-name: floatS2; animation-delay: -4s; }
.s3 { background: var(--accent-teal); width: 350px; height: 350px; top: 15%; right: 40%; animation-name: floatS3; animation-delay: -8s; opacity: 0.3; }

@keyframes floatS1 {
  0% { transform: translate(0, 0) scale(1) rotate(0deg); }
  100% { transform: translate(-60px, 40px) scale(1.1) rotate(45deg); }
}
@keyframes floatS2 {
  0% { transform: translate(0, 0) scale(1) rotate(0deg); }
  100% { transform: translate(40px, -50px) scale(1.15) rotate(-60deg); }
}
@keyframes floatS3 {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-30px, 30px) scale(1.2); }
}

/* Toolbar */
.toolbar {
  position: sticky;
  top: 100px;
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
  top: 160px;
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.55);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.03);
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
  transition: opacity 0.2s ease;
}
.clear-all:hover {
  opacity: 0.8;
}

.cat-list { list-style: none; display: flex; flex-direction: column; gap: 4px; }

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
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-left: 3px solid transparent;
}

.cat-item:hover {
  background: rgba(0,120,212,0.06);
  color: var(--primary-color);
  transform: translateX(4px);
}

.cat-item.active {
  background: linear-gradient(90deg, rgba(0,106,220,0.08) 0%, transparent 100%);
  color: var(--primary-color);
  font-weight: 700;
  border-left-color: var(--primary-color);
  box-shadow: inset 1px 0 0 rgba(0, 120, 212, 0.1);
}

.cat-item .count {
  margin-left: auto;
  font-size: 0.75rem;
  background: rgba(0,0,0,0.05);
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s ease;
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
  .repo-layout {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding-top: 1rem;
  }
  
  .sidebar {
    position: sticky;
    top: 84px; /* Sticks right below the 84px header navbar */
    z-index: 90;
    padding: 0.8rem 1rem;
    margin: 0 -1.2rem; /* Full edge-to-edge bleed for swiping */
    border-radius: 0;
    border-left: none;
    border-right: none;
    border-top: 1px solid rgba(0, 106, 220, 0.08);
    border-bottom: 1px solid rgba(0, 106, 220, 0.08);
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  }
  
  .sidebar-header {
    display: none; /* Hide filter header on mobile to conserve space */
  }
  
  .cat-list {
    flex-direction: row;
    overflow-x: auto;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    padding: 0.2rem 0.5rem;
    gap: 0.5rem;
  }
  
  .cat-list::-webkit-scrollbar {
    display: none; /* Hide scrollbars for native swiping look */
  }
  
  .cat-item {
    padding: 10px 18px; /* Slightly taller and wider for easier finger tapping */
    border-radius: 30px; /* Pill capsule look */
    border: 1px solid rgba(0, 106, 220, 0.08); /* Soft blue border to make them look like buttons */
    background: rgba(255, 255, 255, 0.95); /* High-contrast white background */
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 600;
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
  }
  
  .cat-item:hover {
    transform: none; /* Disable desktop translation on hover */
    background: rgba(0, 120, 212, 0.05);
    border-color: rgba(0, 106, 220, 0.15);
  }
  
  .cat-item.active {
    background: var(--primary-color) !important;
    background-image: none !important; /* Cancel desktop gradient */
    border-color: var(--primary-color) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(0, 106, 220, 0.25) !important;
    font-weight: 700;
  }
  
  .cat-item .count {
    margin-left: 6px;
    background: rgba(0, 0, 0, 0.05);
    color: var(--text-secondary);
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    transition: all 0.25s ease;
  }
  
  .cat-item.active .count {
    background: rgba(255, 255, 255, 0.25) !important;
    color: white !important;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem !important;
  }
  .repo-hero {
    padding: 7rem 1rem 5.5rem;
  }
  .toolbar {
    margin: -1.5rem 1rem 2rem;
    border-radius: 24px;
    padding: 0.5rem;
  }
}

@media (max-width: 560px) {
  .view-toggle { display: none; }
}

/* Skeleton Loader */
.skeleton-card {
  padding: 1.6rem;
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  height: 240px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
}

.skeleton-card.list-mode {
  flex-direction: row;
  align-items: center;
  height: auto;
  padding: 1.2rem 1.6rem;
}

.skeleton-badge {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.skeleton-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-line {
  height: 12px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.skeleton-line.tag { width: 30%; height: 10px; }
.skeleton-line.title { width: 85%; height: 16px; margin-top: 4px; }
.skeleton-line.desc { width: 60%; height: 12px; margin-top: 8px; }

.skeleton-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--border-subtle);
  margin-top: auto;
}

.skeleton-card.list-mode .skeleton-footer {
  padding-top: 0;
  border-top: none;
  margin-top: 0;
  gap: 12px;
}

.skeleton-line.meta { width: 80px; height: 10px; }

.skeleton-actions { display: flex; gap: 6px; }
.skeleton-btn {
  width: 36px;
  height: 36px;
  border-radius: 9px;
  background: rgba(0, 0, 0, 0.05);
}

/* Shimmer Animation */
.shimmer {
  position: relative;
}

.shimmer::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

/* Animation classes */
.state-box.empty {
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
