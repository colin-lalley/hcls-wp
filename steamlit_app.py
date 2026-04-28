import streamlit as st
import pandas as pd
import requests
import time

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

# --- CUSTOM CSS FOR SEAMLESS SCROLLING ---
st.markdown(f"""
    <style>
    /* Main Background and Text */
    .stApp {{
        background-color: {COLORS['lightTaupe']};
        color: {COLORS['darkBlue']};
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['white']};
        border-right: 1px solid {COLORS['lightGray']};
    }}
    
    /* Headings */
    h1, h2, h3 {{
        color: {COLORS['darkBlue']} !important;
        font-weight: 800 !important;
        margin-top: 2rem !important;
    }}
    
    /* Custom Sidebar Navigation Links */
    .nav-link {{
        display: block;
        padding: 0.5rem 1rem;
        color: {COLORS['darkGray']};
        text-decoration: none;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.2s;
        margin-bottom: 4px;
    }}
    .nav-link:hover {{
        background-color: {COLORS['lightGray']};
        color: {COLORS['darkBlue']};
    }}

    /* UI Components */
    .highlight-box {{
        padding: 2rem;
        border-radius: 1rem;
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['lightGray']};
        margin-bottom: 2rem;
    }}
    
    .vouch-button {{
        background-color: {COLORS['primaryGreen']};
        color: {COLORS['darkBlue']};
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
    }}

    .ai-card {{
        background-color: {COLORS['darkBlue']};
        color: {COLORS['white']};
        padding: 2.5rem;
        border-radius: 2rem;
        margin-top: 3rem;
        margin-bottom: 2rem;
    }}

    /* Remove default Streamlit anchor icons for cleaner look */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a {{
        display: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- GEMINI API HELPERS ---
API_KEY = "" # Handled by environment

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
    return "Expert currently unavailable."

# --- SIDEBAR NAVIGATION (JUMP LINKS) ---
with st.sidebar:
    st.markdown(f"<div style='background-color:{COLORS['darkBlue']}; padding:10px; border-radius:8px; text-align:center; color:white; font-weight:bold; margin-bottom:20px;'>V</div>", unsafe_allow_html=True)
    st.title("HLS Blueprint")
    st.markdown("---")
    st.markdown(f"""
        <a class="nav-link" href="#introduction">Introduction</a>
        <a class="nav-link" href="#chapter-1">1. HLS Today</a>
        <a class="nav-link" href="#chapter-2">2. 6 Core Risk Areas</a>
        <a class="nav-link" href="#chapter-3">3. New Risks</a>
        <a class="nav-link" href="#chapter-4">4. Scaling Risk</a>
        <a class="nav-link" href="#chapter-5">5. Insurance Missteps</a>
        <a class="nav-link" href="#conclusion">Conclusion</a>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<a href="https://vouch.us/healthcare-life-sciences" class="vouch-button" style="width:100%">Consult an Advisor</a>', unsafe_allow_html=True)

    # ✨ SIDEBAR CHAT (Expert Assistant)
    st.markdown("---")
    st.subheader("✨ HLS AI Expert")
    chat_input = st.text_input("Ask a question about HLS Risk...", key="chat_box")
    if chat_input:
        with st.spinner("Analyzing Knowledge Base..."):
            response = call_gemini(chat_input, "You are an AI assistant based on the Vouch HLS Blueprint. Be concise and professional.")
            st.info(response)

# --- MAIN CONTENT (ONE SEAMLESS FLOW) ---

# --- Introduction ---
st.markdown('<div id="introduction"></div>', unsafe_allow_html=True)
st.markdown(f"<span style='background-color:{COLORS['accentYellow']}; color:{COLORS['darkGreen']}; padding:4px 8px; border-radius:4px; font-size:10px; font-weight:bold; text-transform:uppercase;'>Strategy Guide</span>", unsafe_allow_html=True)
st.title("The Healthcare & Life Sciences Blueprint")
st.subheader("Managing risk where science, tech, and regulation collide.")

col_intro1, col_intro2 = st.columns([2, 1])
with col_intro1:
    st.write("""
    If you're building in Healthcare and Life Sciences, you're used to navigating uncertainty. Whether you're bringing a new therapy to market, scaling a virtual care platform, or deploying AI-powered diagnostics, you're operating at the intersection of science, technology, and regulation. 
    
    This paper is a practical guide for leaders navigating the high-stakes world of Healthcare and Life Sciences. We’ll break down the six core risk areas, emerging AI exposures, and how to build an insurance strategy that scales with you.
    """)
with col_intro2:
    st.markdown(f"""
    <div style='background-color:{COLORS['white']}; padding:20px; border-radius:15px; border:1px solid {COLORS['lightGray']};'>
        <h4 style='margin-top:0;'>At a Glance</h4>
        <ul style='font-size:13px; color:{COLORS['textGreen']}; margin-bottom:0;'>
            <li>6 Core Risk Factors</li>
            <li>Generative AI Safeguards</li>
            <li>Scaling Milestones</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Chapter 1 ---
st.markdown('<div id="chapter-1"></div>', unsafe_allow_html=True)
st.header("1. Healthcare and Life Sciences Today")
st.write("""
Healthcare and Life Sciences is moving faster than ever. Digital tools are helping to “derisk drug discovery” and compress development timelines that once stretched for years. The line between “health company” and “tech company” is increasingly difficult to draw.
""")

m1, m2, m3 = st.columns(3)
m1.metric("AI Medical Devices", "1,000+", "FDA Authorized")
m2.metric("Breach Costs", "$7.42M", "Industry Record")
m3.metric("Clinical Fail Rate", "90%", "R&D Reality")

st.info("“From AI-enabled R&D to connected medical devices, each advancement introduces new risks that demand vigilant oversight.” — Crowe 2025 Report")

st.markdown("---")

# --- Chapter 2 ---
st.markdown('<div id="chapter-2"></div>', unsafe_allow_html=True)
st.header("2. 6 Risk Areas That Can Derail Growth")
st.write("Cutting-edge companies operate with limited resources in high-stakes conditions where a single misstep can cost time, funding, or lives.")

c2_col1, c2_col2 = st.columns(2)
with c2_col1:
    with st.expander("1. Regulatory Risk", expanded=True):
        st.write("FDA approvals and HIPAA requirements are shifting. Software as a Medical Device (SaMD) guidance is expanding.")
    with st.expander("2. Cyber Risk"):
        st.write("289M U.S. patient records exposed in 2025. Costs exceed $7.4M per incident.")
    with st.expander("3. Clinical Trial Risk"):
        st.write("Protocol errors or safety events can halt years of research. Loss of biological samples is a major property risk.")

with c2_col2:
    with st.expander("4. Supply Chain Risk"):
        st.write("The #1 ranked risk. Vulnerability to single-source contract manufacturers and extreme weather events.")
    with st.expander("5. Product & Professional Liability"):
        st.write("AI diagnostic failures or software errors can cause physical harm, creating complex liability gaps.")
    with st.expander("6. Executive & Board Risk"):
        st.write("Venture-backed directors face personal liability if trials fail or regulatory issues scuttle M&A deals.")

# Data Viz
st.markdown("#### Cost of a Data Breach by Industry (2025)")
chart_data = pd.DataFrame({
    "Industry": ["Healthcare", "Financial", "Technology", "Retail"],
    "Cost ($M)": [7.42, 5.9, 4.6, 3.1]
})
st.bar_chart(chart_data, x="Industry", y="Cost ($M)", color=COLORS['textGreen'])

st.markdown("---")

# --- Chapter 3 ---
st.markdown('<div id="chapter-3"></div>', unsafe_allow_html=True)
st.header("3. New Risks on the Horizon")
st.write("As you scale, new risks surface that can impact valuation, delay deals, or quietly undermine trust.")

c3_col1, c3_col2, c3_col3 = st.columns(3)
with c3_col1:
    st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:{COLORS['darkGreen']}; color:white;'><b>Generative AI</b><br><small>Training on PHI, algorithmic bias, and diagnostic errors are top-of-mind.</small></div>", unsafe_allow_html=True)
with c3_col2:
    st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:{COLORS['accentBlue']}; color:{COLORS['darkBlue']};'><b>ESG Compliance</b><br><small>FDA Diversity requirements and climate risk in supply chains.</small></div>", unsafe_allow_html=True)
with c3_col3:
    st.markdown(f"<div style='padding:20px; border-radius:15px; border:1px solid {COLORS['lightGray']}; background-color:white;'><b>M&A Readiness</b><br><small>Clean IP ownership is critical for the $240B sellers market.</small></div>", unsafe_allow_html=True)

st.markdown("---")

# --- Chapter 4 ---
st.markdown('<div id="chapter-4"></div>', unsafe_allow_html=True)
st.header("4. How Risk Changes as You Scale")
st.write("Evolution from Seed to Commercialization requires qualitatively different insurance strategies.")

tab_bio, tab_health = st.tabs(["BioTech & Therapeutics", "HealthTech & Digital Health"])
with tab_bio:
    st.table(pd.DataFrame([
        {"Stage": "Early R&D", "Priority": "Spoilage / IP Protection"},
        {"Stage": "Clinical Trials", "Priority": "Participant Liability"},
        {"Stage": "Commercial", "Priority": "Product Recall / CBI"}
    ]))
with tab_health:
    st.table(pd.DataFrame([
        {"Stage": "MVP", "Priority": "Cyber / PHI Data"},
        {"Stage": "Enterprise Pilot", "Priority": "Tech E&O / Med Mal"},
        {"Stage": "Growth", "Priority": "EPLI / Scaling D&O"}
    ]))

# ✨ AI TOOL: Strategy Generator
st.markdown(f"""
    <div class='ai-card'>
        <h2 style='color:{COLORS['primaryGreen']} !important;'>✨ Personalized Action Plan</h2>
        <p>Get a custom risk management checklist from Gemini based on your stage.</p>
    </div>
""", unsafe_allow_html=True)

ai_col1, ai_col2 = st.columns(2)
comp_type = ai_col1.selectbox("Focus Area", ["BioTech", "HealthTech", "Devices"])
comp_stage = ai_col2.selectbox("Company Stage", ["Seed", "Series A/B", "Growth"])

if st.button("Generate Strategy"):
    with st.spinner("AI is analyzing whitepaper context..."):
        prompt = f"Company: {comp_type}, Stage: {comp_stage}. Give me 3 bullet points for my insurance strategy."
        strategy = call_gemini(prompt, "You are an expert HLS consultant based on the Vouch Blueprint. Be concise.")
        st.success(strategy)

st.markdown("---")

# --- Chapter 5 ---
st.markdown('<div id="chapter-5"></div>', unsafe_allow_html=True)
st.header("5. Insurance Missteps to Watch For")
st.write("Avoid these common pitfalls that leave growing HLS companies exposed.")

st.markdown(f"""
- **Letting Coverage Go Stale:** Seed policies don't work for Series A risks.
- **Generic Exclusions:** Standard Tech E&O often excludes physical bodily injury.
- **Broker Misalignment:** HLS needs specialists who understand spoilage and trial liability.
""")

st.markdown("---")

# --- Conclusion ---
st.markdown('<div id="conclusion"></div>', unsafe_allow_html=True)
st.title("Conclusion")
st.write("""
Building in HLS means operating in a high-risk, high-reward environment. Resilience comes from systems that scale. Managing risk doesn't mean playing it safe—it means creating the confidence to move boldly.
""")

st.markdown(f"""
<div style='background-color:{COLORS['darkBlue']}; color:white; padding:50px; border-radius:40px; text-align:center;'>
    <h2 style='color:{COLORS['primaryGreen']} !important;'>Built for What's Next.</h2>
    <p>Get the coverage you need to scale with confidence.</p>
    <a href='https://vouch.us/healthcare-life-sciences' class='vouch-button'>Consult an Advisor</a>
</div>
""", unsafe_allow_html=True)

st.caption("© 2026 Vouch Insurance. Headquartered in San Francisco.")
