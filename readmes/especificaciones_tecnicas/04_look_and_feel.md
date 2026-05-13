# 04 — Look and Feel Specifications

This document defines the visual identity, UI/UX principles, and design system of the NeurIPS 2026 Reproducibility Auditor.

## 1. Design Philosophy: "Nature Auditor Pro"

The application follows a **SaaS Premium** aesthetic, moving away from the default Streamlit "utility" look. The goal is to provide a professional, trustworthy interface for scientific auditing.

**Key Principles**:
- **High Contrast**: Dark text on a clean, off-white background.
- **Glassmorphism**: Subtle transparency and blurred backgrounds for containers.
- **Scientific Trust**: Use of professional color palettes (Greens for compliance, Neutrals for metadata).
- **Responsiveness**: Fluid layout that adapts to different screen sizes while maintaining a "wide" structure.

## 2. Color Palette (Design System)

| Category | Token | Hex Color | Usage |
|---|---|---|---|
| **Background** | `bg-main` | `#f8f9fa` | Page background. |
| **Containers** | `bg-card` | `rgba(255, 255, 255, 0.8)` | Glassmorphism card background. |
| **Accent (Success)** | `color-success` | `#00aa00` | "Strong Accept" and "Yes" verdicts. |
| **Accent (Warning)** | `color-warning` | `#ffcc00` | "Borderline" and "N/A" verdicts. |
| **Accent (Danger)** | `color-danger` | `#cc0000` | "Strong Reject" and "No" verdicts. |
| **Text (Primary)** | `text-main` | `#212529` | Headings and primary body text. |
| **Text (Secondary)** | `text-muted` | `#6c757d` | Descriptive text and metadata. |

## 3. Global CSS Theme

**Module**: `frontend/styles/custom_css.py`

The application injects a custom CSS block via `st.markdown(unsafe_allow_html=True)`. Key overrides include:

### 3.1 Layout & Cards
- **`.stApp`**: Sets the global background color.
- **`.audit-card`**: Custom class for the glassmorphism effect:
  ```css
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(200, 200, 200, 0.3);
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  ```

### 3.2 Typography
- **Font Family**: Prioritizes "Inter", "Helvetica Neue", Arial, sans-serif.
- **Headings**: Increased weight and specific letter-spacing for a modern feel.

### 3.3 Buttons
- **Start Audit Button**: Specially styled to be prominent:
  - `font-size: 1.2rem`
  - `padding: 0.75rem 2rem`
  - `background-color: #007bff`
  - `border-radius: 8px`

## 4. Component-Specific Design

### 4.1 Compliance Table
The HTML table in `audit_results.py` uses inline styles to ensure visibility across different Streamlit versions:
- **Verdict Badges**: Small, rounded containers with high-contrast text.
- **Evidence Snippets**: Monospace or slightly smaller font to distinguish from narrative text.

### 4.2 Phase Tracker
A custom progress visualization shown during the audit pipeline:
- **Active Phase**: Highlighted with a pulsing animation or a distinct border color.
- **Completed Phases**: Checkmark icon and green text.
- **Pending Phases**: Subtle gray text.

### 4.3 Gauge Chart (Plotly)
- **Bar Color**: Synchronized with the Quality Tier (see `06_glossary.md`).
- **Font**: "Helvetica" or "Arial" to match the rest of the UI.
- **Margin**: Optimized to prevent clipping in Streamlit's container.

## 5. Animations & Feedback
- **Transitions**: Smooth fade-in for result tabs.
- **Loading State**: A dedicated loading screen with a high z-index, shown during service initialization.
- **Status Callback**: Real-time status updates ("Auditando...", "Analizando SOTA...") displayed in the status container.
