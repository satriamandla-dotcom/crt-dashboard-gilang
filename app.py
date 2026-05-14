"""
CRT Dashboard — Career Review Touchpoint
Live interactive dashboard for coachee performance review
PwC-styled | Built with Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

# =========================================================
# PAGE CONFIG & PWC STYLE
# =========================================================
st.set_page_config(
    page_title="CRT Dashboard — Gilang Catur",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# PwC color palette
PWC_ORANGE = "#D04A02"
PWC_DARK_ORANGE = "#A34000"
PWC_YELLOW = "#FFB600"
PWC_RED = "#E0301E"
PWC_GREEN = "#22A06B"
PWC_DARK = "#2D2D2D"
PWC_GREY = "#7D7D7D"
PWC_LIGHT = "#F2F2F2"
PWC_WHITE = "#FFFFFF"

# Custom CSS — PwC look & feel
st.markdown(f"""
<style>
    .stApp {{
        background-color: {PWC_WHITE};
    }}
    .main-header {{
        background: linear-gradient(90deg, {PWC_ORANGE} 0%, {PWC_DARK_ORANGE} 100%);
        padding: 24px 32px;
        border-radius: 8px;
        margin-bottom: 8px;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .main-header h1 {{
        color: white !important;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }}
    .main-header p {{
        color: white !important;
        margin: 4px 0 0 0;
        font-size: 14px;
        opacity: 0.95;
    }}
    .section-header {{
        background-color: {PWC_ORANGE};
        color: white !important;
        padding: 10px 18px;
        border-radius: 6px;
        font-size: 16px;
        font-weight: 600;
        margin: 24px 0 12px 0;
    }}
    .section-header-dark {{
        background-color: {PWC_DARK};
        color: white !important;
        padding: 10px 18px;
        border-radius: 6px;
        font-size: 16px;
        font-weight: 600;
        margin: 24px 0 12px 0;
    }}
    .bio-card {{
        background: {PWC_LIGHT};
        padding: 14px 18px;
        border-radius: 6px;
        border-left: 4px solid {PWC_ORANGE};
        margin-bottom: 8px;
    }}
    .bio-label {{
        font-size: 11px;
        color: {PWC_GREY};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }}
    .bio-value {{
        font-size: 15px;
        color: {PWC_DARK};
        font-weight: 600;
        margin: 2px 0 0 0;
    }}
    .kpi-card {{
        background: white;
        padding: 16px;
        border-radius: 8px;
        border-top: 4px solid {PWC_ORANGE};
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        text-align: center;
    }}
    .kpi-label {{
        font-size: 12px;
        color: {PWC_GREY};
        text-transform: uppercase;
        font-weight: 600;
        margin: 0;
    }}
    .kpi-value {{
        font-size: 30px;
        color: {PWC_ORANGE};
        font-weight: 700;
        margin: 6px 0 0 0;
        line-height: 1;
    }}
    .verdict-banner {{
        background: linear-gradient(90deg, {PWC_GREEN} 0%, #1B7A52 100%);
        color: white;
        padding: 24px;
        border-radius: 8px;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .insight-card {{
        background: white;
        border: 1px solid #E5E5E5;
        border-left: 4px solid {PWC_ORANGE};
        padding: 12px 16px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 13px;
        color: {PWC_DARK};
    }}
    .strength-card {{
        background: white;
        border-left: 4px solid {PWC_GREEN};
        padding: 14px 18px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 13px;
        line-height: 1.6;
    }}
    .improve-card {{
        background: white;
        border-left: 4px solid {PWC_RED};
        padding: 14px 18px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 13px;
        line-height: 1.6;
    }}
    .comment-down {{
        background: #FFF4ED;
        border-left: 4px solid {PWC_ORANGE};
        padding: 12px 16px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 13px;
    }}
    .comment-peer {{
        background: {PWC_LIGHT};
        border-left: 4px solid {PWC_DARK};
        padding: 12px 16px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 13px;
    }}
    .comment-meta {{
        font-size: 11px;
        color: {PWC_GREY};
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 6px;
    }}
    [data-testid="stSidebar"] {{
        background-color: {PWC_DARK};
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label {{
        color: {PWC_YELLOW} !important;
        font-weight: 600;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {PWC_LIGHT};
        border-radius: 6px 6px 0 0;
        padding: 10px 18px;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {PWC_ORANGE} !important;
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA LOADING & PREPARATION
# =========================================================
@st.cache_data
def load_data(path="Leader_Report_Extract.xlsx"):
    df = pd.read_excel(path, sheet_name="LeaderReport")
    me = df[df["Employee Name"].str.contains("Gilang Catur", case=False, na=False)].copy()

    rating_cols = [
        "Trusted Leadership: Inspire", "Trusted Leadership: Empower", "Trusted Leadership: Evolve",
        "Distinctive Outcomes: Champion", "Distinctive Outcomes: Build", "Distinctive Outcomes: Deliver",
    ]
    rating_map = {
        "Exemplified and motivated others to demonstrate these behaviours": 5,
        "Almost always demonstrated these behaviours": 4,
        "Often demonstrated these behaviours": 3,
        "Sometimes demonstrated these behaviours": 2,
        "Sometimes demonstrated": 2,
        "Acted contradictory to these behaviours": 1,
        "Acted contradictory": 1,
    }

    for c in rating_cols:
        me[c] = me[c].astype(str).str.strip().replace({"nan": np.nan})
        me[c + "_num"] = me[c].map(rating_map)

    def first_part(x):
        if pd.isna(x):
            return ""
        return str(x).split("|")[0].strip()

    def parse_hours(x):
        if pd.isna(x):
            return np.nan
        parts = re.split(r"[|,;]", str(x))
        nums = []
        for p in parts:
            try:
                nums.append(float(p.strip()))
            except Exception:
                pass
        return max(nums) if nums else np.nan

    me["Project_clean"] = me["Project Name"].apply(first_part)
    me["Client_clean"] = me["Client Name"].apply(first_part)
    me["Hours_num"] = me["Project Hours YTD at time of request"].apply(parse_hours)

    return me, rating_cols


me, RATING_COLS = load_data()
down = me[me["Directionality"] == "Downward"].copy()
peer = me[me["Directionality"] == "Peer"].copy()

PARAM_SHORT = {
    "Trusted Leadership: Inspire": "TL: Inspire",
    "Trusted Leadership: Empower": "TL: Empower",
    "Trusted Leadership: Evolve": "TL: Evolve",
    "Distinctive Outcomes: Champion": "DO: Champion",
    "Distinctive Outcomes: Build": "DO: Build",
    "Distinctive Outcomes: Deliver": "DO: Deliver",
}

# =========================================================
# SIDEBAR — FILTERS
# =========================================================
with st.sidebar:
    st.markdown("### 🎛️ DASHBOARD FILTERS")
    st.markdown("---")

    filter_mode = st.radio(
        "Filter by:",
        ["All Projects", "By Project", "By Client"],
        index=0,
    )

    selected_project = None
    selected_client = None

    if filter_mode == "By Project":
        projects = sorted([p for p in down["Project_clean"].dropna().unique() if p])
        selected_project = st.selectbox("Select Project:", projects)
    elif filter_mode == "By Client":
        clients = sorted([c for c in down["Client_clean"].dropna().unique() if c])
        selected_client = st.selectbox("Select Client:", clients)

    st.markdown("---")
    st.markdown("### ℹ️ ABOUT")
    st.caption(
        "Career Review Touchpoint (CRT) Dashboard — interactive review of coachee performance "
        "based on downward and peer feedback assessments.\\n\\n"
        "Use the filters above to drill down by project or client."
    )
    st.markdown("---")
    st.caption("🔒 Confidential — for Career Coach use only")


# Apply filter to downward data
def apply_filter(df):
    if selected_project:
        return df[df["Project_clean"] == selected_project]
    if selected_client:
        return df[df["Client_clean"] == selected_client]
    return df


down_f = apply_filter(down)

# =========================================================
# HEADER
# =========================================================
st.markdown(f"""
<div class="main-header">
    <h1>🎯 Career Review Touchpoint (CRT) Dashboard</h1>
    <p>Performance Year 2026 &nbsp;•&nbsp; Coachee: <b>Gilang Catur</b> &nbsp;•&nbsp; Global Grade: <b>Associate 1</b></p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 1. COACHEE PROFILE
# =========================================================
st.markdown('<div class="section-header">1 · COACHEE PROFILE</div>', unsafe_allow_html=True)

bio_pairs = [
    ("Employee Name", "Gilang Catur"),
    ("Employee ID", "101548448"),
    ("Performance Year", "2026"),
    ("Global Grade", "Associate 1"),
    ("Line of Service", str(me.iloc[0].get("Global Line of Service", "—"))),
    ("Office Location", str(me.iloc[0].get("Office Location Common Name", "—"))),
    ("Career Coach", str(me.iloc[0].get("Career Coach", "—"))),
    ("Relationship Leader", str(me.iloc[0].get("Relationship Leader", "—"))),
]

cols = st.columns(4)
for i, (label, value) in enumerate(bio_pairs):
    with cols[i % 4]:
        st.markdown(
            f'<div class="bio-card"><p class="bio-label">{label}</p>'
            f'<p class="bio-value">{value}</p></div>',
            unsafe_allow_html=True,
        )

# =========================================================
# AT-A-GLANCE KPIs
# =========================================================
st.markdown('<div class="section-header-dark">AT A GLANCE</div>', unsafe_allow_html=True)

avg_score = down_f[[c + "_num" for c in RATING_COLS]].stack().mean()
avg_score_str = f"{avg_score:.2f}" if pd.notna(avg_score) else "—"

kpis = [
    ("Total Feedback", len(me)),
    ("Downward Feedback", len(down)),
    ("Peer Feedback", len(peer)),
    ("Unique Projects", down["Project_clean"].nunique()),
    ("Avg. Score (filtered)", f"{avg_score_str} / 5"),
]
cols = st.columns(5)
for i, (lbl, val) in enumerate(kpis):
    with cols[i]:
        st.markdown(
            f'<div class="kpi-card"><p class="kpi-label">{lbl}</p>'
            f'<p class="kpi-value">{val}</p></div>',
            unsafe_allow_html=True,
        )

# =========================================================
# 5. KNOWLEDGE & TECHNICAL SKILLS VERDICT (top placement)
# =========================================================
st.markdown(
    '<div class="section-header">5 · KNOWLEDGE & TECHNICAL SKILLS VERDICT</div>',
    unsafe_allow_html=True,
)

tech_vals = me["Assessing Knowledge and Technical Skills"].dropna().astype(str).str.strip()
tech_counts = tech_vals.value_counts().to_dict()
verdict = max(tech_counts, key=tech_counts.get) if tech_counts else "Not Assessed"
n_assessed = sum(tech_counts.values())

st.markdown(
    f'<div class="verdict-banner">✅ {verdict}<br>'
    f'<span style="font-size:14px;font-weight:400;opacity:0.95">'
    f'Based on {n_assessed} of {len(down)} downward reviewers who rated this dimension</span></div>',
    unsafe_allow_html=True,
)

with st.expander("📖 View Detailed Verdict Narrative"):
    st.markdown(f"""
    Among the **{len(down)} downward feedback** received, **{n_assessed} reviewers** provided an explicit
    rating on *Assessing Knowledge and Technical Skills*. **All {n_assessed} reviewers** — Iskandar Prakoso
    (Senior Manager), Muhammad Sani (Manager), and Monica Adriana (Manager) — rated Gilang as
    **"{verdict}"**.

    **Interpretation:** This indicates a **consistent and solid technical performance** at the Associate 1 grade level.
    No reviewer rated him below expectation, and his managers across multiple engagements
    (Jasa Marga ITE stream, EALM Telkomsel) corroborate the same view.

    **Recommendation:** Maintain steady delivery while stretching toward *"Exceeds Expectations"* through:
    - Deeper technical specialization (business process analysis frameworks)
    - PPT / storyline crafting skills
    - Leading complex workstreams end-to-end
    """)

# =========================================================
# 2. BEHAVIOUR ASSESSMENT DEEP DIVE
# =========================================================
st.markdown(
    '<div class="section-header">2 · BEHAVIOUR ASSESSMENT DEEP DIVE (DOWNWARD FEEDBACK)</div>',
    unsafe_allow_html=True,
)

filter_label = "All Downward Feedback"
if selected_project:
    filter_label = f"Project: {selected_project}"
elif selected_client:
    filter_label = f"Client: {selected_client}"

st.caption(f"📌 Currently showing: **{filter_label}** · {len(down_f)} feedback record(s)")

if len(down_f) == 0:
    st.warning("No feedback records match the current filter.")
else:
    avg_per_param = {
        PARAM_SHORT[c]: down_f[c + "_num"].mean() for c in RATING_COLS
    }
    avg_df = pd.DataFrame(
        {"Parameter": list(avg_per_param.keys()), "Score": list(avg_per_param.values())}
    ).fillna(0)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        # Horizontal bar chart
        fig_bar = px.bar(
            avg_df.sort_values("Score"),
            x="Score",
            y="Parameter",
            orientation="h",
            text=avg_df.sort_values("Score")["Score"].round(2),
            color_discrete_sequence=[PWC_ORANGE],
        )
        fig_bar.update_traces(
            textposition="outside",
            marker_line_color=PWC_DARK_ORANGE,
            marker_line_width=1.5,
            textfont=dict(size=12, color=PWC_DARK, family="Calibri"),
        )
        fig_bar.update_layout(
            title=dict(
                text="<b>Average Behaviour Score by Parameter</b><br>"
                     "<span style='font-size:11px;color:#7D7D7D'>"
                     "1 = Contradictory · 5 = Exemplified</span>",
                font=dict(size=14, color=PWC_DARK),
            ),
            xaxis=dict(range=[0, 5.4], title="Score", showgrid=True, gridcolor="#EEEEEE"),
            yaxis=dict(title=""),
            plot_bgcolor=PWC_LIGHT,
            paper_bgcolor=PWC_WHITE,
            height=380,
            margin=dict(l=10, r=20, t=70, b=40),
            font=dict(family="Calibri", color=PWC_DARK),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Radar chart
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=list(avg_per_param.values()) + [list(avg_per_param.values())[0]],
            theta=list(avg_per_param.keys()) + [list(avg_per_param.keys())[0]],
            fill="toself",
            fillcolor=f"rgba(208, 74, 2, 0.35)",
            line=dict(color=PWC_DARK_ORANGE, width=2.5),
            name="Score",
        ))
        fig_radar.update_layout(
            title=dict(text="<b>Competency Radar</b>", font=dict(size=14, color=PWC_DARK)),
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=11, color=PWC_DARK)),
            ),
            showlegend=False,
            height=380,
            margin=dict(l=40, r=40, t=70, b=40),
            paper_bgcolor=PWC_WHITE,
            font=dict(family="Calibri", color=PWC_DARK),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Heatmap detail table
    st.markdown(
        '<div class="section-header-dark">DETAIL · PER-ASSESSOR HEATMAP</div>',
        unsafe_allow_html=True,
    )

    heat_df = down_f[
        ["Feedback Giver Name", "Feedback Giver Global Grade", "Project_clean", "Client_clean", "Hours_num"]
        + [c + "_num" for c in RATING_COLS]
    ].copy()
    heat_df.columns = ["Reviewer", "Grade", "Project", "Client", "Hours"] + list(PARAM_SHORT.values())

    score_color_map = {5: "#22A06B", 4: "#7DCC9D", 3: "#FFB600", 2: "#F08C5A", 1: "#E0301E"}

    def color_score(val):
        if pd.isna(val):
            return "background-color: #EEEEEE; color: #7D7D7D; text-align:center"
        v = int(val)
        bg = score_color_map.get(v, "#EEEEEE")
        fc = "white" if v in [5, 2, 1] else PWC_DARK
        return f"background-color: {bg}; color: {fc}; text-align:center; font-weight:600"

    styled = (
        heat_df.style
        .format({"Hours": "{:,.0f}"}, na_rep="—")
        .map(color_score, subset=list(PARAM_SHORT.values()))
        .set_properties(**{"font-family": "Calibri", "font-size": "12px"})
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # Legend
    legend_html = '<div style="display:flex;gap:8px;margin:8px 0;flex-wrap:wrap">'
    for score, desc in [
        (5, "Exemplified & motivated others"),
        (4, "Almost always demonstrated"),
        (3, "Often demonstrated"),
        (2, "Sometimes demonstrated"),
        (1, "Acted contradictory"),
    ]:
        bg = score_color_map[score]
        fc = "white" if score in [5, 2, 1] else PWC_DARK
        legend_html += (
            f'<div style="background:{bg};color:{fc};padding:6px 12px;'
            f'border-radius:4px;font-size:11px;font-weight:600">'
            f'{score} · {desc}</div>'
        )
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)

# =========================================================
# 3. PROJECT ENGAGEMENT & REVIEWER PROFILE
# =========================================================
st.markdown(
    '<div class="section-header">3 · PROJECT ENGAGEMENT & REVIEWER PROFILE INSIGHTS</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1.3, 1])

with col1:
    proj_hours = (
        down.groupby("Project_clean")["Hours_num"].max().reset_index()
        .query("Project_clean != ''")
        .sort_values("Hours_num", ascending=True)
    )
    fig_h = px.bar(
        proj_hours,
        x="Hours_num",
        y="Project_clean",
        orientation="h",
        text=proj_hours["Hours_num"].round(0).astype(int).map("{:,}".format),
        color_discrete_sequence=[PWC_DARK_ORANGE],
    )
    fig_h.update_traces(
        textposition="outside",
        marker_line_color=PWC_DARK,
        marker_line_width=1,
        textfont=dict(size=11, color=PWC_DARK),
    )
    fig_h.update_layout(
        title=dict(text="<b>Project Hours YTD by Engagement</b>", font=dict(size=14, color=PWC_DARK)),
        xaxis=dict(title="Hours", showgrid=True, gridcolor="#EEEEEE"),
        yaxis=dict(title=""),
        plot_bgcolor=PWC_LIGHT,
        paper_bgcolor=PWC_WHITE,
        height=400,
        margin=dict(l=10, r=60, t=60, b=40),
        font=dict(family="Calibri", color=PWC_DARK),
    )
    st.plotly_chart(fig_h, use_container_width=True)

with col2:
    grade_counts = down["Feedback Giver Global Grade"].value_counts().reset_index()
    grade_counts.columns = ["Grade", "Count"]
    fig_g = px.pie(
        grade_counts,
        values="Count",
        names="Grade",
        hole=0.55,
        color_discrete_sequence=[PWC_ORANGE, PWC_DARK_ORANGE, PWC_YELLOW, PWC_RED, PWC_GREY, PWC_DARK],
    )
    fig_g.update_traces(
        textinfo="label+value",
        textfont=dict(size=11, color=PWC_DARK, family="Calibri"),
        marker=dict(line=dict(color="white", width=2)),
    )
    fig_g.update_layout(
        title=dict(text="<b>Downward Feedback Givers by Grade</b>", font=dict(size=14, color=PWC_DARK)),
        height=400,
        showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=10)),
        paper_bgcolor=PWC_WHITE,
        margin=dict(l=10, r=10, t=60, b=40),
        font=dict(family="Calibri", color=PWC_DARK),
    )
    st.plotly_chart(fig_g, use_container_width=True)

# Insights bullets
total_hours = proj_hours["Hours_num"].sum()
top_proj = proj_hours.iloc[-1]
n_director = int(grade_counts.loc[grade_counts["Grade"] == "Director", "Count"].sum())
n_sm = int(grade_counts.loc[grade_counts["Grade"] == "Senior Manager", "Count"].sum())
n_mgr = int(grade_counts.loc[grade_counts["Grade"] == "Manager", "Count"].sum())
long_eng = (proj_hours["Hours_num"] >= 500).sum()
short_eng = (proj_hours["Hours_num"] <= 50).sum()

insights = [
    f"📊 <b>Total downward engagement coverage:</b> ~{int(total_hours):,} hours across {len(proj_hours)} unique project(s).",
    f"🏆 <b>Largest engagement:</b> '{top_proj['Project_clean']}' with {int(top_proj['Hours_num']):,} hours — indicates deep, long-running involvement.",
    f"⏱️ <b>Engagement mix:</b> {long_eng} long-duration project(s) (≥500 hrs) and {short_eng} short-touchpoint project(s) (≤50 hrs) — both <i>depth</i> and <i>breadth</i> exposure.",
    f"👥 <b>Reviewer seniority:</b> {n_director} Director · {n_sm} Senior Manager · {n_mgr} Manager — feedback comes from a robust, senior reviewer pool, lending high credibility.",
    "📈 <b>Diverse client base</b> across Assurance & Advisory (Danantara, Jasa Marga, Telkomsel) supports breadth-of-experience narrative for promotion readiness.",
]
for ins in insights:
    st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)

# =========================================================
# 4. QUALITATIVE INSIGHTS — STRENGTHS & IMPROVEMENTS
# =========================================================
st.markdown(
    '<div class="section-header">4 · QUALITATIVE INSIGHTS — STRENGTHS & AREAS TO IMPROVE</div>',
    unsafe_allow_html=True,
)

all_text = " ".join(
    [str(c) for c in me["Additional Comments"].dropna() if str(c).strip() and str(c) != "nan"]
).lower()

strength_themes = {
    "Commitment & Ownership": ["commit", "ownership", "responsib", "accountab", "dedicat", "reliab", "disciplin"],
    "Communication": ["communicat", "present", "articulat", "clearly", "voice", "engage"],
    "Collaboration & Teamwork": ["collabor", "team", "support", "help", "camaraderie", "inclusive"],
    "Leadership": ["leader", "lead", "delegate", "manage"],
    "Quality of Work": ["high-quality", "high quality", "quality", "meticulous", "thorough", "accurate"],
    "Proactiveness & Initiative": ["proactive", "initiative", "willing", "curious", "open to learn", "passionate", "step in"],
    "Problem-Solving": ["problem-solv", "problem solv", "critical thinking", "solv", "identify issues"],
    "Time Management & Deadlines": ["deadline", "on time", "timely", "tight"],
    "Professionalism": ["professional", "positive", "enthusi", "attitude"],
}
improvement_themes = {
    "Communication & Writing": ["communication", "writing", "writ"],
    "PPT / Presentation Skills": ["ppt", "presentation", "slide"],
    "Strategic Planning": ["strategic"],
}

def count_theme(text, kws):
    return sum(text.count(kw) for kw in kws)

strengths = {k: count_theme(all_text, kws) for k, kws in strength_themes.items()}
improvements = {k: count_theme(all_text, kws) for k, kws in improvement_themes.items()}

col1, col2 = st.columns([1.3, 1])

with col1:
    s_df = pd.DataFrame(
        {"Theme": list(strengths.keys()), "Mentions": list(strengths.values())}
    ).sort_values("Mentions", ascending=True)
    fig_s = px.bar(
        s_df, x="Mentions", y="Theme", orientation="h",
        text="Mentions", color_discrete_sequence=[PWC_GREEN],
    )
    fig_s.update_traces(
        textposition="outside",
        marker_line_color="#1B7A52", marker_line_width=1,
        textfont=dict(size=11, color=PWC_DARK, family="Calibri"),
    )
    fig_s.update_layout(
        title=dict(text="<b>Common Strengths (Theme Frequency)</b>", font=dict(size=14, color=PWC_DARK)),
        xaxis=dict(title="Mentions", showgrid=True, gridcolor="#EEEEEE"),
        yaxis=dict(title=""),
        plot_bgcolor=PWC_LIGHT, paper_bgcolor=PWC_WHITE,
        height=420, margin=dict(l=10, r=40, t=60, b=40),
        font=dict(family="Calibri", color=PWC_DARK),
    )
    st.plotly_chart(fig_s, use_container_width=True)

with col2:
    i_df = pd.DataFrame(
        {"Theme": list(improvements.keys()), "Mentions": list(improvements.values())}
    ).sort_values("Mentions", ascending=True)
    fig_i = px.bar(
        i_df, x="Mentions", y="Theme", orientation="h",
        text="Mentions", color_discrete_sequence=[PWC_RED],
    )
    fig_i.update_traces(
        textposition="outside",
        marker_line_color="#A02216", marker_line_width=1,
        textfont=dict(size=11, color=PWC_DARK, family="Calibri"),
    )
    fig_i.update_layout(
        title=dict(text="<b>Areas to Improve (Theme Frequency)</b>", font=dict(size=14, color=PWC_DARK)),
        xaxis=dict(title="Mentions", showgrid=True, gridcolor="#EEEEEE"),
        yaxis=dict(title=""),
        plot_bgcolor=PWC_LIGHT, paper_bgcolor=PWC_WHITE,
        height=420, margin=dict(l=10, r=40, t=60, b=40),
        font=dict(family="Calibri", color=PWC_DARK),
    )
    st.plotly_chart(fig_i, use_container_width=True)

# Narrative summaries
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="strength-card">
    <b style="color:#22A06B;font-size:14px">✅ STRENGTHS SUMMARY</b><br><br>
    Across all <b>14 written feedback responses</b>, Gilang is most consistently praised for:<br><br>
    <b>1. Collaboration & Teamwork</b> — supportive, inclusive, easy to work with.<br>
    <b>2. Commitment, Ownership & Accountability</b> — reliable, disciplined, delivers on tight deadlines.<br>
    <b>3. Leadership Presence</b> — even as a peer, seen as a 'role model' and effective Team Lead (PwC Ramadhan content team).<br>
    <b>4. Quality of Work</b> — meticulous, thorough, high-quality deliverables.<br>
    <b>5. Communication & Confidence</b> — willing to present to clients, voices ideas in large forums.<br>
    <b>6. Proactiveness</b> — curious, open to learning, frequently steps in to help others.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="improve-card">
    <b style="color:#E0301E;font-size:14px">🎯 AREAS TO IMPROVE</b><br><br>
    Development feedback is limited but consistent:<br><br>
    <b>1. Communication & Writing skills</b> — improving written communication
    (per Manager Monica Adriana).<br><br>
    <b>2. Presentation / PPT-making skills</b> — to elevate client-facing deliverables.<br><br>
    <b>3. Strategic Planning</b> — develop ability to lead complex projects end-to-end
    (per peer Kelvin Tioputra).<br><br>
    <i>Overall, feedback is overwhelmingly positive with growth pointers focused on
    senior-level capability building.</i>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# ALL COMMENTS (TABS)
# =========================================================
st.markdown('<div class="section-header-dark">📝 ALL FEEDBACK COMMENTS</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs([f"⬇️ Downward ({len(down)})", f"↔️ Peer ({len(peer)})"])

def render_comments(df_subset, css_class):
    has_any = False
    for _, r in df_subset.iterrows():
        c = r["Additional Comments"]
        if pd.notna(c) and str(c).strip() and str(c) != "nan":
            has_any = True
            project = r["Project_clean"] or "—"
            st.markdown(
                f'<div class="{css_class}">'
                f'<div class="comment-meta">{r["Feedback Giver Name"]} '
                f'· {r["Feedback Giver Global Grade"]} · Project: {project}</div>'
                f'{str(c).strip()}</div>',
                unsafe_allow_html=True,
            )
    if not has_any:
        st.info("No written comments available in this category.")

with tab1:
    render_comments(down, "comment-down")

with tab2:
    render_comments(peer, "comment-peer")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    f'<div style="text-align:center;color:{PWC_GREY};font-size:11px;padding:12px">'
    f"CRT Dashboard prepared for <b>Gilang Catur</b> · Performance Year 2026 · "
    f"Source: Leader Report Extract · 🔒 Confidential — for Career Coach use only"
    f"</div>",
    unsafe_allow_html=True,
)
