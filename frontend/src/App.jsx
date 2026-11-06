import { useEffect, useState } from "react";

const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(
  /\/$/,
  "",
);

const EXAMPLES = [
  {
    label: "ARIMA in R",
    text: "I am working with a dataset of monthly sales and I want to forecast the next 12 months using an ARIMA model in R.",
  },
  {
    label: "Pandas merge",
    text: "How do I merge two pandas dataframes on multiple columns and keep only the matching rows?",
  },
  {
    label: "React state",
    text: "My React component does not re-render when I update an object in useState. How should I update state immutably?",
  },
];

function TagMark() {
  return (
    <svg className="mark" viewBox="0 0 36 36" aria-hidden="true">
      <rect width="36" height="36" rx="8" fill="#1C1914" />
      <path
        d="M8.5 14.2h13.4l4.1 3.8-4.1 3.8H8.5v-7.6Z"
        stroke="#F6F0E6"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
      <circle cx="13.2" cy="18" r="1.15" fill="#E7C2A8" />
    </svg>
  );
}

async function requestTags(text) {
  let response;
  try {
    response = await fetch(`${API_URL}/api/predict`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
  } catch {
    throw new Error(
      "The tagging API did not respond. Check that it is running and that VITE_API_URL points at it.",
    );
  }

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (response.status === 403) {
    throw new Error(
      "This site is not on the API allow list. Add this page’s origin to ALLOWED_ORIGINS on the backend.",
    );
  }

  if (!response.ok) {
    const detail =
      payload && typeof payload.detail === "string" ? payload.detail : "";
    throw new Error(detail || "The API could not tag this question.");
  }

  return Array.isArray(payload?.tags) ? payload.tags : [];
}

export default function App() {
  const [ready, setReady] = useState(false);
  const [patient, setPatient] = useState(false);
  const [question, setQuestion] = useState("");
  const [tags, setTags] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    let retryTimer;
    const stop = new AbortController();

    async function ping() {
      const attempt = new AbortController();
      const timeout = setTimeout(() => attempt.abort(), 8000);
      const cancelAttempt = () => attempt.abort();
      stop.signal.addEventListener("abort", cancelAttempt);
      try {
        const response = await fetch(`${API_URL}/health`, { signal: attempt.signal });
        if (!cancelled && response.ok) {
          setReady(true);
          return;
        }
      } catch {
        // The service is still starting. Keep the loading screen up.
      } finally {
        clearTimeout(timeout);
        stop.signal.removeEventListener("abort", cancelAttempt);
      }
      if (!cancelled) retryTimer = setTimeout(ping, 3000);
    }

    ping();
    const patientTimer = setTimeout(() => {
      if (!cancelled) setPatient(true);
    }, 8000);

    return () => {
      cancelled = true;
      stop.abort();
      clearTimeout(retryTimer);
      clearTimeout(patientTimer);
    };
  }, []);

  async function onSubmit(event) {
    event.preventDefault();
    const text = question.trim();
    if (!text || loading) {
      setTags(null);
      setError("Enter a question before predicting tags.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      setTags(await requestTags(text));
    } catch (err) {
      setTags(null);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  if (!ready) {
    return (
      <div className="boot" role="status" aria-live="polite">
        <h1>Auto Tag Generator</h1>
        <p>Loading application</p>
        <div className="boot-line" aria-hidden="true">
          <span />
        </div>
        {patient && (
          <p className="boot-note">The model is starting. It can take few minutes.</p>
        )}
      </div>
    );
  }

  return (
    <div className="page">
      <main className="sheet">
        <header className="mast">
          <TagMark />
          <div>
            <h1>Auto Tag Generator</h1>
            <p className="lede">
              Enter a programming question. A CNN trained for multi-label
              classification suggests the Stack Overflow tags that fit, with a
              macro F1 of 0.83.
            </p>
          </div>
        </header>

        <form onSubmit={onSubmit}>
          <label htmlFor="question">Question</label>
          <textarea
            id="question"
            name="question"
            rows={8}
            maxLength={8000}
            value={question}
            placeholder="Describe the problem the way you would ask it on Stack Overflow."
            onChange={(event) => setQuestion(event.target.value)}
          />
          <p className="count" aria-live="polite">
            {question.length} / 8000
          </p>

          <div className="examples">
            <p id="example-label">Try a question</p>
            <div role="group" aria-labelledby="example-label">
              {EXAMPLES.map((example) => (
                <button
                  key={example.label}
                  type="button"
                  className="example"
                  onClick={() => {
                    setQuestion(example.text);
                    setError("");
                  }}
                >
                  {example.label}
                </button>
              ))}
            </div>
          </div>

          <button className="submit" type="submit" disabled={loading}>
            {loading ? "Predicting…" : "Predict tags"}
          </button>
        </form>

        <section className="result" aria-live="polite" aria-busy={loading}>
          {error ? <p className="error">{error}</p> : null}

          {!error && tags === null ? (
            <p className="quiet">Predicted tags will show up here.</p>
          ) : null}

          {!error && tags !== null && tags.length === 0 ? (
            <p className="quiet">No tag crossed the decision threshold for this question.</p>
          ) : null}

          {!error && tags && tags.length > 0 ? (
            <ul className="tags">
              {tags.map((tag) => (
                <li className="tag" key={tag.name}>
                  <span>{tag.name}</span>
                  <span className="score">{Math.round(tag.score * 100)}%</span>
                </li>
              ))}
            </ul>
          ) : null}
        </section>
      </main>
    </div>
  );
}
