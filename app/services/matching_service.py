def compute_match_score(startup: dict, thesis: dict) -> dict:
    score = 0
    rationale = {}

    sector = 40 if startup.get("sector") == thesis.get("sector") else 0
    stage = 30 if startup.get("stage") == thesis.get("stage") else 0
    geography = 15 if startup.get("geography") == thesis.get("geography") else 0
    check_size = 15 if startup.get("check_size") == thesis.get("check_size") else 0

    rationale["sector"] = sector
    rationale["stage"] = stage
    rationale["geography"] = geography
    rationale["check_size"] = check_size

    score = sector + stage + geography + check_size
    return {"score": score, "rationale": rationale}
