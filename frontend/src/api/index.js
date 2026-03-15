/** Cliente HTTP para a API Prompt Lens. */

export const API_BASE =
  (import.meta.env.VITE_API_URL && import.meta.env.VITE_API_URL.replace(/\/$/, '')) || 'http://localhost:8000'
const API_BASE_FULL = `${API_BASE}/api/v1`

/**
 * Erro da API com detail, request_id e code (quando a API retorna erro estruturado).
 */
export class ApiError extends Error {
  constructor(message, { status, requestId, code, detail } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.requestId = requestId
    this.code = code
    this.detail = detail
  }
}

export async function request(endpoint, options = {}) {
  const { method = 'GET', body } = options
  const res = await fetch(`${API_BASE_FULL}${endpoint}`, {
    method,
    headers: { 'Content-Type': 'application/json' },
    ...(body && { body: JSON.stringify(body) }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const detail = err.detail ?? res.statusText
    const message = typeof detail === 'string' ? detail : (detail[0]?.msg || res.statusText)
    const apiError = new ApiError(message, {
      status: res.status,
      requestId: err.request_id,
      code: err.code,
      detail: err.detail,
    })
    throw apiError
  }
  return res.json()
}

export async function analyzePrompt(prompt) {
  return request('/analyze', { method: 'POST', body: { prompt } })
}

export async function getStats() {
  return request('/stats', { method: 'GET' })
}

export const api = { analyzePrompt, getStats }
