# VEERA — Frontend

**Failure-Aware Visual Evidence Acquisition for Reliable Multimodal AI**

A polished React frontend for image-based visual inspection research. Upload an image to investigate potential visible defects, review structured evidence, and understand the reasoning behind each assessment.

> **Research prototype.** VEERA is an academic project exploring how vision-language models can perform visual inspection while remaining aware of their own limitations. Its assessments are experimental AI outputs and should not be treated as professional structural inspections or safety certifications.

---

## Quick Start

### Prerequisites

- **Node.js** ≥ 18 and **npm** ≥ 9

### Install & Run

```bash
# Install dependencies
npm install

# Copy environment config
cp .env.example .env

# Start development server (mock mode by default)
npm run dev
```

The app opens at **http://localhost:5173**.

### Production Build

```bash
npm run build
npm run preview   # preview the production bundle
```

---

## Configuration

All configuration is via environment variables in `.env`:

| Variable             | Default  | Description                                               |
|----------------------|----------|-----------------------------------------------------------|
| `VITE_API_BASE_URL`  | _(empty)_ | Base URL of the Python/FastAPI backend (e.g. `http://localhost:8000`) |
| `VITE_MOCK_MODE`     | `true`   | `true` = use demonstration data; `false` = call real backend |

### Mock Mode (default)

When `VITE_MOCK_MODE=true` or `VITE_API_BASE_URL` is empty, the app runs with local demonstration data. A **"Mock Mode"** badge is displayed in the navbar and all results are clearly labelled as demonstration output.

Three selectable scenarios are available:
1. **Defect detected** — simulates a potential crack finding
2. **No defect** — simulates a clear inspection result
3. **Inconclusive** — simulates an ambiguous/blurry image result

### Real Mode

Set `VITE_MOCK_MODE=false` and `VITE_API_BASE_URL=http://your-backend:8000` to connect to the actual Python/FastAPI pipeline. The frontend will send images to `POST /api/v1/inspect` and render real results.

**In real mode, if the backend is unavailable the app shows an honest error — it never silently substitutes mock data.**

---

## Project Structure

```
VEERA/
├── public/
│   └── favicon.svg              # VEERA favicon
├── src/
│   ├── components/
│   │   ├── Navbar.jsx           # Navigation bar with mock-mode badge
│   │   ├── ImageUpload.jsx      # Drag-and-drop / click upload with preview
│   │   ├── MockSelector.jsx     # Demo scenario picker (dev only)
│   │   ├── ProcessingView.jsx   # Progress stages during inspection
│   │   ├── InspectionResults.jsx # Structured results panel
│   │   ├── ErrorState.jsx       # Error display with retry
│   │   └── Footer.jsx           # Footer
│   ├── pages/
│   │   ├── InspectionPage.jsx   # Main inspection workspace
│   │   └── AboutPage.jsx        # Methodology / About page
│   ├── services/
│   │   └── inspectionApi.js     # HTTP service layer (mock + real)
│   ├── mocks/
│   │   └── inspectionMocks.js   # Three demonstration scenarios
│   ├── hooks/
│   │   └── useInspection.js     # Inspection workflow state management
│   ├── utils/
│   │   └── imageValidation.js   # File type/size validation, preview
│   ├── styles/                  # (index.css at root serves as design system)
│   ├── App.jsx                  # Root with routing
│   ├── main.jsx                 # Entry point
│   └── index.css                # Complete design system + component styles
├── .env.example                 # Environment config template
├── .env                         # Local config (gitignored)
├── index.html                   # HTML template with SEO meta
├── package.json
├── vite.config.js
└── README.md
```

---

## Proposed FastAPI Contract

The frontend is prepared to integrate with a Python/FastAPI backend.

### Endpoint

```
POST /api/v1/inspect
Content-Type: multipart/form-data
```

### Request

| Field    | Type   | Required | Description              |
|----------|--------|----------|--------------------------|
| `image`  | File   | Yes      | JPEG, PNG, or WebP image |

### Response (JSON)

```json
{
  "status": "completed",
  "assessment": "defect_detected | no_defect | inconclusive | error",
  "summary": "Human-readable summary of the assessment.",
  "findings": [
    {
      "category": "crack",
      "description": "Description of what was observed.",
      "evidence": "Supporting visual evidence statement.",
      "region": null,
      "region_image": null
    }
  ],
  "verification": {
    "performed": true,
    "initial_assessment": "What was found initially.",
    "reassessment": "What was found after closer examination.",
    "additional_evidence_acquired": true
  },
  "explanation": "Full explanation of the inspection process and result."
}
```

### Response Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `status` | string | **Yes** | `"completed"` or `"error"` |
| `assessment` | string | No | One of `defect_detected`, `no_defect`, `inconclusive`, `error` |
| `summary` | string | No | Falls back to "No summary provided." |
| `findings` | array | No | Falls back to empty array `[]` |
| `findings[].category` | string | No | e.g. `"crack"`, `"damage"`, `"uncertain"` |
| `findings[].description` | string | No | What the model observed |
| `findings[].evidence` | string | No | Supporting evidence statement |
| `findings[].region` | object | No | Bounding box (future) |
| `findings[].region_image` | string | No | URL/base64 of cropped region |
| `verification.performed` | boolean | No | Whether verification ran |
| `verification.initial_assessment` | string | No | First-pass finding |
| `verification.reassessment` | string | No | Second-pass finding |
| `verification.additional_evidence_acquired` | boolean | No | Whether a crop was examined |
| `explanation` | string | No | Full reasoning summary |

> **This is a proposed contract.** The final schema must be agreed upon with the Python backend developer. The frontend's `inspectionApi.js` service layer validates and normalizes the response, so schema changes only require updating that one module.

---

## Technology Stack

| Layer | Technology |
|---|---|
| UI Framework | React 19 |
| Build Tool | Vite 8 |
| Language | JavaScript (JSX) |
| Icons | Lucide React |
| Routing | React Router DOM v7 |
| Styling | Vanilla CSS (custom properties design system) |
| Backend (planned) | Python · FastAPI · Qwen2.5-VL-3B-Instruct |

---

## Backend Integration Notes

The Python/FastAPI backend is **not part of this repository**. It is expected to:

1. Accept `POST /api/v1/inspect` with `multipart/form-data`
2. Run the Qwen2.5-VL model inference pipeline
3. Return a structured JSON response matching the contract above
4. Handle CORS for the frontend origin

When the backend is ready:
1. Set `VITE_MOCK_MODE=false` in `.env`
2. Set `VITE_API_BASE_URL=http://your-backend-url:8000`
3. Restart the dev server

The frontend will automatically switch from mock to real API calls.

---

## License

Research prototype — not for production use.
