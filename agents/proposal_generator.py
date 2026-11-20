from llm import generate_response


def generate_proposal(
    project,
    requirements,
    architecture,
    project_plan
):

    system_prompt = """
    You are a professional Technical Project Proposal Writer.

    Your responsibility is to combine the outputs of the
    previous three AI agents into one complete project proposal.

    Generate:

    1. Project Title
    2. Executive Summary
    3. Introduction
    4. Problem Statement
    5. Project Objectives
    6. Proposed Solution
    7. Functional Requirements
    8. Non-Functional Requirements
    9. Technical Architecture
    10. Technology Stack
    11. Implementation Methodology
    12. Project Timeline
    13. Expected Results
    14. Conclusion

    Maintain consistency between all sections.

    The proposal should be professional, detailed and
    suitable for an academic or software development project.
    """

    user_prompt = f"""
    PROJECT DETAILS:
    {project}

    REQUIREMENT ANALYSIS:
    {requirements}

    SOFTWARE ARCHITECTURE:
    {architecture}

    PROJECT MANAGEMENT PLAN:
    {project_plan}
    """

    return generate_response(system_prompt, user_prompt)