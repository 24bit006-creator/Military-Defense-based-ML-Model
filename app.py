import streamlit as st
from PIL import Image
from vision_classifier import classify_recon_image
from decision_engine import evaluate_threat

# Page Configuration
st.set_page_config(
    page_title="VigilantE-X | Tactical Recon & Threat Verification",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize theme state (default: Dark/Slate Mode)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Tactical Orange Accent
accent_orange = "#FF6B00"
accent_orange_hover = "#E05D00"

# Theme-dependent styling
if st.session_state.dark_mode:
    bg_color = "#272E3F"              # Light Slate Gray background
    card_bg = "#1F2533"               # Contrast inner card container
    text_color = "#FFFFFF"            # Crisp white for dark mode
    sub_color = "#CBD5E1"             # Soft slate gray for subtitles
    input_bg = "#1A202C"              # Input box background
    border_color = "#475569"          # Defined border
    toggle_label = "☀️ Light View"
else:
    bg_color = "#E0F2FE"              # Baby blue / Light blue background
    card_bg = "#FFFFFF"               # White card container
    text_color = "#0F172A"            # Dark navy text
    sub_color = "#334155"             # Muted slate text
    input_bg = "#F8FAFC"              # Input box background
    border_color = "#BAE6FD"          # Soft blue border
    toggle_label = "🌙 Gray View"

# Custom CSS
st.markdown(f"""
<style>
    /* Hide Deploy button, Hamburger menu, and Footer */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Background and global typography */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    /* Centered Title and Subtitle */
    .header-container {{
        text-align: center;
        margin-top: 5px;
        margin-bottom: 25px;
    }}
    .recon-title {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: {text_color};
    }}
    .recon-subtitle {{
        font-size: 0.95rem;
        font-weight: 500;
        color: {sub_color};
        margin-top: 6px;
        line-height: 1.4;
    }}

    /* Orange Submit Button Styling */
    div.stButton > button[kind="primary"] {{
        background-color: {accent_orange} !important;
        border-color: {accent_orange} !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
    }}
    div.stButton > button[kind="primary"]:hover {{
        background-color: {accent_orange_hover} !important;
        border-color: {accent_orange_hover} !important;
        box-shadow: 0 6px 16px rgba(255, 107, 0, 0.5) !important;
    }}

    /* High-contrast labels */
    label, .stTextArea label, .stFileUploader label {{
        color: {text_color} !important;
        font-weight: 700 !important;
        font-size: 1.0rem !important;
    }}

    /* Input area styling */
    textarea, .stTextArea textarea {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1.5px solid {border_color} !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
    }}

    /* File Uploader styling */
    section[data-testid="stFileUploadDropzone"] {{
        background-color: {input_bg} !important;
        border: 1.5px dashed {border_color} !important;
        border-radius: 8px !important;
        color: {text_color} !important;
    }}
    section[data-testid="stFileUploadDropzone"] span {{
        color: {text_color} !important;
    }}

    /* Metrics in assessment block */
    [data-testid="stMetricValue"] {{
        color: {text_color} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {sub_color} !important;
        font-weight: 600 !important;
    }}
</style>
""", unsafe_allow_html=True)

# Top Bar with Right-Aligned Theme Toggle Button
_, col_toggle = st.columns([4, 1])
with col_toggle:
    if st.button(toggle_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Centered Header with Custom Orange Shield Icon
orange_shield_svg = f"""
<svg width="34" height="34" viewBox="0 0 24 24" fill="{accent_orange}" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; filter: drop-shadow(0px 2px 6px rgba(255,107,0,0.4));">
    <path d="M12 2L4 5V11.09C4 16.14 7.41 20.85 12 22C16.59 20.85 20 16.14 20 11.09V5L12 2ZM12 4.15L18 6.4V11.09C18 15.08 15.45 18.78 12 19.88C8.55 18.78 6 15.08 6 11.09V6.4L12 4.15Z"/>
    <path d="M12 6V18C14.7 17.06 16.74 14.18 16.96 11.09H12V6Z"/>
</svg>
"""

st.markdown(f"""
<div class="header-container">
    <div class="recon-title">{orange_shield_svg} VigilantE-X</div>
    <div class="recon-subtitle">Multimodal Tactical Reconnaissance & Threat Verification Engine.<br>Autonomous verification model designed for tactical defense reconnaissance.</div>
</div>
""", unsafe_allow_html=True)

# ----------------- Main Centered Inputs -----------------
uploaded_file = st.file_uploader("Upload Reconnaissance Asset Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Current Sensor Capture", use_container_width=True)

dispatch_input = st.text_area(
    "Field Dispatch / Radio Note:",
    height=120,
    placeholder="e.g. Unmarked heavy armored tank moving aggressively toward outpost bravo..."
)

analyze_btn = st.button("Analyze Recon Incident", type="primary", use_container_width=True)

# ----------------- Intelligence Assessment Output -----------------
if analyze_btn:
    if uploaded_file is None or not dispatch_input.strip():
        st.warning("Please provide both a reconnaissance photo and a dispatch note.")
    else:
        with st.spinner("Classifying optical features & evaluating intent..."):
            v_class, v_conf, v_hostile = classify_recon_image(uploaded_file)
            result = evaluate_threat(v_class, v_hostile, v_conf, dispatch_input)

        score = result["threat_score"]
        if score >= 75:
            banner_bg = "rgba(220, 38, 38, 0.25)"
            banner_border = "#EF4444"
            badge = "CRITICAL THREAT"
        elif score >= 45:
            banner_bg = "rgba(217, 119, 6, 0.25)"
            banner_border = "#F59E0B"
            badge = "ELEVATED ALERT"
        else:
            banner_bg = "rgba(16, 185, 129, 0.25)"
            banner_border = "#10B981"
            badge = "ROUTINE / ALL CLEAR"

        # Threat Banner
        st.markdown(f"""
        <div style="background-color: {banner_bg}; border-left: 5px solid {banner_border}; padding: 16px; border-radius: 8px; margin-top: 15px;">
            <div style="font-size: 1.15rem; font-weight: 800; color: {text_color};">{badge}</div>
            <div style="font-size: 1.0rem; font-weight: 600; color: {text_color}; margin-top: 4px;">Composite Threat Index: {score} / 100</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        # Model Output Metrics
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Visual Model Output", result["visual_class"], delta=f"{result['visual_confidence']}% Conf")
        with m2:
            st.metric("Text Intent Analysis", result["text_class"], delta=f"{result['text_confidence']}% Conf")

        st.markdown("#### Assessment Findings")
        st.info(result["status"])

        if result["deception_detected"]:
            st.error("**SPOOFING WARNING:** Visual classification directly contradicts dispatch statement!")

        st.markdown("#### Tactical Action Protocol")
        st.success(result["protocol"])