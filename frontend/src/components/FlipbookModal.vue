<script setup>
import { X, Loader2, RefreshCw, BookOpen, Share2, Check, Download, Layers, ShieldAlert } from 'lucide-vue-next'
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  doc: { type: Object, required: true },
  isOpen: { type: Boolean, required: true }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

// Check if the device is mobile
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)

// Ensure absolute URL
const absoluteUrl = computed(() => {
  if (!props.doc?.file) return ''
  let url = props.doc.file
  if (url.includes('localhost:8000')) {
    url = url.replace(/^https?:\/\/localhost:8000/, '')
  }
  if (url.startsWith('http')) return url
  return window.location.origin + url
})

const isLoading = ref(true)
const is3DMode = ref(!isMobile) // Default to 2D on mobile for better performance, 3D on desktop
const isLinkCopied = ref(false)
const flipbookContainerRef = ref(null)
const loadError = ref(null)
let flipbookInstance = null

const copyShareLink = async () => {
  const shareUrl = `${window.location.origin}/repository?doc=${props.doc.id}&view=flipbook`
  try {
    await navigator.clipboard.writeText(shareUrl)
    isLinkCopied.value = true
    setTimeout(() => { isLinkCopied.value = false }, 2000)
  } catch (err) {
    console.error('Failed to copy link:', err)
  }
}

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

// Convert CDN script to local Blob URL to bypass same-origin Web Worker policies
const getBlobUrl = async (url) => {
  try {
    const res = await fetch(url)
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
    const blob = await res.blob()
    return URL.createObjectURL(blob)
  } catch (e) {
    console.warn(`Failed to create blob URL for ${url}:`, e)
    return url
  }
}

const initFlipbook = async () => {
  isLoading.value = true
  loadError.value = null
  
  try {
    // 1. Load styles
    loadCSS('https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/css/dflip.min.css')
    loadCSS('https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/css/themify-icons.min.css')
    
    // 2. Load jQuery
    await loadScript('https://code.jquery.com/jquery-3.7.1.min.js')
    
    // 3. Resolve PDF.js CDN paths with Blob workarounds to prevent worker SecurityError
    const workerCdn = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/pdf.worker.min.js'
    const workerBlobUrl = await getBlobUrl(workerCdn)

    window.DFLIP = window.DFLIP || {}
    window.DFLIP.defaults = window.DFLIP.defaults || {}
    window.DFLIP.defaults.pdfjsSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/pdf.min.js'
    window.DFLIP.defaults.pdfjsWorkerSrc = workerBlobUrl
    window.DFLIP.defaults.threejsSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/three.min.js'
    window.DFLIP.defaults.mockupjsSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/mockup.min.js'
    window.DFLIP.defaults.mockupSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/mockup.min.js'
    window.DFLIP.defaults.soundFile = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/sound/turn2.mp3'

    window.DEARFLIP = window.DEARFLIP || {}
    window.DEARFLIP.defaults = window.DEARFLIP.defaults || {}
    window.DEARFLIP.defaults.pdfjsSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/pdf.min.js'
    window.DEARFLIP.defaults.pdfjsWorkerSrc = workerBlobUrl
    window.DEARFLIP.defaults.threejsSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/three.min.js'
    window.DEARFLIP.defaults.mockupjsSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/mockup.min.js'
    window.DEARFLIP.defaults.mockupSrc = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/mockup.min.js'
    window.DEARFLIP.defaults.soundFile = 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/sound/turn2.mp3'

    // 4. Load DearFlip JS
    await loadScript('https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/dflip.min.js')
    
    await nextTick()
    
    if (window.jQuery && window.jQuery.fn.flipBook && flipbookContainerRef.value) {
      // Clear previous container contents
      flipbookContainerRef.value.innerHTML = ''
      
      // Initialize the Flipbook
      flipbookInstance = window.jQuery(flipbookContainerRef.value).flipBook(absoluteUrl.value, {
        webgl: is3DMode.value,
        height: '100%',
        duration: 800,
        pdfjsSrc: 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/pdf.min.js',
        pdfjsWorkerSrc: workerBlobUrl,
        threejsSrc: 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/three.min.js',
        mockupjsSrc: 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/mockup.min.js',
        mockupSrc: 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/js/libs/mockup.min.js',
        soundFile: 'https://cdn.jsdelivr.net/npm/@dearhive/dearflip-jquery-flipbook/dflip/sound/turn2.mp3'
      })
      
      // DearFlip loads PDF asynchronously. Let's hide the overlay spinner shortly after loading starts.
      setTimeout(() => {
        isLoading.value = false
      }, 1500)
    } else {
      throw new Error('DearFlip jQuery plugin is not initialized')
    }
  } catch (error) {
    console.error('Failed to load Flipbook:', error)
    loadError.value = 'Failed to load flipbook components. Please check your network connection or try 2D view.'
    isLoading.value = false
  }
}

const toggleMode = () => {
  is3DMode.value = !is3DMode.value
  if (flipbookInstance && typeof flipbookInstance.dispose === 'function') {
    try {
      flipbookInstance.dispose()
    } catch (e) {
      console.warn(e)
    }
  }
  initFlipbook()
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  initFlipbook()
})

onUnmounted(() => {
  document.body.style.overflow = ''
  if (flipbookInstance && typeof flipbookInstance.dispose === 'function') {
    try {
      flipbookInstance.dispose()
    } catch (e) {
      console.warn(e)
    }
  }
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="close">
        <div class="modal-container">
          <header class="modal-header">
            <div class="modal-title">
              <BookOpen :size="20" class="title-icon" />
              <h3>{{ doc.title }} — 3D Flipbook</h3>
              <span class="file-tag">Flipbook</span>
            </div>

            <!-- 2D / 3D Mode Toggle -->
            <div class="mode-toggle">
              <button 
                :class="['toggle-btn', { active: is3DMode }]" 
                @click="toggleMode"
                title="3D WebGL mode gives a realistic page flipping effect"
              >
                3D View
              </button>
              <button 
                :class="['toggle-btn', { active: !is3DMode }]" 
                @click="toggleMode"
                title="2D HTML mode is faster and works everywhere, including old devices"
              >
                2D View
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
              <a :href="absoluteUrl" download title="Download PDF" class="icon-btn">
                <Download :size="18" />
              </a>
              <button @click="close" class="icon-btn close-btn" title="Close">
                <X :size="20" />
              </button>
            </div>
          </header>
          
          <div class="modal-body">
            <!-- 3D Flipbook Container -->
            <div ref="flipbookContainerRef" class="flipbook-canvas"></div>

            <!-- Loading overlay -->
            <div class="overlay-state loading" v-if="isLoading">
              <Loader2 class="animate-spin" :size="40" />
              <p>Preparing 3D Flipbook...</p>
              <span class="subtext">Rendering PDF pages into interactive book layout</span>
            </div>

            <!-- Error overlay -->
            <div class="overlay-state error" v-if="loadError">
              <ShieldAlert :size="48" class="error-icon" />
              <p>{{ loadError }}</p>
              <button @click="toggleMode" class="btn-retry">
                <RefreshCw :size="16" />
                <span>Switch to {{ is3DMode ? '2D HTML' : '3D WebGL' }} Mode</span>
              </button>
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
  background: rgba(10, 18, 30, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal-container {
  background: #1e1e24; /* Sleek dark mode background specifically for reading */
  width: 100%;
  max-width: 1200px;
  height: 92vh;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 35px 70px -15px rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  animation: modal-slide-up 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #18181c;
  gap: 1rem;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  flex: 1;
  color: #ffffff;
}

.title-icon {
  color: var(--primary-light, #0078d4);
  flex-shrink: 0;
}

.modal-title h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-tag {
  font-size: 0.65rem;
  font-weight: 700;
  background: rgba(0, 120, 212, 0.2);
  color: #3aa0ff;
  padding: 3px 9px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  flex-shrink: 0;
}

/* 2D / 3D Mode Toggle */
.mode-toggle {
  display: flex;
  background: rgba(255, 255, 255, 0.06);
  padding: 3px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
}

.toggle-btn {
  border: none;
  background: transparent;
  padding: 6px 14px;
  font-size: 0.8rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.6);
  border-radius: 9px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn.active {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.modal-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.icon-btn {
  background: transparent;
  border: none;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.close-btn:hover {
  background: rgba(220, 38, 38, 0.2);
  color: #ef4444;
  border-color: rgba(220, 38, 38, 0.3);
}

.icon-btn.copied {
  color: #4ade80 !important;
  background: rgba(74, 222, 128, 0.1) !important;
  border-color: rgba(74, 222, 128, 0.2) !important;
}

.modal-body {
  flex: 1;
  background: #141416;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.flipbook-canvas {
  width: 100%;
  height: 100%;
}

/* Overlay loading / error states */
.overlay-state {
  position: absolute;
  inset: 0;
  background: #141416;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.9);
  z-index: 10;
  padding: 2rem;
  text-align: center;
}

.overlay-state svg.animate-spin {
  color: var(--primary-light, #3aa0ff);
}

.overlay-state p {
  margin: 0;
  font-weight: 600;
  font-size: 1.05rem;
}

.overlay-state .subtext {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

.error-icon {
  color: #ef4444;
}

.btn-retry {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary-color, #0078d4);
  color: white;
  border: none;
  border-radius: 30px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 15px rgba(0, 120, 212, 0.4);
}

.btn-retry:hover {
  transform: translateY(-2px);
  background: #0086f0;
  box-shadow: 0 6px 20px rgba(0, 120, 212, 0.5);
}

/* Animations */
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
    transform: translateY(35px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 768px) {
  .modal-overlay { padding: 0.75rem; }
  .modal-container { height: 94vh; }
  .modal-header {
    flex-wrap: wrap;
    padding: 0.8rem 1rem;
    gap: 0.75rem;
  }
  .modal-title h3 { max-width: 150px; }
  .file-tag { display: none; }
  .mode-toggle {
    order: 3;
    width: 100%;
    justify-content: center;
  }
}
</style>
