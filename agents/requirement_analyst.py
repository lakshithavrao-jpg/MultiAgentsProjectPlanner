from llm import generate_response


def analyze_requirements(project):

    system_prompt = """
    You are an expert Business Analyst and Requirement Analyst.

    Your responsibility is to analyse project ideas and convert
    them into structured software requirements.

    Generate:

    1. Problem Statement
    2. Project Objectives
    3. Functional Requirements
    4. Non-Functional Requirements
    5. User Roles
    6. Expected Features
    7. Project Scope
    8. Expected Outcomes

    Be specific, practical and technically accurate.
    Use clear headings and bullet points.
    """

    user_prompt = f"""
    PROJECT NAME: {project['name']}

    DESCRIPTION: {project['description']}

    DOMAIN: {project['domain']}

    COMPLEXITY: {project['complexity']}

    TEAM SIZE: {project['team_size']}

    DURATION: {project['duration']}

    TECHNOLOGIES: {project['technologies']}

    ADDITIONAL REQUIREMENTS:
    {project['additional_requirements']}
    """

    return generate_response(system_prompt, user_prompt)