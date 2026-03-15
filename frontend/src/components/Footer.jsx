import { API_BASE } from '../api'

export function Footer() {
  return (
    <footer className="footer">
      <a href={`${API_BASE}/docs`} target="_blank" rel="noreferrer">
        Documentação da API (OpenAPI)
      </a>
      {' · '}
      <a href={`${API_BASE}/health`} target="_blank" rel="noreferrer">
        Health
      </a>
    </footer>
  )
}
