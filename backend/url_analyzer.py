from urllib.parse import urlparse
import re


SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "cutt.ly"
]


def analyze_url(url: str):

    original_url = url.strip()

    if not original_url.startswith(("http://", "https://")):
        url = "http://" + url
    else:
        url = original_url

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    score = 0
    signals = []

    # HTTP instead of HTTPS
    if parsed.scheme == "http":
        score += 20
        signals.append("No HTTPS")

    # URL shortener
    if domain in SHORTENERS:
        score += 25
        signals.append("URL shortener")

    # IP address instead of domain
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):
        score += 30
        signals.append("IP address used as domain")

    # Suspicious words
    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "payment",
        "refund",
        "reward",
        "kyc",
        "bank"
    ]

    for word in suspicious_words:
        if word in url.lower():
            score += 5
            signals.append(f"Suspicious keyword: {word}")

    # @ symbol
    if "@" in url:
        score += 25
        signals.append("@ symbol in URL")

    # Very long URL
    if len(url) > 100:
        score += 10
        signals.append("Unusually long URL")

    score = min(score, 100)

    if score >= 70:
        risk_level = "HIGH RISK"
    elif score >= 40:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"

    return {
        "url": original_url,
        "domain": domain,
        "risk_score": score,
        "risk_level": risk_level,
        "signals": signals
    }