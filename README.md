# CRT Dashboard — Live Online Version (FINAL)

Interactive Career Review Touchpoint dashboard for **Gilang Catur** (PY2026).
Built with Streamlit + Plotly · PwC orange/dark theme.

## ✨ What's NEW in this final version

1. ✅ **Corrected dataset** — assessor feedback and Gilang's self-description are now properly separated. No more mismatch!
2. 🎤 **CRT Meeting Live Notes module** — type assessor comments live during the meeting
3. 🔍 **Analyze button** — instantly extracts strength + improvement themes from your typed notes
4. 📊 **Auto-generated charts** — bar charts of themes + sentiment gauge
5. 🤖 **AI-style summary** — automatic top-3 themes + coach recommendation
6. 💾 **Download button** — exports full meeting record as Markdown
7. 👁️ **Sidebar toggles** — show/hide empty reviewers, show/hide self-descriptions

## 🚀 Deploy in 5 minutes (FREE)

### Step 1 — Create a private GitHub repo
1. Go to https://github.com → **New repository** → set to **Private**
2. Name e.g. `crt-dashboard-gilang`

### Step 2 — Upload these 3 files
- `app.py`
- `crt_data.csv` (the cleaned dataset)
- `requirements.txt`

### Step 3 — Deploy on Streamlit Cloud
1. https://share.streamlit.io → sign in with GitHub
2. **New app** → select your repo → branch `main` → main file = `app.py`
3. **Deploy** ✅ → get a public URL like `https://your-app.streamlit.app`

## 🖥️ Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Sections in the dashboard

1. **Coachee Profile** — bio cards
2. **At-a-Glance** — 5 live KPIs
3. **Knowledge & Technical Skills Verdict** — green banner
4. **Behaviour Assessment Deep Dive** — bar + radar + heatmap (filterable)
5. **Project Engagement & Reviewer Profile** — hours bar + grade donut + insights
6. **Strengths & Improvements** — themes from written feedback
7. **All Comments** — tabbed (Downward / Peer)
8. **🎤 CRT Meeting Live Notes** — interactive note-taking + AI analysis 🆕

🔒 **Confidential** — for Career Coach use only.
