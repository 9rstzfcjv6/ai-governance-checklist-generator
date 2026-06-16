AI_SYSTEM_TYPES = [
    "Internal productivity AI tool",
    "Medical AI system",
    "HR / recruitment AI system",
    "Customer-facing chatbot",
    "Automated decision system",
    "Data analytics / prediction system"
]


GOVERNANCE_CONTROLS = {
    "Internal productivity AI tool": [
        {
            "category": "Data Governance",
            "control_objective": "Ensure that internal data used by the AI tool is appropriate and does not include unnecessary sensitive information.",
            "recommended_control": "Define clear rules on which internal documents, personal data and confidential information may be used with the AI tool.",
            "risk_level": "Medium",
            "owner": "Legal / IT / Data Governance Team",
            "priority": "Important"
        },
        {
            "category": "User Training",
            "control_objective": "Ensure employees understand the limitations and risks of using AI tools for internal work.",
            "recommended_control": "Provide internal guidance on acceptable AI use, prohibited inputs and review of AI-generated outputs.",
            "risk_level": "Medium",
            "owner": "Legal / HR / Compliance Team",
            "priority": "Important"
        },
        {
            "category": "Confidentiality",
            "control_objective": "Prevent confidential company information from being exposed to external AI systems.",
            "recommended_control": "Prohibit users from entering trade secrets, unpublished product information, source code or sensitive business data into unauthorized AI tools.",
            "risk_level": "High",
            "owner": "Legal / Security Team",
            "priority": "Urgent"
        }
    ],

    "Medical AI system": [
        {
            "category": "Data Governance",
            "control_objective": "Ensure that training, validation and testing datasets are traceable, representative and properly governed.",
            "recommended_control": "Document dataset provenance, quality checks, labeling process, representativeness and data access controls.",
            "risk_level": "High",
            "owner": "Data Governance / R&D / Legal Team",
            "priority": "Urgent"
        },
        {
            "category": "Human Oversight",
            "control_objective": "Ensure that clinical or medical AI outputs remain subject to appropriate human review.",
            "recommended_control": "Define the role of qualified human reviewers, escalation rules and limits on automated recommendations.",
            "risk_level": "High",
            "owner": "Clinical / Product / Legal Team",
            "priority": "Urgent"
        },
        {
            "category": "Documentation",
            "control_objective": "Maintain technical and governance documentation supporting development, validation and deployment.",
            "recommended_control": "Maintain model cards, validation reports, risk assessments, intended-use documentation and change logs.",
            "risk_level": "High",
            "owner": "R&D / Regulatory / Legal Team",
            "priority": "Urgent"
        },
        {
            "category": "Monitoring",
            "control_objective": "Monitor system performance after deployment to identify drift, errors or unsafe outputs.",
            "recommended_control": "Implement post-market monitoring, incident reporting, performance review and model update procedures.",
            "risk_level": "High",
            "owner": "Product / Quality / Regulatory Team",
            "priority": "Urgent"
        }
    ],

    "HR / recruitment AI system": [
        {
            "category": "Bias / Fairness",
            "control_objective": "Reduce the risk of discriminatory outcomes in hiring or employment-related decisions.",
            "recommended_control": "Test the system for bias, document evaluation results and require human review before employment decisions.",
            "risk_level": "High",
            "owner": "HR / Legal / Compliance Team",
            "priority": "Urgent"
        },
        {
            "category": "Transparency",
            "control_objective": "Ensure candidates and employees receive appropriate information about AI use.",
            "recommended_control": "Provide clear notices explaining where AI is used, what role it plays and how human review can be requested.",
            "risk_level": "High",
            "owner": "HR / Legal Team",
            "priority": "Urgent"
        },
        {
            "category": "Human Oversight",
            "control_objective": "Prevent fully automated employment decisions without appropriate review.",
            "recommended_control": "Require human validation before rejecting candidates, ranking applicants or making employment-related decisions.",
            "risk_level": "High",
            "owner": "HR / Legal Team",
            "priority": "Urgent"
        }
    ],

    "Customer-facing chatbot": [
        {
            "category": "Transparency",
            "control_objective": "Ensure users understand that they are interacting with an AI system.",
            "recommended_control": "Display a clear notice that the chatbot is AI-generated and may produce inaccurate or incomplete outputs.",
            "risk_level": "Medium",
            "owner": "Product / Legal / UX Team",
            "priority": "Important"
        },
        {
            "category": "Content Safety",
            "control_objective": "Reduce the risk of harmful, misleading or inappropriate chatbot outputs.",
            "recommended_control": "Define prohibited response categories, escalation rules, fallback responses and human support channels.",
            "risk_level": "High",
            "owner": "Product / Trust & Safety / Legal Team",
            "priority": "Urgent"
        },
        {
            "category": "Data Protection",
            "control_objective": "Limit the collection and processing of personal data through chatbot interactions.",
            "recommended_control": "Avoid collecting unnecessary personal data and provide clear instructions not to submit sensitive information.",
            "risk_level": "High",
            "owner": "Privacy / Legal / Product Team",
            "priority": "Urgent"
        }
    ],

    "Automated decision system": [
        {
            "category": "Human Oversight",
            "control_objective": "Ensure meaningful human control over decisions that materially affect individuals.",
            "recommended_control": "Define review, appeal and override mechanisms for decisions produced or supported by the AI system.",
            "risk_level": "High",
            "owner": "Legal / Compliance / Business Team",
            "priority": "Urgent"
        },
        {
            "category": "Explainability",
            "control_objective": "Ensure decisions can be explained at an appropriate level to users, regulators or internal reviewers.",
            "recommended_control": "Document key decision factors, model limitations and explanation procedures.",
            "risk_level": "High",
            "owner": "Data Science / Legal / Compliance Team",
            "priority": "Urgent"
        },
        {
            "category": "Accountability",
            "control_objective": "Clarify responsibility for system deployment, review and decision outcomes.",
            "recommended_control": "Assign internal owners for system governance, decision review, incident handling and periodic assessment.",
            "risk_level": "High",
            "owner": "Business / Legal / Compliance Team",
            "priority": "Urgent"
        }
    ],

    "Data analytics / prediction system": [
        {
            "category": "Data Governance",
            "control_objective": "Ensure input data is accurate, relevant and appropriately governed.",
            "recommended_control": "Document data sources, data quality checks, access rights and limitations of the dataset.",
            "risk_level": "Medium",
            "owner": "Data / Legal / Business Team",
            "priority": "Important"
        },
        {
            "category": "Model Monitoring",
            "control_objective": "Detect performance degradation, drift or unreliable predictions over time.",
            "recommended_control": "Implement periodic model performance review, drift monitoring and update procedures.",
            "risk_level": "Medium",
            "owner": "Data Science / Product Team",
            "priority": "Important"
        },
        {
            "category": "Business Use Limitation",
            "control_objective": "Prevent predictions from being used outside their validated context.",
            "recommended_control": "Define permitted use cases, prohibited uses and escalation rules for high-impact decisions.",
            "risk_level": "Medium",
            "owner": "Business / Legal / Product Team",
            "priority": "Important"
        }
    ]
}