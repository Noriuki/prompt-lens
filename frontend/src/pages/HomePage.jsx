import { useState } from "react";
import { analyzePrompt, ApiError } from "../api";
import { Layout } from "../components";

export function HomePage() {
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

  return (
    <Layout>
      <section className="panel">
        <h2>Analisar prompt</h2>
        <p className="hint">
          Cole ou digite o texto do prompt. A análise usa RAG (boas práticas) +
          LLM (OpenAI).
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
        <button
          type="button"
          className="btn primary"
          onClick={handleAnalyze}
          disabled={loading || !prompt.trim()}
        >
          {loading ? "Analisando…" : "Analisar"}
        </button>

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

        {result && !error && (
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
            <div className="flags">
              <span className={result.has_instructions ? "flag on" : "flag"}>
                {result.has_instructions ? "✓" : "—"} Instruções
              </span>
              <span className={result.has_examples ? "flag on" : "flag"}>
                {result.has_examples ? "✓" : "—"} Exemplos
              </span>
            </div>
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
        )}
      </section>
    </Layout>
  );
}
