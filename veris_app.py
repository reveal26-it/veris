import streamlit as st
import json
import sys
sys.path.insert(0, ".")

from veris_engine import veris_verify_full, generate_proof_links

st.set_page_config(page_title="Veris | Structural Verification", page_icon="🔍", layout="wide")

# ============================================================
# FUTURISTIC CSS ENGINE
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #030303; }

    /* Neon Logo */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 2rem;
        padding: 1rem;
        border-bottom: 1px solid #1a1a1a;
    }
    .logo-mark {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: 800;
        color: #000;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.4);
    }
    .logo-text {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.05em;
        margin: 0;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
    }
    .logo-tagline {
        font-size: 0.8rem;
        color: #00f2fe;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 5px;
    }

    /* Futuristic Cards */
    .glass-card {
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 1rem;
    }

    /* Severity Banners */
    .severity-critical {
        background: linear-gradient(90deg, rgba(220,38,38,0.2) 0%, rgba(220,38,38,0.05) 100%);
        border-left: 4px solid #dc2626;
        color: #ff4d4d;
        padding: 1.5rem;
        border-radius: 8px;
        font-size: 1.5rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.1em;
        text-shadow: 0 0 15px rgba(220,38,38,0.5);
    }
    .severity-high {
        background: linear-gradient(90deg, rgba(245,158,11,0.2) 0%, rgba(245,158,11,0.05) 100%);
        border-left: 4px solid #f59e0b;
        color: #fbbf24;
        padding: 1.5rem;
        border-radius: 8px;
        font-size: 1.5rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 0 15px rgba(245,158,11,0.5);
    }
    .severity-medium {
        background: linear-gradient(90deg, rgba(234,179,8,0.2) 0%, rgba(234,179,8,0.05) 100%);
        border-left: 4px solid #eab308;
        color: #fde047;
        padding: 1.5rem;
        border-radius: 8px;
        font-size: 1.5rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
    }
    .severity-low, .severity-minimal {
        background: linear-gradient(90deg, rgba(34,197,94,0.2) 0%, rgba(34,197,94,0.05) 100%);
        border-left: 4px solid #22c55e;
        color: #4ade80;
        padding: 1.5rem;
        border-radius: 8px;
        font-size: 1.5rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 0 15px rgba(34,197,94,0.5);
    }

    /* Proof Items */
    .proof-item {
        background: #0a0a0a;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #1a1a1a;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }
    .proof-item:hover { border-color: #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.1); }
    .proof-trusted { border-left: 3px solid #22c55e; }
    .proof-forged { border-left: 3px solid #dc2626; }
    .proof-unknown { border-left: 3px solid #f59e0b; }

    /* Streamlit Overrides */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0a0a0a !important;
        border: 1px solid #222 !important;
        color: #00f2fe !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2) !important;
    }
    .stButton button {
        background: transparent !important;
        color: #00f2fe !important;
        border: 1px solid #00f2fe !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: 0.1em !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background: #00f2fe !important;
        color: #000 !important;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.4) !important;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="logo-container">
    <div class="logo-mark">V</div>
    <div>
        <div class="logo-text">VERIS</div>
        <div class="logo-tagline">Structural Verification Engine v1.0</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MAIN INTERFACE
# ============================================================
col_input, col_empty, col_output = st.columns([1.2, 0.1, 1.2])

with col_input:
    st.markdown("<h3 style='color:#fff; font-weight:600;'>System Input</h3>", unsafe_allow_html=True)
    
    content_type = st.selectbox("Verification Type", ["Text", "Link / URL", "Video", "Image", "Audio", "Document", "Email", "Code", "Social Post", "Mixed"])
    
    content = None
    content_data = None

    if content_type == "Text":
        content = st.text_area("Paste text here:", height=150)
    elif content_type == "Link / URL":
        content = st.text_input("Enter URL:", placeholder="https://example.com/article")
    elif content_type == "Video":
        col1, col2 = st.columns(2)
        with col1:
            v_date = st.text_input("Creation date:", key="v_date", placeholder="1970-01-01")
            v_device = st.text_input("Device:", key="v_device", placeholder="unknown")
        with col2:
            v_res = st.text_input("Resolution:", key="v_res")
            v_source = st.text_input("Source URL:", key="v_source")
        v_transcript = st.text_area("Transcript:", height=100, key="v_transcript")
        v_visual = st.text_input("Visual artifacts (comma-separated):", key="v_visual", placeholder="face swap, lip sync error")
        v_audio = st.text_input("Audio artifacts (comma-separated):", key="v_audio", placeholder="voice clone, unnatural cadence")
        content_data = {"metadata": {"creation_date": v_date, "device": v_device, "resolution": v_res}, "frame_analysis": {"artifacts": [a.strip() for a in v_visual.split(",") if a.strip()]}, "audio_analysis": {"artifacts": [a.strip() for a in v_audio.split(",") if a.strip()]}, "transcript": v_transcript, "source_url": v_source}
    elif content_type == "Image":
        col1, col2 = st.columns(2)
        with col1:
            i_date = st.text_input("Creation date:", key="i_date", placeholder="1970-01-01")
            i_device = st.text_input("Device:", key="i_device", placeholder="unknown")
        with col2:
            i_software = st.text_input("Software:", key="i_software", placeholder="Photoshop")
            i_source = st.text_input("Source URL:", key="i_source")
        i_text = st.text_area("Text in image:", height=100, key="i_text")
        i_visual = st.text_input("Visual artifacts:", key="i_visual", placeholder="clone stamp, splicing")
        content_data = {"metadata": {"creation_date": i_date, "device": i_device, "software": i_software}, "visual_analysis": {"artifacts": [a.strip() for a in i_visual.split(",") if a.strip()]}, "text_in_image": i_text, "source_url": i_source}
    elif content_type == "Audio":
        col1, col2 = st.columns(2)
        with col1:
            a_date = st.text_input("Creation date:", key="a_date")
            a_device = st.text_input("Device:", key="a_device")
        with col2:
            a_duration = st.text_input("Duration:", key="a_duration")
            a_source = st.text_input("Source URL:", key="a_source")
        a_transcript = st.text_area("Transcript:", height=100, key="a_transcript")
        a_artifacts = st.text_input("Audio artifacts:", key="a_artifacts")
        content_data = {"metadata": {"creation_date": a_date, "device": a_device, "duration": a_duration}, "audio_analysis": {"artifacts": [a.strip() for a in a_artifacts.split(",") if a.strip()]}, "transcript": a_transcript, "source_url": a_source}
    elif content_type == "Document":
        col1, col2 = st.columns(2)
        with col1:
            d_date = st.text_input("Creation date:", key="d_date")
            d_author = st.text_input("Author:", key="d_author")
        with col2:
            d_format = st.text_input("Format:", key="d_format")
            d_source = st.text_input("Source URL:", key="d_source")
        d_text = st.text_area("Document text:", height=150, key="d_text")
        d_signals = st.text_input("Tampering signals:", key="d_signals")
        content_data = {"metadata": {"creation_date": d_date, "author": d_author, "format": d_format}, "integrity": {"signals": [s.strip() for s in d_signals.split(",") if s.strip()]}, "text": d_text, "source_url": d_source}
    elif content_type == "Email":
        col1, col2 = st.columns(2)
        with col1:
            e_from = st.text_input("From:", key="e_from")
            e_spf = st.selectbox("SPF:", ["pass", "fail", "neutral"], key="e_spf")
        with col2:
            e_domain = st.text_input("Sending domain:", key="e_domain")
            e_dkim = st.selectbox("DKIM:", ["pass", "fail", "neutral"], key="e_dkim")
        e_body = st.text_area("Email body:", height=150, key="e_body")
        content_data = {"headers": {"from": e_from, "from_domain": e_domain, "spf": e_spf, "dkim": e_dkim}, "body": e_body}
    elif content_type == "Code":
        col1, col2 = st.columns(2)
        with col1:
            c_author = st.text_input("Author:", key="c_author")
        with col2:
            c_source = st.text_input("Source:", key="c_source")
        c_code = st.text_area("Code:", height=150, key="c_code")
        content_data = {"metadata": {"author": c_author, "source": c_source}, "code": c_code}
    elif content_type == "Social Post":
        col1, col2 = st.columns(2)
        with col1:
            s_age = st.text_input("Account age:", key="s_age")
            s_followers = st.number_input("Follower count:", min_value=0, value=0, key="s_followers")
        with col2:
            s_ratio = st.number_input("Like-to-share ratio:", min_value=0.0, value=0.0, key="s_ratio")
            s_similarity = st.slider("Comment similarity (0-1):", 0.0, 1.0, 0.0, key="s_similarity")
        s_text = st.text_area("Post text:", height=150, key="s_text")
        s_source = st.text_input("Source URL:", key="s_source")
        content_data = {"metadata": {"account_age": s_age, "follower_count": s_followers}, "engagement": {"like_to_share_ratio": s_ratio, "comment_similarity": s_similarity}, "text": s_text, "source_url": s_source}
    elif content_type == "Mixed":
        m_text = st.text_area("Text:", height=100, key="m_text")
        m_link = st.text_input("URL:", key="m_link")
        content_data = {}
        if m_text:
            content_data["text"] = m_text
        if m_link:
            content_data["link"] = m_link

    st.markdown("<br>", unsafe_allow_html=True)
    verify_clicked = st.button("EXECUTE VERIFICATION", use_container_width=True)

with col_output:
    if verify_clicked:
        if content_data is not None:
            payload = content_data
            ctype_map = {"Video": "video", "Image": "image", "Audio": "audio", "Document": "document", "Email": "email", "Code": "code", "Social Post": "social", "Mixed": "mixed"}
            ctype = ctype_map.get(content_type, "text")
        elif content:
            payload = content
            ctype = "link" if content_type == "Link / URL" else "text"
        else:
            st.warning("Please enter some content to verify.")
            st.stop()

        with st.spinner("Analyzing structural integrity..."):
            result = veris_verify_full(payload, ctype)

        st.markdown("<h3 style='color:#fff; font-weight:600;'>Analysis Output</h3>", unsafe_allow_html=True)

        if "error" in result:
            st.error(result["error"])
        else:
            v = result.get("verification", result)
            if "severity" in v:
                sev = v["severity"]
                st.markdown(f'<div class="severity-{sev["level"]}">SEVERITY: {sev["score"]} / 100 — {sev["level"].upper()}</div>', unsafe_allow_html=True)
                if sev.get("reasons"):
                    st.markdown("<div style='color:#888; font-family:monospace; font-size:0.85rem; margin-top:1rem;'>", unsafe_allow_html=True)
                    for r in sev["reasons"]:
                        st.markdown(f"<div style='margin-bottom:0.25rem;'>› {r}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            elif "total_severity" in v:
                st.markdown(f'<div class="severity-{v["level"]}">TOTAL SEVERITY: {v["total_severity"]} / 100 — {v["level"].upper()}</div>', unsafe_allow_html=True)
                if v.get("all_reasons"):
                    st.markdown("<div style='color:#888; font-family:monospace; font-size:0.85rem; margin-top:1rem;'>", unsafe_allow_html=True)
                    for r in v["all_reasons"]:
                        st.markdown(f"<div style='margin-bottom:0.25rem;'>› {r}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            proofs = generate_proof_links(result)
            if proofs:
                st.markdown("<br><h4 style='color:#fff; font-weight:600;'>Traceable Proofs</h4>", unsafe_allow_html=True)
                seen = set()
                for p in proofs:
                    if p.get("url") and p["url"] not in seen:
                        seen.add(p["url"])
                        tier = p.get("trust_tier", "unknown")
                        score = p.get("trust_score", 0)
                        label = p.get("trust_label", "Unknown")
                        cls = "proof-trusted" if tier in ["verified", "trusted"] else "proof-forged" if p.get("forgery") else "proof-unknown"
                        icon = "✅" if tier in ["verified", "trusted"] else "🚨" if p.get("forgery") else "⚠️"
                        st.markdown(f'<div class="proof-item {cls}">{icon} <a href="{p["url"]}" target="_blank" style="color:#00f2fe; text-decoration:none;">{p["label"]}</a> <span style="color:#555;">—</span> {label} <span style="color:#555;">(score: {score})</span></div>', unsafe_allow_html=True)

            with st.expander("RAW JSON DATA"):
                st.json(v)
    else:
        st.markdown("""
        <div class="glass-card" style="margin-top:2rem; text-align:center;">
            <h2 style="color:#222; font-size:5rem; margin:0;">⚡</h2>
            <p style="color:#555; font-family:monospace;">Awaiting system input...</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="text-align: center; color: #222; font-size: 0.7rem; margin-top: 4rem; font-family: monospace;">VERIS PROTOCOL v1.0 // WINDOW, NOT GATE</div>', unsafe_allow_html=True)
