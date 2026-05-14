# CRT Dashboard — Live Online Version

Interactive Career Review Touchpoint dashboard for **Gilang Catur** (PY2026).
Built with Streamlit + Plotly, styled in PwC orange/dark theme.

## 🚀 Deploy in 5 minutes (FREE — Streamlit Community Cloud)

### Step 1 — Create a GitHub repo
1. Go to https://github.com → click **New repository**
2. Name it e.g. `crt-dashboard-gilang`
3. Set to **Private** (recommended, since data is confidential)
4. Click **Create repository**

### Step 2 — Upload these 3 files to the repo
- `app.py`
- `requirements.txt`
- `Leader_Report_Extract.xlsx` (rename your source file to this exact name)

You can drag-and-drop them in GitHub's web UI ("Add file" → "Upload files").

### Step 3 — Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **New app** → select your repo → branch `main` → main file `app.py`
4. Click **Deploy** ✅

In ~2 minutes you'll get a public URL like:
`https://crt-dashboard-gilang.streamlit.app`

You can share this link with anyone (or keep it private — Streamlit Cloud lets you restrict by email).

---

## 🖥️ Run locally (optional)

```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open http://localhost:8501

---

## 📊 What's inside

1. **Coachee Profile** — Bio card (Name, ID, PY, Grade, LoS, Office, Coach, Leader)
2. **At-a-Glance KPIs** — Live updating counters
3. **Behaviour Assessment Deep Dive** — Bar chart + Radar chart + per-assessor heatmap
   - 🎛️ **Interactive sidebar filter**: All / By Project / By Client
4. **Project Engagement & Reviewer Profile** — Hours bar chart + grade donut + 5 insight bullets
5. **Qualitative Insights** — Strength themes (green) + Improvement themes (red) + narrative summaries
6. **Knowledge & Technical Skills Verdict** — Big banner: "In line with expectations"
7. **All Comments** — Tabbed view (Downward / Peer) with full feedback text

🔒 **Confidential** — for Career Coach use only.
