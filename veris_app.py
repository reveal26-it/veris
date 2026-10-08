
import streamlit as st
import sys
sys.path.insert(0, ".")

from veris_engine import veris_verify_full, generate_proof_links

st.set_page_config(page_title="Veris", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; }
    .main-header { font-size: 3rem; font-weight: 800; color: #ffffff; margin-bottom: 0; }
    .sub-header { font-size: 1rem; color: #888888; margin-top: 0; margin-bottom: 2rem; }
    .severity-critical { background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; padding: 1.75rem; border-radius: 12px; font-size: 1.5rem; font-weight: 800; text-align: center; }
    .severity-high { background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%); color: white; padding: 1.75rem; border-radius: 12px; font-size: 1.5rem; font-weight: 800; text-align: center; }
    .severity-medium { background: linear-gradient(135deg, #eab308 0%, #a16207 100%); color: white; padding: 1.75rem; border-radius: 12px; font-size: 1.5rem; font-weight: 800; text-align: center; }
    .severity-low { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 1.75rem; border-radius: 12px; font-size: 1.5rem; font-weight: 800; text-align: center; }
    .severity-minimal { background: linear-gradient(135deg, #22c55e 0%, #15803d 100%); color: white; padding: 1.75rem; border-radius: 12px; font-size: 1.5rem; font-weight: 800; text-align: center; }
    .proof-item { background: #1c1c1c; padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid #333333; margin-bottom: 0.5rem; font-family: monospace; font-size: 0.85rem; }
    .proof-trusted { border-left: 3px solid #22c55e; }
    .proof-forged { border-left: 3px solid #ef4444; }
    .proof-unknown { border-left: 3px solid #f59e0b; }
    .footer { text-align: center; color: #555555; font-size: 0.8rem; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #222222; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Veris</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Structural Verification Engine</div>', unsafe_allow_html=True)

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
        v_date = st.text_input("Creation date:", key="v_date")
        v_device = st.text_input("Device:", key="v_device")
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
        i_date = st.text_input("Creation date:", key="i_date")
        i_device = st.text_input("Device:", key="i_device")
    with col2:
        i_software = st.text_input("Software:", key="i_software")
        i_source = st.text_input("Source URL:", key="i_source")
    i_text = st.text_area("Text in image:", height=100, key="i_text")
    i_visual = st.text_input("Visual artifacts:", key="i_visual")
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

verify_clicked = st.button("Verify", type="primary")

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

    with st.spinner("Analyzing structure..."):
        result = veris_verify_full(payload, ctype)

    st.markdown("---")

    if "error" in result:
        st.error(result["error"])
    else:
        v = result.get("verification", result)
        if "severity" in v:
            sev = v["severity"]
            st.markdown(f'<div class="severity-{sev["level"]}">SEVERITY: {sev["score"]} / 100 — {sev["level"].upper()}</div>', unsafe_allow_html=True)
            if sev.get("reasons"):
                st.markdown("### Reasons")
                for r in sev["reasons"]:
                    st.markdown(f"- {r}")
        elif "total_severity" in v:
            st.markdown(f'<div class="severity-{v["level"]}">TOTAL SEVERITY: {v["total_severity"]} / 100 — {v["level"].upper()}</div>', unsafe_allow_html=True)
            if v.get("all_reasons"):
                st.markdown("### Reasons")
                for r in v["all_reasons"]:
                    st.markdown(f"- {r}")

        proofs = generate_proof_links(result)
        if proofs:
            st.markdown("### Traceable Proofs")
            seen = set()
            for p in proofs:
                if p.get("url") and p["url"] not in seen:
                    seen.add(p["url"])
                    tier = p.get("trust_tier", "unknown")
                    score = p.get("trust_score", 0)
                    label = p.get("trust_label", "Unknown")
                    cls = "proof-trusted" if tier in ["verified", "trusted"] else "proof-forged" if p.get("forgery") else "proof-unknown"
                    st.markdown(f'<div class="proof-item {cls}"><a href="{p["url"]}" target="_blank" style="color:#3b82f6;">{p["label"]}</a> — {label} (score: {score})</div>', unsafe_allow_html=True)

        with st.expander("Full JSON Report"):
            st.json(v)

st.markdown('<div class="footer">Veris does not block content. It reveals. You decide.</div>', unsafe_allow_html=True)
