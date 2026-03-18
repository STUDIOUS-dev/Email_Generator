import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000, // 2 minutes — scraping + LLM can be slow
  headers: { 'Content-Type': 'application/json' },
})

/**
 * Check API health and available LLM providers.
 * @returns {Promise<{status: string, providers: Array}>}
 */
export async function checkHealth() {
  const { data } = await api.get('/health')
  return data
}

/**
 * Generate a cold email from a job posting URL.
 * @param {object} payload
 * @param {string} payload.url              - Job posting URL
 * @param {string} payload.sender_name      - Sender's name (default: Mohan)
 * @param {string} payload.company_name     - Company name (default: AtliQ)
 * @param {string} payload.company_description - Short company description
 * @returns {Promise<{email: string, job: object, provider_used: string, portfolio_links: string[]}>}
 */
export async function generateEmail(payload) {
  const { data } = await api.post('/generate', payload)
  return data
}

export default api
