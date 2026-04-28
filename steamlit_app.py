import streamlit as st
import pandas as pd
import requests
import time
import json

# --- BRAND CONFIGURATION ---
COLORS = {
    "darkBlue": "#0F1C2C",
    "lightTaupe": "#F7FAF2",
    "darkGreen": "#1A5745",
    "primaryGreen": "#3BE0AD",
    "textGreen": "#19A078",
    "accentYellow": "#E8FC83",
    "accentBlue": "#50EAF2",
    "darkGray": "#A8A8A8",
    "lightGray": "#EBEAE8",
    "white": "#FFFFFF"
}

st.set_page_config(
    page_title="Vouch | HLS Blueprint",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ADVANCED CUSTOM CSS FOR 1:1 VISUAL PORT ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');

    html, body, [class*="css"]  {{
        font-family: 'Inter', sans-serif;
        scroll-behavior: smooth;
    }}

    .stApp {{
        background-color: {COLORS['lightTaupe']};
        color: {COLORS['darkBlue']};
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['white']};
        border-right: 1px solid {COLORS['lightGray']};
    }}

    /* Editorial Typography */
    .hero-badge {{
        background-color: {COLORS['accentYellow']};
        color: {COLORS['darkGreen']};
        padding: 6px 12px;
        border-radius: 2px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.2em;
        display: inline-block;
        margin-bottom: 40px;
    }}

    .hero-title {{
        font-size: 72px;
        font-weight: 800;
        line-height: 0.9;
        letter-spacing: -0.04em;
        color: {COLORS['darkBlue']};
        margin-bottom: 48px;
    }}

    .hero-subtitle {{
        font-size: 24px;
        font-weight: 500;
        color: {COLORS['darkBlue']};
        margin-bottom: 64px;
        line-height: 1.2;
    }}

    /* 1:1 Metric Card Styling */
    .metric-card-container {{
        display: flex;
        gap: 32px;
        margin-bottom: 80px;
        flex-wrap: wrap;
    }}

    .metric-card {{
        flex: 1;
        min-width: 280px;
        background-color: {COLORS['white']};
        padding: 40px;
        border-radius: 16px;
        border: 1px solid {COLORS['lightGray']};
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .metric-icon {{
        color: {COLORS['darkBlue']};
        margin-bottom: 40px;
    }}

    .metric-value {{
        font-size: 60px;
        font-weight: 800;
        color: {COLORS['darkBlue']};
        margin-bottom: 16px;
        line-height: 1;
    }}

    .metric-label {{
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.15em;
        line-height: 1.3;
        color: {COLORS['darkBlue']};
        text-transform: uppercase;
    }}

    /* Sidebar Navigation Links */
    .nav-link {{
        display: block;
        padding: 12px 8px;
        color: {COLORS['darkGray']};
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s;
        border-radius: 8px;
    }}
    .nav-link:hover {{
        background-color: {COLORS['lightGray']};
        color: {COLORS['darkBlue']};
    }}

    /* Custom Button */
    .vouch-button {{
        background-color: {COLORS['primaryGreen']};
        color: {COLORS['darkBlue']};
        padding: 16px;
        border-radius: 4px;
        font-weight: 700;
        text-align: center;
        text-decoration: none;
        display: block;
        margin-top: 32px;
        font-size: 14px;
        transition: transform 0.2s;
    }}
    .vouch-button:hover {{
        transform: scale(1.02);
    }}

    .ai-card {{
        background-color: {COLORS['white']};
        padding: 48px;
        border-radius: 48px;
        border: 1px solid {COLORS['lightGray']};
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-top: 64px;
    }}

    .ai-result {{
        background-color: {COLORS['darkBlue']};
        color: white;
        padding: 32px;
        border-radius: 24px;
        margin-top: 32px;
    }}

    /* Chapter Header */
    .chapter-header {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-top: 120px;
        margin-bottom: 48px;
    }}
    .chapter-num {{
        color: {COLORS['darkGray']};
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.2em;
    }}
    .chapter-line {{
        height: 1px;
        flex: 1;
        background-color: {COLORS['darkGray']};
        opacity: 0.3;
    }}

    /* Blockquote */
    .vouch-quote {{
        border-left: 8px solid {COLORS['primaryGreen']};
        padding-left: 32px;
        font-style: italic;
        font-size: 24px;
        color: {COLORS['darkBlue']};
        margin: 48px 0;
        font-weight: 500;
        line-height: 1.4;
    }}

    /* Hide default Streamlit elements for clean port */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# --- GEMINI API HELPERS ---
API_KEY = "" # Environment provided

def call_gemini(prompt, system_instruction=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]} if system_instruction else None
    }
    delay = 1
    for _ in range(5):
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except: pass
        time.sleep(delay)
        delay *= 2
    return "The HLS AI Expert is currently offline. Please try again in a moment."

# --- SIDEBAR NAVIGATION (SMOOTH SCROLL PORT) ---
with st.sidebar:
    st.markdown(f"<div style='background-color:{COLORS['darkBlue']}; padding:10px; width:40px; height:40px; border-radius:4px; text-align:center; color:white; font-weight:bold; font-size:24px; margin-bottom:20px;'>V</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom:64px;'><div style='font-size:10px; font-weight:800; letter-spacing:0.2em; color:{COLORS['darkBlue']};'>WHITEPAPER</div><div style='font-size:12px; font-weight:500; color:{COLORS['darkBlue']};'>Vouch Insurance</div></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <a class="nav-link" href="#introduction">Introduction</a>
        <a class="nav-link" href="#chapter-1">1. HLS Today</a>
        <a class="nav-link" href="#chapter-2">2. 6 Core Risk Areas</a>
        <a class="nav-link" href="#chapter-3">3. New Risks</a>
        <a class="nav-link" href="#chapter-4">4. Scaling Risk</a>
        <a class="nav-link" href="#chapter-5">5. Insurance Missteps</a>
        <a class="nav-link" href="#conclusion">Conclusion</a>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<a href="https://vouch.us/healthcare-life-sciences" class="vouch-button">Talk to an Advisor</a>', unsafe_allow_html=True)

    # ✨ SIDEBAR EXPERT CHAT
    st.markdown("---")
    st.markdown("<div style='font-size:12px; font-weight:700; color:#0F1C2C; margin-bottom:12px;'>✨ HLS AI EXPERT</div>", unsafe_allow_html=True)
    chat_input = st.text_input("Ask about HLS risk...", key="expert_chat")
    if chat_input:
        with st.spinner("Analyzing..."):
            response = call_gemini(chat_input, "You are an AI assistant based on the Vouch HLS Blueprint. Answer professionaly and briefly.")
            st.info(response)

# --- MAIN CONTENT ---

# --- Introduction ---
st.markdown('<div id="introduction"></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">STRATEGY GUIDE</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-title">The Healthcare & Life Sciences <span style="color:{COLORS['primaryGreen']};">Blueprint</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Managing risk where science, tech, and regulation collide.</div>', unsafe_allow_html=True)

st.write("""
If you're building in Healthcare and Life Sciences, you're used to navigating uncertainty. Whether you're bringing a new therapy to market, scaling a virtual care platform, or deploying AI-powered diagnostics, you're operating at the intersection of science, technology, and regulation. The rewards are massive, but so are the risks.

From regulatory hurdles to clinical trial failures to data breaches exposing millions of patient records, a single misstep can derail years of work and potentially cost millions in investment. At the same time, breakthroughs save lives and reshape entire industries.

This paper is a practical guide for leaders navigating the high-stakes world of Healthcare and Life Sciences. We’ll break down:
""")

st.markdown("""
* **The six core risk areas** that consistently challenge growing companies.
* **Emerging exposures** tied to generative AI, ESG, and M&A.
* **How risk evolves as you grow** and why exposure looks different at every stage.
* **How to build an insurance strategy that scales with you.**
""")

# --- Chapter 1 ---
st.markdown('<div id="chapter-1"></div>', unsafe_allow_html=True)
st.markdown('<div class="chapter-header"><div class="chapter-num">CHAPTER 01</div><div class="chapter-line"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h2 style="font-size:40px; font-weight:800; color:{COLORS['darkBlue']}; margin-bottom:48px;">Healthcare and Life Sciences Today</h2>', unsafe_allow_html=True)

st.write("""
Healthcare and Life Sciences is moving faster than ever. Today, companies are advancing gene therapies, scaling virtual care, building AI-powered clinical decision tools, and applying machine learning to speed up everything from drug discovery to patient triage.

On the HealthTech side, the FDA has authorized over 1,000 AI-enabled medical devices for marketing in the U.S., a figure that continues to climb.
""")

# 1:1 METRICS CARDS PORT
m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <div>
                <div class="metric-value">1,000+</div>
                <div class="metric-label">AI-ENABLED MEDICAL DEVICES AUTHORIZED BY FDA</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 18h8M3 22h18M12 2h3.5a2.5 2.5 0 0 1 0 5H12V2zM9 2v20M12 7v7a2 2 0 0 1-2 2H9"/></svg>
            </div>
            <div>
                <div class="metric-value">90%</div>
                <div class="metric-label">DRUG CANDIDATES THAT FAIL IN CLINICAL TRIALS</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2C6.477 2 2 4.239 2 7v10c0 2.761 4.477 5 10 5s10-2.239 10-5V7c0-2.761-4.477-5-10-5z"/><path d="M2 7c0 2.761 4.477 5 10 5s10-2.239 10-5"/><path d="M2 12c0 2.761 4.477 5 10 5s10-2.239 10-5"/></svg>
            </div>
            <div>
                <div class="metric-value">289M</div>
                <div class="metric-label">US PATIENT RECORDS EXPOSED IN 2025</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="vouch-quote">
“From AI-enabled R&D to connected medical devices and decentralized trials, each advancement introduces new risks that demand vigilant oversight.” — Crowe 2025 Report
</div>
""", unsafe_allow_html=True)

# --- Chapter 2 ---
st.markdown('<div id="chapter-2"></div>', unsafe_allow_html=True)
st.markdown('<div class="chapter-header"><div class="chapter-num">CHAPTER 02</div><div class="chapter-line"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h2 style="font-size:40px; font-weight:800; color:{COLORS['darkBlue']}; margin-bottom:48px;">6 Risk Areas That Can Derail Growth</h2>', unsafe_allow_html=True)

st.write("HLS companies on the cutting edge are building in high-stakes conditions where a single misstep can cost time, funding, or lives.")

c2_1, c2_2 = st.columns(2)
with c2_1:
    with st.expander("1. Regulatory Risk", expanded=True):
        st.write("Compliance demands shift mid-sprint. From FDA approvals to Software as a Medical Device (SaMD) guidance.")
    with st.expander("2. Cyber Risk"):
        st.write("289M U.S. patient records exposed. Average breach cost is $7.42M—highest of any industry.")
    with st.expander("3. Clinical Trial Risk"):
        st.write("Roughly 90% of candidates fail. Loss of biological samples is an often-underestimated property risk.")

with c2_2:
    with st.expander("4. Supply Chain Risk"):
        st.write("Ranked as the #1 risk. Single contract manufacturers (CMOs/CROs) create dangerous single points of failure.")
    with st.expander("5. Product & Professional Liability"):
        st.write("Hybrid challenges: AI diagnostic tool errors or telehealth platform failures causing physical harm.")
    with st.expander("6. Executive & Board Risk"):
        st.write("Leadership carries personal risk. Shareholders may sue directors if a Phase 3 trial fails and valuation drops.")

# Chart
st.markdown("#### Average Data Breach Cost by Industry (2025)")
chart_data = pd.DataFrame({
    "Industry": ["Healthcare", "Financial Services", "Technology", "Retail"],
    "Cost ($M)": [7.42, 5.9, 4.6, 3.1]
})
st.bar_chart(chart_data, x="Industry", y="Cost ($M)", color=COLORS['textGreen'])

# --- Chapter 4 ---
st.markdown('<div id="chapter-4"></div>', unsafe_allow_html=True)
st.markdown('<div class="chapter-header"><div class="chapter-num">CHAPTER 04</div><div class="chapter-line"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h2 style="font-size:40px; font-weight:800; color:{COLORS['darkBlue']}; margin-bottom:48px;">How Risk Changes as You Scale</h2>', unsafe_allow_html=True)

st.write("A clinical-stage BioTech and a scaling HealthTech company need entirely different risk strategies.")

# ✨ AI TOOL: Strategy Generator
st.markdown(f"""
    <div class="ai-card">
        <h2 style="color:{COLORS['darkBlue']} !important; margin-bottom: 24px;">✨ Personalized Risk Action Plan</h2>
        <div style="font-size: 18px; opacity: 0.6; margin-bottom: 40px; color: {COLORS['darkBlue']};">Generate a custom 3-priority checklist from our HLS AI Expert.</div>
""", unsafe_allow_html=True)

f_col1, f_col2 = st.columns(2)
f_type = f_col1.selectbox("Company Type", ["BioTech / Pharma", "HealthTech / SaaS", "Medical Device"])
f_stage = f_col2.selectbox("Growth Stage", ["Pre-Seed / Seed", "Series A / B", "Commercialized"])

if st.button("✨ Generate My Strategy"):
    with st.spinner("Analyzing whitepaper context..."):
        prompt = f"Company: {f_type}, Stage: {f_stage}. Provide the top 3 risk priorities based on the whitepaper."
        strategy = call_gemini(prompt, "You are a specialist HLS risk consultant. Provide concise, bulleted priorities.")
        st.markdown(f'<div class="ai-result">{strategy}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Conclusion ---
st.markdown('<div id="conclusion"></div>', unsafe_allow_html=True)
st.title("Conclusion")

st.markdown(f"""
<div style='background-color:{COLORS['darkBlue']}; color:white; padding:80px; border-radius:48px; text-align:center; margin-top:80px;'>
    <h2 style='color:white !important; font-size:48px; font-weight:800; margin-bottom:24px;'>Built for What's Next.</h2>
    <p style='font-size:20px; opacity:0.8; margin-bottom:48px;'>Managing risk creates the confidence to move boldly.</p>
    <a href='https://vouch.us/healthcare-life-sciences' class='vouch-button' style='width:280px; margin:0 auto;'>Consult an Advisor</a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Vouch Insurance. The insurance broker for ambitious leaders.")
