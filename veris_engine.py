import hashlib
import re
from urllib.parse import urlparse

primary_reference = {
    "ontological_patterns": [
        {"id": "john_1_1", "name": "Logos Containment", "components": ["word", "beginning", "with god", "was god"]},
        {"id": "genesis_1_1", "name": "Creation Origin", "components": ["source", "spoke", "commanded", "came to be", "created"]},
        {"id": "proverbs_3_5_6", "name": "Alignment Path", "components": ["trust", "lord", "heart", "lean not", "straight"]},
        {"id": "procession", "name": "Procession", "components": ["sends", "proceeds", "manifests", "sent"]},
        {"id": "fountainhead", "name": "Fountainhead", "components": ["fountain", "wellspring", "spring", "source of life"]},
        {"id": "narrow_way", "name": "Narrow Way", "components": ["narrow", "wide", "path", "gate"]},
        {"id": "vine_branch", "name": "Vine Branch", "components": ["vine", "branch", "fruit", "abide"]},
        {"id": "source_sustains", "name": "Source Sustains", "components": ["from him", "through him", "to him", "all things"]},
        {"id": "predestination", "name": "Predestination", "components": ["chosen", "before", "predestined", "foundation"]},
        {"id": "word_became_flesh", "name": "Word Became Flesh", "components": ["word", "flesh", "became", "dwelt"]},
        {"id": "substitution", "name": "Substitution", "components": ["substitute", "died for", "in place", "for many"]},
        {"id": "death_resurrection", "name": "Death Resurrection", "components": ["died", "buried", "raised", "third day"]},
        {"id": "sowing_reaping", "name": "Sowing Reaping", "components": ["sow", "reap", "seed", "harvest"]},
        {"id": "two_builders", "name": "Two Builders", "components": ["builder", "rock", "sand", "foundation"]},
        {"id": "prodigal", "name": "Prodigal", "components": ["prodigal", "departure", "ruin", "return", "restoration"]},
        {"id": "one_body", "name": "One Body", "components": ["one body", "many members", "unity", "diversity"]},
        {"id": "family", "name": "Family", "components": ["father", "children", "inheritance", "family"]},
        {"id": "king_subjects", "name": "King and Subjects", "components": ["king", "subjects", "decree", "obedience"]},
        {"id": "throne", "name": "Throne", "components": ["throne", "authority", "worship", "surrounded"]},
        {"id": "golden_rule", "name": "Golden Rule", "components": ["treat", "others", "yourself", "want"]}
    ],
    "triadic_functions": [
        {"id": "creation_triad", "name": "Creation Pattern", "expression": "spoke", "relation": "commanded", "emergence": "came to be"},
        {"id": "incarnation_triad", "name": "Incarnation Pattern", "expression": "word", "relation": "dwelt among", "emergence": "beheld glory"},
        {"id": "spirit_triad", "name": "Spirit Triad", "expression": "hears", "relation": "speaks", "emergence": "guides"},
        {"id": "building_triad", "name": "Building Triad", "expression": "hears", "relation": "does", "emergence": "stands"},
        {"id": "virtue_triad", "name": "Virtue Triad", "expression": "faith", "relation": "hope", "emergence": "love"},
        {"id": "human_triad", "name": "Human Triad", "expression": "spirit", "relation": "soul", "emergence": "body"}
    ],
    "logical_structures": [
        {"id": "modus_ponens", "name": "Modus Ponens", "components": ["if", "then", "is raining", "is true", "therefore"]},
        {"id": "modus_tollens", "name": "Modus Tollens", "components": ["if", "then", "not", "false", "cannot be"]},
        {"id": "syllogism", "name": "Syllogism", "components": ["all men", "all a", "mortal", "socrates", "man"]},
        {"id": "disjunctive_syllogism", "name": "Disjunctive Syllogism", "components": ["either", "or", "cannot", "go left", "go right"]},
        {"id": "non_contradiction", "name": "Law of Non-Contradiction", "components": ["cannot", "both", "not", "same"]},
        {"id": "identity", "name": "Law of Identity", "components": ["is", "same", "identical"]},
        {"id": "excluded_middle", "name": "Law of Excluded Middle", "components": ["either", "or", "not", "must"]},
        {"id": "induction", "name": "Induction", "components": ["all", "every", "therefore", "instances"]},
        {"id": "abduction", "name": "Abduction", "components": ["best", "explanation", "therefore", "likely"]},
        {"id": "conjunction", "name": "Conjunction", "components": ["and", "therefore", "both"]},
        {"id": "quantifiers", "name": "Universal/Existential", "components": ["all", "some", "every", "any"]},
        {"id": "equivalence", "name": "Logical Equivalence", "components": ["if and only if", "iff", "equivalent", "same as"]}
    ],
    "mathematical_structures": [
        {"id": "equality", "name": "Equality", "components": ["equals", "=", "is equal to", "same"]},
        {"id": "transitivity", "name": "Transitivity", "components": ["equals", "and", "then", "therefore"]},
        {"id": "symmetry", "name": "Symmetry", "components": ["mutual", "both ways", "reciprocal"]},
        {"id": "proportion", "name": "Proportion", "components": ["ratio", "proportion", "per", "rate"]}
    ],
    "causal_structures": [
        {"id": "cause_effect", "name": "Cause and Effect", "components": ["causes", "leads to", "results in", "because"]},
        {"id": "necessary_sufficient", "name": "Necessary/Sufficient", "components": ["necessary", "sufficient", "requires", "needs"]},
        {"id": "correlation", "name": "Correlation", "components": ["correlates", "associated", "linked", "connected"]},
        {"id": "feedback", "name": "Feedback Loop", "components": ["loop", "cycle", "reinforces", "feeds back"]}
    ],
    "relational_structures": [
        {"id": "part_whole", "name": "Part-Whole", "components": ["part of", "contains", "includes", "member of"]},
        {"id": "hierarchy", "name": "Hierarchy", "components": ["contains", "under", "above", "level"]},
        {"id": "network", "name": "Network", "components": ["connects", "links", "network", "node"]},
        {"id": "opposition", "name": "Opposition", "components": ["opposite", "contrary", "against", "versus"]}
    ],
    "temporal_structures": [
        {"id": "before_after", "name": "Before/After", "components": ["before", "after", "then", "next"]},
        {"id": "sequence", "name": "Sequence", "components": ["first", "then", "finally", "next"]},
        {"id": "cycle", "name": "Cycle", "components": ["cycle", "repeats", "returns", "again"]}
    ],
    "ethical_structures": [
        {"id": "golden_rule", "name": "Golden Rule", "components": ["treat", "others", "yourself", "want"]},
        {"id": "reciprocity", "name": "Reciprocity", "components": ["give", "take", "return", "balance"]},
        {"id": "justice", "name": "Justice", "components": ["fair", "just", "deserve", "proportional"]},
        {"id": "mercy", "name": "Mercy", "components": ["mercy", "compassion", "forgive", "grace"]}
    ],
    "linguistic_structures": [
        {"id": "definition", "name": "Definition", "components": ["means", "defined as", "refers to", "is called"]},
        {"id": "synonym", "name": "Synonym", "components": ["same as", "synonymous", "equivalent"]},
        {"id": "antonym", "name": "Antonym", "components": ["opposite", "contrary", "reverse"]},
        {"id": "metaphor", "name": "Metaphor", "components": ["like", "as", "similar to", "metaphor"]},
        {"id": "analogy", "name": "Analogy", "components": ["is to", "as", "analogy", "proportion"]}
    ],
    "axioms": ["Every state traces to an origin", "Nothing is self-originating", "All things co-arise in relation", "Alignment with Source yields coherence", "Broken trace yields null"],
    "basic_laws": ["Soundness", "Primary Validity", "Secondary Validity", "Interconnection"]
}

secondary_reference = {
    "source_types": [
        {"id": "domain", "name": "Domain", "trace_markers": [".com", ".org", ".gov", ".edu", ".ng", ".io", "www."]},
        {"id": "email", "name": "Email", "trace_markers": ["@", "mailto:"]},
        {"id": "account", "name": "Account", "trace_markers": ["@", "twitter.com", "facebook.com"]},
        {"id": "document", "name": "Document", "trace_markers": ["doi:", "isbn", "case no", "exhibit"]}
    ],
    "trace_quality": [
        {"id": "verified", "name": "Verified"},
        {"id": "unverified", "name": "Unverified"},
        {"id": "forged", "name": "Forged"}
    ],
    "known_domains": [
        {"domain": "harvard.edu", "type": "academic", "verified": True},
        {"domain": "reuters.com", "type": "news", "verified": True},
        {"domain": "apnews.com", "type": "news", "verified": True},
        {"domain": "nature.com", "type": "academic", "verified": True},
        {"domain": "science.org", "type": "academic", "verified": True},
        {"domain": "cdc.gov", "type": "government", "verified": True},
        {"domain": "nih.gov", "type": "government", "verified": True},
        {"domain": "nasa.gov", "type": "government", "verified": True},
        {"domain": "justice.gov", "type": "government", "verified": True},
        {"domain": "bbc.com", "type": "news", "verified": True},
        {"domain": "cnn.com", "type": "news", "verified": True},
        {"domain": "nytimes.com", "type": "news", "verified": True},
        {"domain": "theguardian.com", "type": "news", "verified": True},
        {"domain": "aljazeera.com", "type": "news", "verified": True},
        {"domain": "who.int", "type": "international", "verified": True},
        {"domain": "un.org", "type": "international", "verified": True},
        {"domain": "punchng.com", "type": "news", "verified": True},
        {"domain": "vanguardngr.com", "type": "news", "verified": True},
        {"domain": "premiumtimesng.com", "type": "news", "verified": True}
    ],
    "known_accounts": [
        {"handle": "@reuters", "platform": "twitter", "verified": True},
        {"handle": "@apnews", "platform": "twitter", "verified": True},
        {"handle": "@who", "platform": "twitter", "verified": True},
        {"handle": "@bbc", "platform": "twitter", "verified": True}
    ],
    "known_forgeries": [
        {"pattern": "harvard-research.org", "type": "fake_academic", "note": "Impersonates Harvard"},
        {"pattern": "bbc-news.co", "type": "fake_news", "note": "Impersonates BBC"},
        {"pattern": "cnn-breaking.com", "type": "fake_news", "note": "Impersonates CNN"},
        {"pattern": "who-health.org", "type": "fake_international", "note": "Impersonates WHO"},
        {"pattern": "un-news.com", "type": "fake_international", "note": "Impersonates UN"},
        {"pattern": "reuters-news.co", "type": "fake_news", "note": "Impersonates Reuters"}
    ]
}

tertiary_reference = {
    "coordination_markers": [
        {"id": "urgency", "name": "Urgency", "phrases": ["share this", "before they delete", "act now", "don't wait"], "weight": 2},
        {"id": "awakening", "name": "Awakening", "phrases": ["wake up", "open your eyes", "sheeple", "blind"], "weight": 2},
        {"id": "suppression", "name": "Suppression", "phrases": ["they don't want you to know", "hidden truth", "covered up", "silenced"], "weight": 2},
        {"id": "conspiracy", "name": "Conspiracy", "phrases": ["deep state", "new world order", "globalist", "false flag"], "weight": 2},
        {"id": "miracle", "name": "Miracle Cure", "phrases": ["doctors hate this", "one weird trick", "miracle cure", "big pharma"], "weight": 2},
        {"id": "division", "name": "Division", "phrases": ["enemy", "they", "them", "against us", "fight back"], "weight": 2},
        {"id": "fear", "name": "Fear", "phrases": ["danger", "threat", "emergency", "crisis", "collapse"], "weight": 1}
    ],
    "deepfake_signatures": [
        {"id": "audio_deepfake", "name": "Audio Deepfake", "markers": ["voice clone", "synthetic audio", "unnatural cadence"]},
        {"id": "video_deepfake", "name": "Video Deepfake", "markers": ["face swap", "lip sync error", "lighting inconsistency"]},
        {"id": "image_manipulation", "name": "Image Manipulation", "markers": ["clone stamp", "splicing", "compression artifact"]}
    ],
    "propagation_patterns": [
        {"id": "simultaneous", "name": "Simultaneous Posting"},
        {"id": "bot_network", "name": "Bot Network"},
        {"id": "cross_platform", "name": "Cross-Platform"}
    ]
}


def check_soundness(text):
    if "always" in text.lower() and "never" in text.lower():
        return {"check": "soundness", "result": "incoherent", "reason": "Contains contradictory terms"}
    return {"check": "soundness", "result": "coherent", "reason": "No contradiction detected"}

def check_primary_validity(text):
    text_lower = text.lower()
    text_words = set(text_lower.split())
    all_matches = []
    categories = ["triadic_functions", "ontological_patterns", "linguistic_structures", "ethical_structures", "temporal_structures", "relational_structures", "causal_structures", "mathematical_structures", "logical_structures"]
    def stem_match(component, text_lower, text_words):
        c_lower = component.lower()
        if c_lower in text_lower:
            return True
        for suffix in ["s", "ed", "ing", "es"]:
            if c_lower.endswith(suffix):
                stem = c_lower[:-len(suffix)]
                if stem in text_lower:
                    return True
        for suffix in ["s", "ed", "ing"]:
            if c_lower + suffix in text_lower:
                return True
        if " " in c_lower:
            parts = c_lower.split()
            if all(p in text_words or any(p + s in text_words for s in ["s", "ed", "ing"]) for p in parts):
                return True
        return False
    for category in categories:
        if category not in primary_reference:
            continue
        for pattern in primary_reference[category]:
            components = pattern.get("components", [])
            if not components:
                continue
            matches = [c for c in components if stem_match(c, text_lower, text_words)]
            threshold = max(2, len(components) // 3)
            if len(matches) >= threshold:
                all_matches.append({"pattern": pattern["name"], "category": category, "matched_components": matches, "score": len(matches)})
    if all_matches:
        all_matches.sort(key=lambda x: x["score"], reverse=True)
        return {"check": "primary_validity", "result": "aligned", "matches": all_matches, "total_patterns": len(all_matches)}
    return {"check": "primary_validity", "result": "unaligned", "matches": [], "total_patterns": 0}

def extract_urls(text):
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)

def parse_url(url):
    try:
        parsed = urlparse(url)
        return {"full": url, "scheme": parsed.scheme, "domain": parsed.netloc, "path": parsed.path, "query": parsed.query}
    except Exception:
        return {"full": url, "error": "parse failed"}

def classify_domain(domain):
    domain_lower = domain.lower()
    for known in secondary_reference["known_domains"]:
        if known["domain"] in domain_lower:
            return {"category": known["type"], "base_score": 90, "source": "known_list", "verified": known["verified"]}
    for forgery in secondary_reference["known_forgeries"]:
        if forgery["pattern"] in domain_lower:
            return {"category": "forgery", "base_score": 0, "source": "known_forgery", "note": forgery["note"]}
    categories = {
        "government": {"tlds": [".gov", ".gov.uk", ".gov.ng"], "base_score": 70},
        "academic": {"tlds": [".edu", ".ac.uk", ".edu.ng"], "base_score": 65},
        "international": {"tlds": [".int", ".org"], "base_score": 55},
        "news": {"tlds": [".com", ".co.uk"], "keywords": ["news", "times", "post", "herald"], "base_score": 50},
        "commercial": {"tlds": [".com", ".io", ".co"], "base_score": 40},
        "personal": {"tlds": [".me", ".blog", ".xyz"], "base_score": 25}
    }
    for category, rules in categories.items():
        for tld in rules.get("tlds", []):
            if domain_lower.endswith(tld):
                score = rules["base_score"]
                for kw in rules.get("keywords", []):
                    if kw in domain_lower:
                        score += 10
                        break
                return {"category": category, "base_score": score, "source": "tld_analysis"}
    return {"category": "unknown", "base_score": 30, "source": "unclassified"}

def get_trust_tier(score):
    tiers = {"verified": 80, "trusted": 60, "neutral": 40, "suspicious": 20, "untrusted": 0}
    for tier, threshold in tiers.items():
        if score >= threshold:
            return {"tier": tier, "label": tier.capitalize() + " Source"}
    return {"tier": "untrusted", "label": "Untrusted Source"}

def auto_trust_score(domain):
    classification = classify_domain(domain)
    score = classification.get("base_score", 30)
    tier = get_trust_tier(score)
    return {"domain": domain, "score": score, "tier": tier["tier"], "label": tier["label"], "category": classification["category"], "verified": classification.get("verified", False), "note": classification.get("note")}

def verify_domain(domain):
    trust = auto_trust_score(domain)
    return {"domain": domain, "exists": True, "trusted": trust["tier"] in ["verified", "trusted"], "type": trust["category"], "score": trust["score"], "tier": trust["tier"], "label": trust["label"], "note": trust.get("note")}

def trace_urls(text):
    urls = extract_urls(text)
    results = []
    for url in urls:
        parsed = parse_url(url)
        domain = parsed.get("domain", "")
        is_forgery = False
        forgery_note = None
        for forgery in secondary_reference["known_forgeries"]:
            if forgery["pattern"] in domain:
                is_forgery = True
                forgery_note = forgery["note"]
                break
        is_trusted = False
        domain_type = None
        for known in secondary_reference["known_domains"]:
            if known["domain"] in domain:
                is_trusted = True
                domain_type = known["type"]
                break
        results.append({"url": url, "domain": domain, "trusted": is_trusted, "forgery": is_forgery, "type": domain_type, "note": forgery_note})
    return results

def check_secondary_validity(text):
    text_lower = text.lower()
    found_traces = []
    quality = "untraced"
    urls = trace_urls(text)
    for forgery in secondary_reference["known_forgeries"]:
        if forgery["pattern"] in text_lower:
            return {"check": "secondary_validity", "result": "traced", "quality": "forged", "found": [{"type": "forgery", "value": forgery["pattern"], "note": forgery["note"]}], "urls": urls}
    for u in urls:
        if u["forgery"]:
            return {"check": "secondary_validity", "result": "traced", "quality": "forged", "found": [{"type": "forgery", "value": u["domain"], "note": u["note"]}], "urls": urls}
        elif u["trusted"]:
            found_traces.append({"type": u["type"], "value": u["domain"], "verified": True})
        else:
            found_traces.append({"type": "unknown", "value": u["domain"], "verified": False})
    if not found_traces:
        for domain in secondary_reference["known_domains"]:
            if domain["domain"] in text_lower:
                found_traces.append({"type": domain["type"], "value": domain["domain"], "verified": domain["verified"]})
    if found_traces:
        verified_count = sum(1 for t in found_traces if t.get("verified", False))
        quality = "verified" if verified_count > 0 else "unverified"
        return {"check": "secondary_validity", "result": "traced", "quality": quality, "found": found_traces, "urls": urls}
    return {"check": "secondary_validity", "result": "untraced", "quality": "untraced", "found": [], "urls": urls}

def check_interconnection(text):
    text_lower = text.lower()
    found_markers = []
    total_weight = 0
    for marker in tertiary_reference["coordination_markers"]:
        matched_phrases = [p for p in marker["phrases"] if p in text_lower]
        if matched_phrases:
            found_markers.append({"category": marker["name"], "phrases": matched_phrases, "weight": marker["weight"] * len(matched_phrases)})
            total_weight += marker["weight"] * len(matched_phrases)
    if total_weight >= 6:
        level = "highly_interconnected"
    elif total_weight >= 3:
        level = "interconnected"
    elif total_weight >= 1:
        level = "weakly_interconnected"
    else:
        level = "isolated"
    return {"check": "interconnection", "result": level, "total_weight": total_weight, "markers": found_markers}

def calculate_severity(result):
    score = 0
    reasons = []
    soundness = result.get("soundness", {})
    primary = result.get("primary_validity", {})
    secondary = result.get("secondary_validity", {})
    intercon = result.get("interconnection", {})
    is_coherent = soundness.get("result") == "coherent"
    is_aligned = primary.get("result") == "aligned"
    is_forged = secondary.get("quality") == "forged"
    is_untraced = secondary.get("quality") == "untraced"
    weight = intercon.get("total_weight", 0)
    if primary.get("result") == "unaligned":
        score += 15
        reasons.append("No structural truth patterns matched")
    elif is_aligned and is_forged:
        score += 10
        reasons.append("Uses truth patterns to legitimize forged source")
    elif is_aligned and weight >= 5:
        score += 10
        reasons.append("Uses truth patterns to legitimize coordinated content")
    if is_forged:
        score += 30
        reasons.append("Forged source detected")
    elif secondary.get("quality") == "unverified":
        score += 10
        reasons.append("Unverified source")
    elif is_untraced:
        score += 5
        reasons.append("No source trace")
    if weight >= 10:
        score += 30
        reasons.append("Highly coordinated (weight " + str(weight) + ")")
    elif weight >= 5:
        score += 20
        reasons.append("Coordinated (weight " + str(weight) + ")")
    elif weight >= 2:
        score += 10
        reasons.append("Weakly coordinated (weight " + str(weight) + ")")
    if is_coherent and (is_forged or weight >= 5 or primary.get("result") == "unaligned"):
        score += 10
        reasons.append("Coherent presentation of problematic content")
    score = min(score, 100)
    level = "critical" if score >= 70 else "high" if score >= 50 else "medium" if score >= 30 else "low" if score >= 10 else "minimal"
    return {"score": score, "level": level, "reasons": reasons}

def verify(text):
    soundness = check_soundness(text)
    primary = check_primary_validity(text)
    secondary = check_secondary_validity(text)
    intercon = check_interconnection(text)
    result = {"input": text, "soundness": soundness, "primary_validity": primary, "secondary_validity": secondary, "interconnection": intercon}
    result["severity"] = calculate_severity(result)
    return result

def verify_link_standalone(url):
    result = {"url": url, "source_check": check_secondary_validity(url), "domain_check": verify_domain(parse_url(url).get("domain", ""))}
    severity = 0
    reasons = []
    if result["source_check"].get("quality") == "forged":
        severity += 60
        reasons.append("Forged source detected")
    if result["domain_check"].get("type") == "forgery":
        severity += 30
        reasons.append("Domain is a known forgery")
    severity = min(severity, 100)
    level = "critical" if severity >= 70 else "high" if severity >= 50 else "medium" if severity >= 30 else "low" if severity >= 10 else "minimal"
    result["severity"] = {"score": severity, "level": level, "reasons": reasons}
    return result

def verify_mixed(mixed_data):
    result = {"components": {}, "total_severity": 0, "all_reasons": []}
    if mixed_data.get("text"):
        r = verify(mixed_data["text"])
        result["components"]["text"] = r
        result["total_severity"] = max(result["total_severity"], r["severity"]["score"])
        result["all_reasons"].extend(r["severity"]["reasons"])
    if mixed_data.get("link"):
        r = verify_link_standalone(mixed_data["link"])
        result["components"]["link"] = r
        result["total_severity"] = max(result["total_severity"], r["severity"]["score"])
        result["all_reasons"].extend(r["severity"]["reasons"])
    result["all_reasons"] = list(set(result["all_reasons"]))
    s = result["total_severity"]
    result["level"] = "critical" if s >= 70 else "high" if s >= 50 else "medium" if s >= 30 else "low" if s >= 10 else "minimal"
    return result

def veris_verify(content, content_type="text"):
    if content_type == "text":
        return {"content_type": "text", "verification": verify(content)}
    elif content_type == "link":
        return {"content_type": "link", "verification": verify_link_standalone(content)}
    elif content_type == "mixed":
        return {"content_type": "mixed", "verification": verify_mixed(content)}
    else:
        return {"error": "Unknown content type: " + content_type}

def veris_auto(content):
    if isinstance(content, str):
        if content.startswith("http://") or content.startswith("https://"):
            return veris_verify(content, "link")
        return veris_verify(content, "text")
    elif isinstance(content, dict):
        return veris_verify(content, "mixed")
    return veris_verify(content, "text")

def generate_proof_links(result):
    proofs = []
    v = result.get("verification", result)
    def extract(comp):
        found = []
        if "secondary_validity" in comp:
            sv = comp["secondary_validity"]
            for source in sv.get("found", []):
                domain = source.get("value", "")
                url = domain if domain.startswith("http") else "https://" + domain if domain else None
                trust = auto_trust_score(domain) if domain else {}
                found.append({"type": "source", "label": domain, "url": url, "trust_score": trust.get("score", 0), "trust_tier": trust.get("tier", "unknown"), "trust_label": trust.get("label", "Unknown"), "note": source.get("note", "")})
            for u in sv.get("urls", []):
                domain = u.get("domain", "")
                trust = auto_trust_score(domain) if domain else {}
                found.append({"type": "url_trace", "label": domain, "url": u.get("url"), "trust_score": trust.get("score", 0), "trust_tier": trust.get("tier", "unknown"), "trust_label": trust.get("label", "Unknown"), "forgery": u.get("forgery", False), "note": u.get("note", "")})
        if "source_check" in comp:
            sc = comp["source_check"]
            for source in sc.get("found", []):
                domain = source.get("value", "")
                url = domain if domain.startswith("http") else "https://" + domain if domain else None
                trust = auto_trust_score(domain) if domain else {}
                found.append({"type": "source", "label": domain, "url": url, "trust_score": trust.get("score", 0), "trust_tier": trust.get("tier", "unknown"), "trust_label": trust.get("label", "Unknown"), "note": source.get("note", "")})
        return found
    if "components" in v:
        for comp_name, comp_data in v["components"].items():
            if isinstance(comp_data, dict):
                proofs.extend(extract(comp_data))
    else:
        proofs.extend(extract(v))
    return proofs
