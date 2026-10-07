
import streamlit as st
import sys
sys.path.insert(0, ".")

from veris_engine import veris_auto, veris_verify, generate_proof_links

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

content_type = st.selectbox("Verification Type", ["Text", "Link / URL", "Mixed"])

content = None
content_data = None

if content_type == "Text":
    content = st.text_area("Paste text here:", height=150, placeholder="Paste any text to verify its structure...")
elif content_type == "Link / URL":
    content = st.text_input("Enter URL:", placeholder="https://example.com/article")
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
        ctype = "mixed"
    elif content:
        payload = content
        ctype = "link" if content_type == "Link / URL" else "text"
    else:
        st.warning("Please enter some content to verify.")
        st.stop()

    with st.spinner("Analyzing structure..."):
        result = veris_verify(payload, ctype)

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
