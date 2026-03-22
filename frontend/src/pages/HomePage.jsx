import { useState } from "react";
import { analyzePrompt, ApiError } from "../api";
import { Layout } from "../components";

export function HomePage() {
  const [step, setStep] = useState("input");
  const [error, setError] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorCode, setErrorCode] = useState(null);
  const [errorRequestId, setErrorRequestId] = useState(null);

  const handleAnalyze = async () => {
    setError(null);
    setErrorRequestId(null);
    setErrorCode(null);
    setResult(null);
    setLoading(true);
    try {
      const data = await analyzePrompt(prompt);
      setResult(data);
      setStep("analysis");
    } catch (err) {
      setError(err.message || "Erro ao analisar");
      if (err instanceof ApiError) {
        if (err.requestId) setErrorRequestId(err.requestId);
        if (err.code) setErrorCode(err.code);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setStep("input");
    setResult(null);
    setError(null);
    setErrorRequestId(null);
    setErrorCode(null);
  };

  return (
    <Layout>
      {step === "input" && (
        <section className="panel">
          <h2>Analisar prompt</h2>
          <p className="hint">
            Cole ou digite o texto do prompt. A análise usa LLM (OpenAI).
          </p>
          <label htmlFor="prompt">Prompt</label>
          <textarea
            id="prompt"
            className="input"
            rows={8}
            placeholder="Ex.: Você é um assistente. Explique em 3 passos como..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <div className="form-actions">
            <button
              type="button"
              className="btn primary"
              onClick={handleAnalyze}
              disabled={loading || !prompt.trim()}
            >
              {loading ? "Analisando…" : "Analisar"}
            </button>
          </div>

          {error && (
            <div className="result error" role="alert">
              <p className="error-message">{error}</p>
              {errorCode === "RATE_LIMIT_EXCEEDED" && (
                <p className="error-hint">Aguarde um minuto e tente novamente.</p>
              )}
              {errorRequestId && (
                <p className="error-request-id">Request ID: {errorRequestId}</p>
              )}
            </div>
          )}
        </section>
      )}

      {step === "analysis" && result && (
        <section className="panel analysis-panel">
          <div className="panel-header">
            <h2>Análise</h2>
            <button
              type="button"
              className="btn secondary"
              onClick={handleNewAnalysis}
            >
              Nova análise
            </button>
          </div>
          <div className="result analysis-result">
            {result.summary && (
              <p className="analysis-summary">{result.summary}</p>
            )}
            <div className="metrics">
              <div className="score-row">
                <span className="score-label">Clareza (LLM)</span>
                <span>{result.clarity_score}/10</span>
              </div>
              <div className="score-row">
                <span className="score-label">Palavras</span>
                <span>{result.word_count}</span>
              </div>
              <div className="score-row">
                <span className="score-label">Caracteres</span>
                <span>{result.char_count}</span>
              </div>
              <div className="score-row">
                <span className="score-label">Linhas</span>
                <span>{result.line_count}</span>
              </div>
              <div className="score-row">
                <span className="score-label">Tokens (est.)</span>
                <span>{result.estimated_tokens}</span>
              </div>
            </div>
            <p className="checklist-heading">Critérios</p>
            <ul className="checklist">
              <li
                className={
                  result.has_instructions
                    ? "checklist-item checked"
                    : "checklist-item"
                }
              >
                <span className="checklist-box" aria-hidden="true">
                  {result.has_instructions ? "✓" : ""}
                </span>
                <span className="checklist-label">Instruções</span>
              </li>
              <li
                className={
                  result.has_examples ? "checklist-item checked" : "checklist-item"
                }
              >
                <span className="checklist-box" aria-hidden="true">
                  {result.has_examples ? "✓" : ""}
                </span>
                <span className="checklist-label">Exemplos</span>
              </li>
            </ul>
            {result.suggestions && result.suggestions.length > 0 && (
              <>
                <p className="sections-title">Sugestões</p>
                <ul className="sections-list">
                  {result.suggestions.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </>
            )}
            {result.sections && result.sections.length > 0 && (
              <>
                <p className="sections-title">Seções detectadas</p>
                <ul className="sections-list">
                  {result.sections.map((s, i) => (
                    <li key={i}>
                      {s}
                      {s.length >= 80 ? "…" : ""}
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
        </section>
      )}
    </Layout>
  );
}
