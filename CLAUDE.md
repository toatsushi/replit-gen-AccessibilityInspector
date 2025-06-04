# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
streamlit run app.py
```

### Dependencies
```bash
pip install -r requirements.txt
```

### Update WCAG Criteria
```bash
python src/update_wcag_versions.py
```

## Architecture Overview

This is a modular web accessibility testing platform that combines automated axe-core testing with AI-powered manual assessment for comprehensive WCAG 2.1 compliance evaluation.

### Core Component Flow
```
URL Input → AccessibilityChecker → {automated + content extraction} → AIEvaluator → ReportGenerator → Streamlit UI
```

### Key Components

**AccessibilityChecker** (`src/accessibility_checker.py`)
- Handles Selenium WebDriver automation with Chrome headless
- Integrates axe-core JavaScript library for automated accessibility scanning
- Extracts page content (headings, images, forms, links) using BeautifulSoup
- Primary entry point for all web scraping and automated testing

**AIEvaluator** (`src/ai_evaluator.py`)
- Provides AI-powered assessment using OpenAI (GPT-4o) or Anthropic (Claude) APIs
- Evaluates WCAG criteria that require human judgment
- Generates structured assessments with confidence scores and recommendations
- Processes manual criteria that can't be automated

**ReportGenerator** (`src/report_generator.py`)
- Central aggregation point for automated and manual test results
- Calculates compliance scores and cross-references findings
- Exports to multiple formats: JSON, HTML, CSV
- Implements priority-based recommendation system

**WCAG Criteria** (`src/wcag_criteria.py`)
- Contains 30+ WCAG 2.1 success criteria definitions
- Distinguishes between manual vs automated evaluation criteria
- Provides evaluation guidelines and priority mappings for each criterion

### Environment Configuration

Required environment variables for AI features:
- `OPENAI_API_KEY` - For OpenAI GPT-4o integration
- `ANTHROPIC_API_KEY` - For Anthropic Claude integration

### Feature Flags

The AI assessment feature is controlled by `AI_ASSESSMENT_FEATURE_FLAG` in `app.py` (currently disabled).

### Session State Management

Streamlit session state preserves analysis results across UI interactions:
- `st.session_state.results` - Raw analysis data
- `st.session_state.report` - Generated report
- `st.session_state.report_generator` - Report generator instance

### Report Export Flow

1. Analysis results stored in session state
2. ReportGenerator processes combined automated/manual results
3. Export functions generate JSON/HTML downloads via Streamlit download buttons
4. HTML reports use embedded CSS for standalone viewing