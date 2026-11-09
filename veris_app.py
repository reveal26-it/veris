import streamlit as st
import json
import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS
from supabase import create_client, Client
sys.path.insert(0, ".")

from veris_engine import veris_verify_full, generate_proof_links

st.set_page_config(page_title="Veris | Structural Verification", page_icon="🔍", layout="wide")

# ============================================================
# SUPABASE DATABASE CONNECTION
# ============================================================
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

# ============================================================
# FUTURISTIC CSS ENGINE
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #030303; }
    .logo-container { display: flex; align-items: center; gap: 15px; margin-bottom: 2rem; padding: 1rem; border-bottom: 1px solid #1a1a1a; }
    .logo-text { font-size: 2.5rem; font-weight: 800; color: #ffffff; letter-spacing: -0.05em; margin: 0; text-shadow: 0 0 20px rgba(0, 242, 254, 0.3); }
    .logo-tagline { font-size: 0.8rem; color: #00f2fe; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 5px; }
    .glass-card { background: rgba(20, 20, 20, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 2rem; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); margin-bottom: 1rem; }
    .severity-critical { background: linear-gradient(90deg, rgba(220,38,38,0.2) 0%, rgba(220,38,38,0.05) 100%); border-left: 4px solid #dc2626; color: #ff4d4d; padding: 1.5rem; border-radius: 8px; font-size: 1.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; text-shadow: 0 0 15px rgba(220,38,38,0.5); }
    .severity-high { background: linear-gradient(90deg, rgba(245,158,11,0.2) 0%, rgba(245,158,11,0.05) 100%); border-left: 4px solid #f59e0b; color: #fbbf24; padding: 1.5rem; border-radius: 8px; font-size: 1.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .severity-medium { background: linear-gradient(90deg, rgba(234,179,8,0.2) 0%, rgba(234,179,8,0.05) 100%); border-left: 4px solid #eab308; color: #fde047; padding: 1.5rem; border-radius: 8px; font-size: 1.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .severity-low, .severity-minimal { background: linear-gradient(90deg, rgba(34,197,94,0.2) 0%, rgba(34,197,94,0.05) 100%); border-left: 4px solid #22c55e; color: #4ade80; padding: 1.5rem; border-radius: 8px; font-size: 1.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .proof-item { background: #0a0a0a; padding: 1rem; border-radius: 8px; border: 1px solid #1a1a1a; margin-bottom: 0.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }
    .proof-trusted { border-left: 3px solid #22c55e; } .proof-forged { border-left: 3px solid #dc2626; } .proof-unknown { border-left: 3px solid #f59e0b; }
    .stTextArea textarea, .stTextInput input { background-color: #0a0a0a !important; border: 1px solid #222 !important; color: #00f2fe !important; font-family: 'JetBrains Mono', monospace !important; }
    .stButton button { background: transparent !important; color: #00f2fe !important; border: 1px solid #00f2fe !important; font-weight: 700 !important; font-family: 'JetBrains Mono', monospace !important; letter-spacing: 0.1em !important; }
    .stButton button:hover { background: #00f2fe !important; color: #000 !important; box-shadow: 0 0 25px rgba(0, 242, 254, 0.4) !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="logo-container">
    <svg width="60" height="60" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#00f2fe;stop-opacity:1" /><stop offset="100%" style="stop-color:#4facfe;stop-opacity:1" /></linearGradient></defs>
        <circle cx="100" cy="100" r="85" fill="none" stroke="url(#grad1)" stroke-width="3" opacity="0.3"/><circle cx="100" cy="100" r="60" fill="none" stroke="url(#grad1)" stroke-width="2" opacity="0.5"/>
        <line x1="100" y1="15" x2="100" y2="185" stroke="url(#grad1)" stroke-width="2" opacity="0.4"/><line x1="15" y1="100" x2="185" y2="100" stroke="url(#grad1)" stroke-width="2" opacity="0.4"/>
        <circle cx="100" cy="100" r="12" fill="url(#grad1)"/><circle cx="100" cy="40" r="4" fill="url(#grad1)" opacity="0.6"/><circle cx="100" cy="160" r="4" fill="url(#grad1)" opacity="0.6"/>
        <circle cx="40" cy="100" r="4" fill="url(#grad1)" opacity="0.6"/><circle cx="160" cy="100" r="4" fill="url(#grad1)" opacity="0.6"/>
    </svg>
    <div><div class="logo-text">VERIS</div><div class="logo-tagline">Structural Verification Engine v2.0</div></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MAIN INTERFACE
# ============================================================
col_input, col_empty, col_output = st.columns([1.2, 0.1, 1.2])

with col_input:
    st.markdown("<h3 style='color:#fff; font-weight:600;'>System Input</h3>", unsafe_allow_html=True)
    
    content_type = st.selectbox("Verification Type", ["Text", "Link / URL", "Image (Upload)", "Video (Upload)", "Audio (Upload)", "Document (Upload)", "Email", "Code", "Social Post", "Mixed"])
    
    content = None
    content_data = None

    if content_type == "Text":
        content = st.text_area("Paste text here:", height=150)
        
    elif content_type == "Link / URL":
        content = st.text_input("Enter URL:", placeholder="https://example.com/article")
        
    elif content_type == "Image (Upload)":
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            exif_data = {}
            if image._getexif():
                for tag_id, value in image._getexif().items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_data[tag] = value
            st.info(f"**Extracted Metadata:** {len(exif_data)} tags found.")
            i_visual = st.multiselect("Select visual artifacts (if visible):", ["clone stamp", "splicing", "lighting mismatch", "edge blur", "none"])
            content_data = {
                "metadata": {"creation_date": exif_data.get("DateTime", "unknown"), "device": exif_data.get("Make", "unknown"), "software": exif_data.get("Software", "unknown")},
                "visual_analysis": {"artifacts": [a for a in i_visual if a != "none"]},
                "text_in_image": "", "source_url": ""
            }

    elif content_type == "Video (Upload)":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
        if uploaded_file is not None:
            st.video(uploaded_file)
            st.info("Video uploaded. (Note: In production, this would run through an AI deepfake scanner).")
            v_visual = st.multiselect("Select visual artifacts:", ["face swap", "lip sync error", "lighting inconsistency", "none"])
            v_audio = st.multiselect("Select audio artifacts:", ["voice clone", "unnatural cadence", "none"])
            v_transcript = st.text_area("Transcript (if available):")
            content_data = {
                "metadata": {"creation_date": "unknown", "device": "unknown", "resolution": "unknown"},
                "frame_analysis": {"artifacts": [a for a in v_visual if a != "none"]},
                "audio_analysis": {"artifacts": [a for a in v_audio if a != "none"]},
                "transcript": v_transcript, "source_url": ""
            }

    elif content_type == "Audio (Upload)":
        uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "ogg"])
        if uploaded_file is not None:
            st.audio(uploaded_file)
            st.info("Audio uploaded. (Note: In production, this would run through a voice-clone detector).")
            a_artifacts = st.multiselect("Select audio artifacts:", ["voice clone", "unnatural cadence", "breath pattern missing", "none"])
            a_transcript = st.text_area("Transcript (if available):")
            content_data = {
                "metadata": {"creation_date": "unknown", "device": "unknown", "duration": "unknown"},
                "audio_analysis": {"artifacts": [a for a in a_artifacts if a != "none"]},
                "transcript": a_transcript, "source_url": ""
            }

    elif content_type == "Document (Upload)":
        uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt", "docx"])
        if uploaded_file is not None:
            st.info(f"Document uploaded: {uploaded_file.name}")
            if uploaded_file.type == "text/plain":
                doc_text = uploaded_file.read().decode("utf-8")
            else:
                doc_text = "Binary document (PDF/Word). Text extraction pending."
            content_data = {
                "metadata": {"creation_date": "unknown", "author": "unknown", "format": uploaded_file.type},
                "integrity": {"signals": []},
                "text": doc_text, "source_url": ""
            }

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
        if m_text: content_data["text"] = m_text
        if m_link: content_data["link"] = m_link

    st.markdown("<br>", unsafe_allow_html=True)
    verify_clicked = st.button("EXECUTE VERIFICATION", use_container_width=True)

with col_output:
    if verify_clicked:
        if content_data is not None:
            payload = content_data
            ctype_map = {"Image (Upload)": "image", "Video (Upload)": "video", "Audio (Upload)": "audio", "Document (Upload)": "document", "Email": "email", "Code": "code", "Social Post": "social", "Mixed": "mixed"}
            ctype = ctype_map.get(content_type, "text")
        elif content:
            payload = content
            ctype = "link" if content_type == "Link / URL" else "text"
        else:
            st.warning("Please enter some content to verify.")
            st.stop()

        with st.spinner("Analyzing structural integrity..."):
            result = veris_verify_full(payload, ctype)
            
        # Save to Database
        if supabase:
            try:
                v_res = result.get("verification", result)
                sev = v_res.get("severity", {})
                supabase.table("veris_logs").insert({
                    "content_type": ctype,
                    "content_snippet": str(payload)[:100],
                    "severity_score": sev.get("score", 0),
                    "severity_level": sev.get("level", "unknown"),
                    "reasons": sev.get("reasons", [])
                }).execute()
            except Exception as e:
                pass

        st.markdown("<h3 style='color:#fff; font-weight:600;'>Analysis Output</h3>", unsafe_allow_html=True)

        if "error" in result:
            st.error(result["error"])
        else:
            v = result.get("verification", result)
            if "severity" in v:
                sev = v["severity"]
                st.markdown(f'<div class="severity-{sev["level"]}">SEVERITY: {sev["score"]} / 100 — {sev["level"].upper()}</div>', unsafe_allow_html=True)
                
                # Display the Human-Readable Evidence Chain
                if sev.get("evidence_chain"):
                    st.markdown("<div style='background:#0a0a0a; padding:1.5rem; border-radius:8px; border-left:3px solid #00f2fe; margin-top:1rem;'>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color:#00f2fe; margin-top:0; font-family:JetBrains Mono; font-size:0.9rem;'>VERIFICATION EVIDENCE</h4>", unsafe_allow_html=True)
                    for e in sev["evidence_chain"]:
                        st.markdown(f"<div style='color:#ccc; font-size:0.9rem; margin-bottom:0.5rem; font-family:Inter;'>• {e}</div>", unsafe_allow_html=True)
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

st.markdown('<div style="text-align: center; color: #222; font-size: 0.7rem; margin-top: 4rem; font-family: monospace;">VERIS PROTOCOL v2.0 // WINDOW, NOT GATE</div>', unsafe_allow_html=True)
