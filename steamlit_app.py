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

# --- CUSTOM CSS ---
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
    }}
    
    /* Custom Container for Highlights */
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
    }}

    /* AI Tool Styling */
    .ai-card {{
        background-color: {COLORS['darkBlue']};
        color: {COLORS['white']};
        padding: 2rem;
        border-radius: 2rem;
        margin-top: 2rem;
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
    for i in range(5):
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            pass
        time.sleep(delay)
        delay *= 2
    return "I'm having trouble connecting to the AI expert right now. Please try again in a moment."

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(f"<div style='background-color:{COLORS['darkBlue']}; padding:10px; border-radius:8px; text-align:center; color:white; font-weight:bold; margin-bottom:20px;'>V</div>", unsafe_allow_html=True)
    st.title("HLS Blueprint")
    st.markdown("---")
    
    selection = st.radio(
        "Navigate Chapters",
        ["Introduction", "1. HLS Today", "2. 6 Core Risk Areas", "3. New Risks", "4. Scaling Risk", "5. Insurance Missteps", "Conclusion"]
    )
    
    st.markdown("---")
    st.markdown(f'<a href="https://vouch.us/healthcare-life-sciences" class="vouch-button" style="width:100%">Talk to an Advisor</a>', unsafe_allow_html=True)

# --- CONTENT SECTIONS ---

if selection == "Introduction":
    st.markdown(f"<span style='background-color:{COLORS['accentYellow']}; color:{COLORS['darkGreen']}; padding:4px 8px; border-radius:4px; font-size:10px; font-weight:bold; text-transform:uppercase;'>Strategy Guide</span>", unsafe_allow_html=True)
    st.title("The Healthcare & Life Sciences Blueprint")
    st.subheader("Managing risk where science, tech, and regulation collide.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        If you're building in Healthcare and Life Sciences, you're used to navigating uncertainty. Whether you're bringing a new therapy to market, scaling a virtual care platform, or deploying AI-powered diagnostics, you're operating at the intersection of science, technology, and regulation. The rewards are massive, but so are the risks.

        From regulatory hurdles to clinical trial failures to data breaches exposing millions of patient records, a single misstep can derail years of work and potentially cost millions in investment. At the same time, breakthroughs save lives and reshape entire industries.

        This paper is a practical guide for leaders navigating the high-stakes world of Healthcare and Life Sciences. We’ll break down:
        """)
        
        st.markdown(f"""
        - **The six core risk areas** that consistently challenge growing companies.
        - **Emerging exposures** tied to generative AI, ESG, and M&A.
        - **How risk evolves as you grow** from Seed to Commercialization.
        - **How to build an insurance strategy that scales with you.**
        """)
    with col2:
        st.markdown(f"""
        <div style='background-color:{COLORS['white']}; padding:20px; border-radius:15px; border:1px solid {COLORS['lightGray']};'>
            <h4 style='margin-top:0;'>Focus Areas</h4>
            <ul style='font-size:14px; color:{COLORS['textGreen']};'>
                <li>BioTech & Pharma</li>
                <li>HealthTech / SaaS</li>
                <li>Digital Health</li>
                <li>Medical Devices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif selection == "1. HLS Today":
    st.header("Chapter 1: Healthcare and Life Sciences Today")
    st.write("""
    Healthcare and Life Sciences is moving faster than ever. The COVID-19 pandemic didn't just accelerate telehealth, it kicked off a wave of investment and innovation across BioTech, HealthTech, digital therapeutics, and diagnostics. Today, companies are advancing gene therapies, scaling virtual care, building AI-powered clinical decision tools, and applying machine learning to speed up everything from drug discovery to patient triage.
    """)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("AI Medical Devices", "1,000+", delta="FDA Authorized", delta_color="normal")
    m2.metric("Breach Costs", "$7.42M", delta="Industry High")
    m3.metric("Clinical Fail Rate", "90%", delta="Drug Candidates")

    st.write("""
    Cloud infrastructure, machine learning, and real-time data are reshaping how research happens, how trials are run, and how treatments reach patients. Digital tools are helping to “derisk drug discovery” and compress development timelines that once stretched for years.
    
    ### Speed Comes with Tradeoffs
    Your company faces some of the highest-stakes risks in any industry. You operate in one of the most tightly regulated environments, handle extremely sensitive patient and genomic data, and often deal with materials that are irreplaceable or highly perishable.
    """)
    
    st.info("“From AI-enabled R&D to connected medical devices and decentralized trials, each advancement introduces new risks that demand vigilant oversight.” — Crowe 2025 Report")

elif selection == "2. 6 Core Risk Areas":
    st.header("Chapter 2: 6 Risk Areas That Can Derail Your Growth")
    
    risks = [
        {"title": "1. Regulatory Risk", "desc": "Compliance demands shift mid-sprint. From FDA approvals to HIPAA and the evolving framework for Software as a Medical Device (SaMD)."},
        {"title": "2. Cyber Risk", "desc": "HLS companies are prime targets. Record high breaches in 2025 with $7.42M average cost per healthcare data breach."},
        {"title": "3. Clinical Trial Risk", "desc": "Odd are steep. Sponsors bear full responsibility for protocol errors, safety events, or loss of critical research materials."},
        {"title": "4. Supply Chain Risk", "desc": "Ranked as the top risk above even cyber. Vulnerability to single contract manufacturers (CMOs/CROs)."},
        {"title": "5. Product & Professional Liability", "desc": "Hybrid liability challenges: part professional (malpractice), part product. Tech policies often gap bodily injury."},
        {"title": "6. Executive & Board Risk", "desc": "Leadership carries personal risk. Shareholders may sue if a Phase 3 trial fails or a valuation drops."}
    ]
    
    for r in risks:
        with st.expander(r['title']):
            st.write(r['desc'])
            st.button(f"View Coverage for {r['title'].split('.')[1]}", key=r['title'])

    st.markdown("---")
    st.subheader("Industry Context: Data Breach Costs (2025)")
    chart_data = pd.DataFrame({
        "Industry": ["Healthcare", "Financial", "Technology", "Retail"],
        "Cost ($ Millions)": [7.42, 5.9, 4.6, 3.1]
    })
    st.bar_chart(chart_data, x="Industry", y="Cost ($ Millions)", color=COLORS['textGreen'])

elif selection == "3. New Risks":
    st.header("Chapter 3: New Risks on the Horizon")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style='background-color:{COLORS['darkGreen']}; color:white; padding:25px; border-radius:20px;'>
            <h3 style='color:white !important;'>Generative AI</h3>
            <p>60% of HLS executives plan to increase Gen AI investment. Risks include training on sensitive data, output bias, and diagnostic errors.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style='background-color:{COLORS['white']}; border:1px solid {COLORS['lightGray']}; padding:25px; border-radius:20px;'>
            <h3>M&A Readiness</h3>
            <p>$240B in M&A investment in 2025. IP assignment chains and compliance gaps are the primary deal-breakers during diligence.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Environmental, Social, and Governance (ESG)")
    st.write("""
    Climate change directly threatens operations. 48% of Life Science companies cited natural disasters among top supply chain concerns. Social demands are also rising, with new FDA Diversity Action Plan requirements in 2025.
    """)

elif selection == "4. Scaling Risk":
    st.header("Chapter 4: How Risk Changes as You Scale")
    st.write("A clinical-stage BioTech and a scaling HealthTech company need entirely different risk strategies. Use major milestones as triggers for a risk review.")

    tab1, tab2 = st.tabs(["BioTech & Therapeutics", "HealthTech & Digital Health"])
    
    with tab1:
        st.table(pd.DataFrame([
            {"Stage": "Early (R&D)", "Risks": "Material loss, lab accidents", "Coverage": "Property (Spoilage), Workers' Comp"},
            {"Stage": "Clinical Trials", "Risks": "Injury, protocol error", "Coverage": "Clinical Trial Liability"},
            {"Stage": "Post-Approval", "Risks": "Market harm, recall", "Coverage": "Product Liability, Product Recall"}
        ]))
        
    with tab2:
        st.table(pd.DataFrame([
            {"Stage": "MVP / Early", "Risks": "Data breach, PHI exposure", "Coverage": "Cyber, E&O"},
            {"Stage": "Enterprise Pilot", "Risks": "HIPAA, bodily injury software", "Coverage": "Med Mal, Tech E&O (BI Endorsement)"},
            {"Stage": "Commercial Scale", "Risks": "Contract liability, scaling failure", "Coverage": "EPLI, Enhanced D&O"}
        ]))

    # --- ✨ AI RISK PLAN GENERATOR ---
    st.markdown(f"""
    <div class='ai-card'>
        <h2 style='color:{COLORS['primaryGreen']} !important;'>✨ Personalized Risk Action Plan</h2>
        <p>Generate a custom 3-step priority checklist based on your company stage.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        c1, c2, c3 = st.columns(3)
        comp_type = c1.selectbox("Company Type", ["BioTech", "HealthTech", "Medical Device"])
        comp_stage = c2.selectbox("Stage", ["Seed/R&D", "Clinical/Series A", "Commercial/Scaling"])
        comp_size = c3.text_input("Headcount", "1-20")
        
        if st.button("Generate Strategy"):
            with st.spinner("Analyzing HLS risk profile..."):
                sys_prompt = "You are an expert HLS risk consultant. Based on the whitepaper, provide a 3-step action plan for this specific user. Keep it brief and actionable."
                user_prompt = f"Company: {comp_type}, Stage: {comp_stage}, Employees: {comp_size}. What are my priorities?"
                strategy = call_gemini(user_prompt, sys_prompt)
                st.markdown(f"**Your Strategy:**\n\n{strategy}")

elif selection == "5. Insurance Missteps":
    st.header("Chapter 5: Insurance Missteps to Watch For")
    
    missteps = [
        ("Letting Coverage Go Stale", "A policy at Seed leaves you exposed at Series A. Adjust coverage before exposure changes."),
        ("Relying on Generic Policies", "Standard policies often exclude bodily injury from software—a dangerous gap for digital health."),
        ("Underinsuring or Overinsuring", "Match insurance to actual worst-case scenarios, not just lease requirements."),
        ("Working with Non-Specialists", "Brokers who don't know HLS may miss condemnation coverage or trial requirements.")
    ]
    
    for title, text in missteps:
        with st.container():
            st.markdown(f"#### {title}")
            st.write(text)
            st.markdown("---")

elif selection == "Conclusion":
    st.title("Conclusion")
    st.write("""
    Building in Healthcare and Life Sciences means operating in one of the most high-risk, high-reward environments out there. Resilience comes from combining strong operations with systems that scale. 
    
    **To founders and leaders: managing risk doesn't mean playing it safe, but creating the confidence to move boldly.**
    """)
    
    st.markdown(f"""
    <div style='background-color:{COLORS['darkBlue']}; color:white; padding:40px; border-radius:30px; text-align:center;'>
        <h2 style='color:{COLORS['primaryGreen']} !important;'>Ready to build your blueprint?</h2>
        <p>Talk to a Vouch advisor who specializes in Healthcare and Life Sciences.</p>
        <br>
        <a href='https://vouch.us/healthcare-life-sciences' class='vouch-button'>Visit Vouch.us</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2026 Vouch Insurance. Trusted by 6,000+ ambitious companies. Headquartered in San Francisco.")

# --- ✨ FLOATING EXPERT CHAT (GEMINI) ---
st.sidebar.markdown("---")
st.sidebar.subheader("✨ HLS AI Expert")
chat_input = st.sidebar.text_input("Ask a question about HLS Risk...")
if chat_input:
    with st.sidebar:
        with st.spinner("Thinking..."):
            sys_msg = "You are an AI assistant for the HLS Blueprint whitepaper. Use only the whitepaper context to answer. Be concise."
            response = call_gemini(chat_input, sys_msg)
            st.write(response)
