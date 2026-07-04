<script setup>
import { FileText, Download, Calendar, ExternalLink, Eye, BookOpen } from 'lucide-vue-next'

const props = defineProps({
  doc:      { type: Object, required: true },
  listMode: { type: Boolean, default: false }
})

const emit = defineEmits(['preview', 'flipbook'])

const formatDate = (d) =>
  new Date(d).toLocaleDateString('en-US', { year:'numeric', month:'short', day:'numeric' })

const ext = (filename) => filename?.split('.').pop().toUpperCase() ?? 'FILE'

const extColor = (e) => ({
  'PDF': '#d13438', 'DOCX': '#0078d4', 'DOC': '#0078d4', 'XLSX': '#107c10'
}[e] ?? '#5c2d91')
</script>

<template>
  <div :class="['doc-card glass', { 'list-mode': listMode }]">
    <!-- File Badge -->
    <div class="file-badge" :style="{ background: extColor(ext(doc.file)) }">
      <FileText :size="22" color="white" />
      <span>{{ ext(doc.file) }}</span>
    </div>

    <div class="card-info">
      <div class="cat-tag">{{ doc.category_name }}</div>
      <h3 class="doc-title">{{ doc.title }}</h3>
      <p class="doc-desc" v-if="doc.description">{{ doc.description }}</p>
    </div>

    <div class="card-footer">
      <div class="meta">
        <Calendar :size="13" />
        <span>{{ formatDate(doc.uploaded_at) }}</span>
      </div>
      <div class="actions">
        <button 
          v-if="ext(doc.file) === 'PDF'" 
          @click.prevent="emit('flipbook', doc)" 
          class="action-btn fb" 
          title="Flipbook View"
        >
          <BookOpen :size="17" />
        </button>
        <button @click.prevent="emit('preview', doc)" class="action-btn" title="Preview">
          <Eye :size="17" />
        </button>
        <a :href="doc.file" download class="action-btn dl" title="Download">
          <Download :size="17" />
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.doc-card {
  padding: 1.6rem;
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  transition: var(--transition-smooth);
  border: 1px solid transparent;
}

.doc-card:hover {
  transform: translateY(-6px);
  background: white;
  box-shadow: var(--card-shadow-hover);
  border-color: rgba(0,120,212,0.15);
}

/* List mode overrides */
.doc-card.list-mode {
  flex-direction: row;
  align-items: center;
  height: auto;
  padding: 1.2rem 1.6rem;
}

.doc-card.list-mode:hover { transform: translateX(6px) translateY(0); }
.doc-card.list-mode .doc-desc { display: none; }
.doc-card.list-mode .card-info { flex: 1; }

/* File badge */
.file-badge {
  width: 52px; height: 52px;
  border-radius: 14px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 1px;
  flex-shrink: 0;
  box-shadow: 0 6px 18px rgba(0,0,0,0.18);
}

.file-badge span {
  font-size: 0.55rem;
  font-weight: 900;
  color: white;
  letter-spacing: 0.05em;
}

/* Info */
.cat-tag {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--primary-color);
  margin-bottom: 4px;
}

.doc-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.doc-desc {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-top: 6px;
}

/* Footer */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--border-subtle);
  margin-top: auto;
}

.doc-card.list-mode .card-footer {
  padding-top: 0;
  border-top: none;
  margin-top: 0;
}

.meta {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8rem;
  color: var(--text-light);
}

.actions { display: flex; gap: 6px; }

.action-btn {
  width: 36px; height: 36px;
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  background: #f4f4f4;
  color: var(--text-secondary);
  transition: var(--transition-smooth);
}

.action-btn:hover       { background: var(--primary-color); color: white; }
.action-btn.fb:hover    { background: #5c2d91; }
.action-btn.dl:hover    { background: #107c10; }
</style>
