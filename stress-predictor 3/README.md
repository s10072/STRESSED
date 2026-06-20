# 🧠 What's Your Stress Type?

An AI-powered stress profiling app — like MBTI but for your stress and lifestyle patterns.

Answer 5 short questions about your daily habits and get a personalised stress type (e.g. "The Silent Stacker", "The Burnt-out Achiever") with a description, strengths, risks, and tailored tips.

Built with Python, scikit-learn, Claude AI, and Streamlit.

## Live Demo

👉 [Open the app](https://your-app-link.streamlit.app) *(replace after deploying)*

## How it works

1. Answer 5 natural language questions about sleep, mood, work, and habits
2. A Random Forest ML model estimates your stress level from your answers
3. Claude AI analyses your responses and generates a personalised stress profile
4. You get your stress type, a score out of 10, strengths, risks, and 3 actionable tips

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here  # get one free at console.anthropic.com
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Connect your repo, set `app.py` as entry point
4. Add your API key: Settings → Secrets → `ANTHROPIC_API_KEY = "your_key"`
5. Deploy — you'll get a public link in ~2 minutes

## Tech stack

- `scikit-learn` — Random Forest stress classifier
- `anthropic` — Claude AI for natural language profile generation
- `streamlit` — frontend UI
- `numpy` — feature engineering
