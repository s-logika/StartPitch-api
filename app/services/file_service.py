def normalize_pitch_payload(payload: dict) -> dict:
    return {
        "title": payload.get("title"),
        "summary": payload.get("summary"),
        "content_url": payload.get("content_url"),
        "input_type": payload.get("input_type", "form"),
    }
