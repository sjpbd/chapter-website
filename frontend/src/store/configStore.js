import { defineStore } from 'pinia'
import axios from 'axios'

export const useConfigStore = defineStore('config', {
  state: () => ({
    siteName: 'SJP Chapter Hub',
    logo: null,
    favicon: null,
    footerText: '',
    isLoading: false,
    error: null
  }),

  actions: {
    async fetchConfig() {
      this.isLoading = true
      try {
        const baseUrl = import.meta.env.VITE_API_URL || ''
        const response = await axios.get(`${baseUrl}/api/config/`)
        const data = response.data
        
        this.siteName = data.site_name || 'SJP Chapter Hub'
        this.logo = data.logo
        this.favicon = data.favicon
        this.footerText = data.footer_text || ''
        
        // Update favicon dynamically if provided
        if (this.favicon) {
          let link = document.querySelector("link[rel~='icon']")
          if (!link) {
            link = document.createElement('link')
            link.rel = 'icon'
            document.head.appendChild(link)
          }
          link.href = this.favicon
        }
        
        // Update document title
        document.title = this.siteName
        
      } catch (err) {
        console.error('Failed to fetch site config:', err)
        this.error = 'Could not load site configuration'
      } finally {
        this.isLoading = false
      }
    }
  }
})
