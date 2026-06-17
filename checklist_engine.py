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

def get_governance_maturity_level(completion_rate):
    if completion_rate <= 25:
        return "Initial / Low Maturity"

    if completion_rate <= 50:
        return "Developing"

    if completion_rate <= 75:
        return "Managed"

    return "Mature"

def get_action_plan_recommendations(governance_maturity_level):
    if governance_maturity_level == "Initial / Low Maturity":
        return [
            "Prioritize urgent and high-risk governance controls before deployment or external use.",
            "Assign clear control owners across Legal, Compliance, Product, Data and R&D teams.",
            "Create a baseline AI system inventory and document current governance gaps.",
            "Define minimum internal rules for data use, human oversight and documentation."
        ]

    if governance_maturity_level == "Developing":
        return [
            "Formalize internal AI governance procedures and approval workflows.",
            "Start collecting evidence of control implementation for future audits or reviews.",
            "Improve documentation around data sources, model limitations, intended use and human review.",
            "Define escalation paths for incidents, unexpected outputs or high-risk use cases."
        ]

    if governance_maturity_level == "Managed":
        return [
            "Strengthen audit trails and periodic review processes.",
            "Establish recurring cross-functional AI governance meetings.",
            "Monitor performance, bias, security and operational risks over time.",
            "Prepare governance documentation for external due diligence or regulatory review."
        ]

    if governance_maturity_level == "Mature":
        return [
            "Move toward continuous monitoring of AI governance KPIs.",
            "Benchmark governance controls against emerging standards and sector practices.",
            "Prepare for external assurance, certification or independent review where relevant.",
            "Use governance data to support strategic AI deployment and risk-based scaling."
        ]

    return [
        "Review the AI system governance profile and define next-step actions based on risk level and implementation status."
    ]

def identify_governance_gap(control, implementation_status):
    risk_level = control["risk_level"]
    priority = control["priority"]

    if implementation_status == "Not Applicable":
        return "Not applicable"

    if risk_level == "High" and implementation_status == "Not Started":
        return "Critical governance gap"

    if priority == "Urgent" and implementation_status == "Not Started":
        return "Immediate action required"

    if risk_level == "High" and implementation_status == "In Progress":
        return "Active remediation needed"

    if risk_level == "Medium" and implementation_status == "Not Started":
        return "Planned governance improvement"

    if implementation_status == "Implemented":
        return "Control implemented"

    if implementation_status == "In Progress":
        return "Implementation in progress"

    return "Governance review recommended"