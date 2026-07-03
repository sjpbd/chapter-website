<script setup>
import { X, Download, Maximize2, Loader2, Share2, Check } from 'lucide-vue-next'
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  doc: { type: Object, required: true },
  isOpen: { type: Boolean, required: true }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

// Determine if the device is mobile
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)

// Ensure the file URL is absolute for external viewers (like Google Docs Viewer)
const absoluteUrl = computed(() => {
  if (!props.doc?.file) return ''
  let url = props.doc.file
  if (url.includes('localhost:8000')) {
    url = url.replace(/^https?:\/\/localhost:8000/, '')
  }
  if (url.startsWith('http')) return url
  return window.location.origin + url
})

const isPdf = computed(() => {
  return props.doc?.file?.toLowerCase().endsWith('.pdf')
})

const viewType = ref('normal')
const isLoadingFlipbook = ref(false)
const flipbookContainerRef = ref(null)
const isLinkCopied = ref(false)

const copyShareLink = async () => {
  const shareUrl = `${window.location.origin}/repository?doc=${props.doc.id}`
  try {
    await navigator.clipboard.writeText(shareUrl)
    isLinkCopied.value = true
    setTimeout(() => { isLinkCopied.value = false }, 2000)
  } catch (err) {
    console.error('Failed to copy link:', err)
  }
}

// For mobile and non-PDF files, Google Docs Viewer provides a much better "direct" experience
const viewerUrl = computed(() => {
  if (!absoluteUrl.value) return ''
  
  // If it's a PDF on desktop, use native browser viewer (better performance/features)
  if (isPdf.value && !isMobile) {
    return absoluteUrl.value + '#toolbar=1&navpanes=0&scrollbar=1'
  }
  
  // Otherwise, use Google Docs Viewer for a consistent "inline" experience
  return `https://docs.google.com/viewer?url=${encodeURIComponent(absoluteUrl.value)}&embedded=true`
})

// Dynamic Script & CSS Loaders to avoid loading flipbook assets when not used
function loadScript(url) {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${url}"]`)) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = url
    script.async = true
    script.onload = () => resolve()
    script.onerror = () => reject()
    document.head.appendChild(script)
  })
}

function loadCSS(url) {
  if (document.querySelector(`link[href="${url}"]`)) return
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = url
  document.head.appendChild(link)
}

const switchToFlipbook = async () => {
  viewType.value = 'flipbook'
  if (isLoadingFlipbook.value) return
  
  isLoadingFlipbook.value = true
  try {
    // 1. Load styles
    loadCSS('https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/css/dflip.min.css')
    loadCSS('https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/css/themify-icons.min.css')
    
    // 2. Load jQuery (required by DearFlip)
    await loadScript('https://code.jquery.com/jquery-3.7.1.min.js')
    
    // 3. Load DearFlip JS
    await loadScript('https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/dflip.min.js')
    
    // 4. Wait for DOM update and initialize flipbook
    await nextTick()
    
    if (window.jQuery && window.jQuery.fn.flipBook && flipbookContainerRef.value) {
      flipbookContainerRef.value.innerHTML = ''
      window.jQuery(flipbookContainerRef.value).flipBook(absoluteUrl.value, {
        webgl: true,
        height: '100%',
        duration: 800
      })
    }
  } catch (error) {
    console.error('Failed to load DearFlip flipbook library:', error)
  } finally {
    isLoadingFlipbook.value = false
  }
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

            <!-- View Mode Selector -->
            <div class="view-mode-selector" v-if="isPdf">
              <button 
                :class="['vms-btn', { active: viewType === 'normal' }]" 
                @click="viewType = 'normal'"
              >
                Standard View
              </button>
              <button 
                :class="['vms-btn', { active: viewType === 'flipbook' }]" 
                @click="switchToFlipbook"
              >
                Flipbook View 📖
              </button>
            </div>

            <div class="modal-actions">
              <button 
                @click="copyShareLink" 
                class="icon-btn" 
                :class="{ copied: isLinkCopied }"
                :title="isLinkCopied ? 'Link copied!' : 'Copy shareable link'"
              >
                <Check v-if="isLinkCopied" :size="18" />
                <Share2 v-else :size="18" />
              </button>
              <a :href="absoluteUrl" target="_blank" title="Open in new tab" class="icon-btn">
                <Maximize2 :size="18" />
              </a>
              <a :href="absoluteUrl" download title="Download" class="icon-btn">
                <Download :size="18" />
              </a>
              <button @click="close" class="icon-btn close-btn" title="Close">
                <X :size="20" />
              </button>
            </div>
          </header>
          
          <div class="modal-body">
            <!-- Standard PDF Viewer (Iframe) -->
            <iframe 
              v-if="viewType === 'normal'" 
              :src="viewerUrl" 
              class="pdf-frame" 
              frameborder="0"
            ></iframe>

            <!-- 3D Flipbook Viewer -->
            <div 
              v-else 
              ref="flipbookContainerRef" 
              class="flipbook-container"
            >
              <!-- Loading spinner -->
              <div class="flipbook-loader" v-if="isLoadingFlipbook">
                <Loader2 class="animate-spin" :size="36" />
                <p>Preparing 3D Flipbook...</p>
              </div>
            </div>
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
  gap: 1rem;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  flex: 1;
}

.modal-title h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-main);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-tag {
  font-size: 0.7rem;
  font-weight: 700;
  background: rgba(0,120,212,0.1);
  color: var(--primary-color);
  padding: 3px 8px;
  border-radius: 20px;
  text-transform: uppercase;
  flex-shrink: 0;
}

/* View Mode Selector styling */
.view-mode-selector {
  display: flex;
  background: rgba(0, 0, 0, 0.05);
  padding: 3px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.03);
  flex-shrink: 0;
}

.vms-btn {
  border: none;
  background: transparent;
  padding: 6px 14px;
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-secondary);
  border-radius: 9px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.vms-btn.active {
  background: white;
  color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 106, 220, 0.12);
}

.modal-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
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

.icon-btn.copied {
  color: #16a34a !important;
  background: rgba(22, 163, 74, 0.1) !important;
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
  background: #525659;
}

/* 3D Flipbook Viewer Container */
.flipbook-container {
  width: 100%;
  height: 100%;
  background: #333333;
  position: relative;
}

.flipbook-loader {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
}

.flipbook-loader svg {
  color: var(--primary-light);
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
  .modal-header {
    flex-wrap: wrap;
    padding: 0.8rem 1rem;
  }
  .modal-title {
    width: auto;
    flex: 1;
  }
  .modal-title h3 { max-width: 180px; }
  .file-tag { display: none; }
  .view-mode-selector {
    order: 3;
    width: 100%;
    margin-top: 0.5rem;
    justify-content: center;
  }
}
</style>
