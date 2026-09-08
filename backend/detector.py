import re


SCAM_KEYWORDS = {
    "urgent": 12,
    "verify": 10,
    "verification": 10,
    "account blocked": 20,
    "account suspended": 20,
    "click": 8,
    "click here": 15,
    "otp": 15,
    "password": 10,
    "kyc": 18,
    "reward": 15,
    "winner": 15,
    "won": 10,
    "prize": 15,
    "cashback": 10,
    "lottery": 20,
    "bank": 8,
    "upi": 8,
    "payment": 8,
    "refund": 12,
    "fee": 8,
    "pay now": 18,
    "send money": 20,
    "limited time": 12,
}


def analyze_text(text: str):

    text_lower = text.lower()

    score = 0
    detected_signals = []

    for keyword, points in SCAM_KEYWORDS.items():
        if keyword in text_lower:
            score += points
            detected_signals.append(keyword)

    # URL detection
    urls = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        text_lower
    )

    if urls:
        score += 15
        detected_signals.append("suspicious link")

    # Phone number detection
    phones = re.findall(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    if phones:
        score += 5
        detected_signals.append("phone number")

    # Excessive urgency
    urgency_words = [
        "immediately",
        "right now",
        "urgent",
        "within 24 hours",
        "act now"
    ]

    for word in urgency_words:
        if word in text_lower:
            score += 10
            if word not in detected_signals:
                detected_signals.append(word)

    score = min(score, 100)

    if score >= 70:
        risk_level = "HIGH RISK"
        verdict = "Possible phishing/fraud"
    elif score >= 40:
        risk_level = "MEDIUM RISK"
        verdict = "Suspicious message"
    else:
        risk_level = "LOW RISK"
        verdict = "No major fraud signals detected"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "verdict": verdict,
        "signals": detected_signals
    }