import hashlib
import re
from urllib.parse import urlparse

# ... (Keep all your primary, secondary, and tertiary reference dictionaries exactly as they are) ...
# I am only showing the functions here to save space, but you will paste the whole file.

def check_soundness(text):
    # Basic contradiction check
    if "always" in text.lower() and "never" in text.lower():
        return {"check": "soundness", "result": "incoherent", "reason": "Contains contradictory terms (always/never)"}
    return {"check": "soundness", "result": "coherent", "reason": "No contradiction detected"}

def check_contradiction(text):
    # NEW: Structural Contradiction Check
    text_lower = text.lower()
    
    # Check for financial contradictions
    if re.search(r'\$[\d,]+(m|k|b)', text_lower) and "however" in text_lower and "only" in text_lower:
        return {"check": "contradiction", "result": "contradictory", "reason": "Conflicting financial figures detected."}
        
    # Check for legal/status contradictions
    if ("scheduled to finalize" in text_lower or "scheduled to close" in text_lower) and ("bankruptcy" in text_lower or "legally impossible" in text_lower):
        return {"check": "contradiction", "result": "contradictory", "reason": "Conflicting legal status detected."}
        
    return {"check": "contradiction", "result": "none", "reason": "No structural contradiction detected."}

def check_primary_validity(text):
    # ... keep existing logic ...
    pass

def check_secondary_validity(text):
    # ... keep existing logic ...
    pass

def check_interconnection(text):
    # ... keep existing logic ...
    pass

def calculate_severity(result):
    score = 0
    reasons = []
    soundness = result.get("soundness", {})
    contradiction = result.get("contradiction", {})
    primary = result.get("primary_validity", {})
    secondary = result.get("secondary_validity", {})
    intercon = result.get("interconnection", {})

    # NEW: Contradiction penalty
    if contradiction.get("result") == "contradictory":
        score += 40
        reasons.append("Structural contradiction detected: " + contradiction.get("reason", ""))

    if soundness.get("result") == "incoherent":
        score += 20
        reasons.append("Incoherent terms detected")

    # ... keep existing severity logic for primary, secondary, intercon ...
    
    score = min(score, 100)
    level = "critical" if score >= 70 else "high" if score >= 50 else "medium" if score >= 30 else "low" if score >= 10 else "minimal"
    return {"score": score, "level": level, "reasons": reasons}

def verify(text):
    soundness = check_soundness(text)
    contradiction = check_contradiction(text)
    primary = check_primary_validity(text)
    secondary = check_secondary_validity(text)
    intercon = check_interconnection(text)
    
    result = {
        "input": text,
        "soundness": soundness,
        "contradiction": contradiction,
        "primary_validity": primary,
        "secondary_validity": secondary,
        "interconnection": intercon
    }
    result["severity"] = calculate_severity(result)
    return result
