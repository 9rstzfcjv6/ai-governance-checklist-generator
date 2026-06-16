from governance_data import GOVERNANCE_CONTROLS


def generate_checklist(ai_system_type):
    return GOVERNANCE_CONTROLS.get(ai_system_type, [])


def calculate_risk_counts(checklist):
    high_count = 0
    medium_count = 0
    low_count = 0

    for control in checklist:
        if control["risk_level"] == "High":
            high_count += 1
        elif control["risk_level"] == "Medium":
            medium_count += 1
        elif control["risk_level"] == "Low":
            low_count += 1

    return high_count, medium_count, low_count


def calculate_governance_score(checklist):
    score = 0

    for control in checklist:
        if control["risk_level"] == "High":
            score += 3
        elif control["risk_level"] == "Medium":
            score += 2
        elif control["risk_level"] == "Low":
            score += 1

    return score


def get_overall_governance_assessment(high_count, medium_count):
    if high_count >= 3:
        return "High governance attention required."

    if high_count >= 1:
        return "Targeted governance review recommended."

    if medium_count >= 1:
        return "Moderate governance controls recommended."

    return "Low governance concern based on current checklist."