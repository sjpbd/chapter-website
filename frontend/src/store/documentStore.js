import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export const useDocumentStore = defineStore('documents', {
  state: () => ({
    categories: [],
    documents: [],
    sliders: [],
    features: [],
    stats: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchCategories() {
      try {
        const res = await axios.get(`${API_BASE}/categories/?show_in_sidebar=true`)
        this.categories = res.data
      } catch (err) {
        this.error = err.message
      }
    },
    async fetchDocuments(params = {}) {
      this.loading = true
      try {
        const res = await axios.get(`${API_BASE}/documents/`, { params })
        this.documents = res.data
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    async fetchSliders() {
      try {
        const res = await axios.get(`${API_BASE}/sliders/`)
        this.sliders = res.data
      } catch (err) {
        this.error = err.message
      }
    },
    async fetchFeatures() {
      try {
        const res = await axios.get(`${API_BASE}/features/`)
        this.features = res.data
      } catch (err) {
        this.error = err.message
      }
    },
    async fetchStats() {
      try {
        const res = await axios.get(`${API_BASE}/stats/`)
        this.stats = res.data
      } catch (err) {
        this.error = err.message
      }
    }
  }
})
