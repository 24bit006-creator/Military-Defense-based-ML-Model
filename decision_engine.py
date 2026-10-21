import os
import joblib

TEXT_MODEL_PATH = os.path.join("models", "text_threat_pipeline.pkl")

def evaluate_threat(visual_class: str, visual_is_hostile: bool, visual_conf: float, dispatch_text: str):
    if not os.path.exists(TEXT_MODEL_PATH):
        from train_text_model import train
        train()

    text_pipeline = joblib.load(TEXT_MODEL_PATH)
    
    text_pred = text_pipeline.predict([dispatch_text])[0]
    text_probs = text_pipeline.predict_proba([dispatch_text])[0]
    
    text_is_hostile = bool(text_pred == 1)
    text_conf = float(text_probs[text_pred] * 100)
    text_class = "Hostile / Tactical Breach" if text_is_hostile else "Routine Dispatch"

    deception_detected = False
    
    if visual_is_hostile and not text_is_hostile:
        deception_detected = True
        status = "DECEPTION DETECTED: Visual confirms hostile combat asset while dispatch claims routine activity."
        threat_score = int(min(100, (visual_conf * 0.7) + 30))
        alert_level = "CRITICAL / SPOOFING"
        protocol = "Initiate perimeter lockdown. Scramble Quick Reaction Force (QRF). Hold checkpoint entry."
    elif visual_is_hostile and text_is_hostile:
        status = "CONFIRMED HOSTILE THREAT: Both visual reconnaissance and dispatch agree on high threat level."
        threat_score = int((visual_conf + text_conf) / 2)
        alert_level = "RED ALERT (HOSTILE)"
        protocol = "Engage counter-threat protocols. Designate sector hostile. Alert battalion command."
    elif not visual_is_hostile and text_is_hostile:
        status = "INVESTIGATION REQUIRED: Suspicious field text but visual asset appears standard/non-combat."
        threat_score = int(max(text_conf * 0.6, 50))
        alert_level = "WARNING (ELEVATED)"
        protocol = "Halt vehicle at perimeter barrier. Deploy secondary manual inspection and ID verification."
    else:
        status = "ALL CLEAR: Routine friendly/supply asset confirmed by dispatch and imagery."
        threat_score = int(max(10, 100 - ((visual_conf + text_conf) / 2)))
        alert_level = "NORMAL / ROUTINE"
        protocol = "Grant standard sector transit authorization and log checkpoint clearance."

    return {
        "visual_class": visual_class,
        "visual_confidence": round(visual_conf, 2),
        "visual_is_hostile": visual_is_hostile,
        "text_class": text_class,
        "text_confidence": round(text_conf, 2),
        "text_is_hostile": text_is_hostile,
        "threat_score": threat_score,
        "alert_level": alert_level,
        "status": status,
        "deception_detected": deception_detected,
        "protocol": protocol
    }
