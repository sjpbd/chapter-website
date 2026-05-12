<script setup>
import { X, Download, Maximize2 } from 'lucide-vue-next'
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
  doc: { type: Object, required: true },
  isOpen: { type: Boolean, required: true }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

// Prevent background scrolling when modal is open
onMounted(() => {
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="close">
        <div class="modal-container">
          <header class="modal-header">
            <div class="modal-title">
              <h3>{{ doc.title }}</h3>
              <span class="file-tag">{{ doc.category_name }}</span>
            </div>
            <div class="modal-actions">
              <a :href="doc.file" target="_blank" title="Open in new tab" class="icon-btn">
                <Maximize2 :size="18" />
              </a>
              <a :href="doc.file" download title="Download" class="icon-btn">
                <Download :size="18" />
              </a>
              <button @click="close" class="icon-btn close-btn" title="Close">
                <X :size="20" />
              </button>
            </div>
          </header>
          
          <div class="modal-body">
            <!-- Native browser PDF rendering using object/iframe -->
            <iframe :src="doc.file + '#toolbar=1&navpanes=0&scrollbar=1'" class="pdf-frame" frameborder="0"></iframe>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.modal-container {
  background: white;
  width: 100%;
  max-width: 1000px;
  height: 90vh;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  animation: modal-slide-up 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fdfdfd;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-title h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-main);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 400px;
}

.file-tag {
  font-size: 0.7rem;
  font-weight: 700;
  background: rgba(0,120,212,0.1);
  color: var(--primary-color);
  padding: 3px 8px;
  border-radius: 20px;
  text-transform: uppercase;
}

.modal-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: transparent;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.icon-btn:hover {
  background: rgba(0,0,0,0.05);
  color: var(--primary-color);
}

.close-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}

.modal-body {
  flex: 1;
  background: #e5e7eb;
  padding: 0;
  position: relative;
}

.pdf-frame {
  width: 100%;
  height: 100%;
  border: none;
  background: #525659; /* Default PDF viewer background */
}

/* Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@keyframes modal-slide-up {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 768px) {
  .modal-overlay { padding: 1rem; }
  .modal-container { height: 95vh; }
  .modal-title h3 { max-width: 200px; }
  .file-tag { display: none; }
}
</style>
