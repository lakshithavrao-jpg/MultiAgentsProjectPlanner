from llm import generate_response


def design_architecture(project, requirements):

    system_prompt = """
    You are a Senior Software Architect.

    Your responsibility is to design a complete software
    architecture based on the project requirements.

    Generate:

    1. Architecture Overview
    2. Recommended Technology Stack
    3. Frontend Architecture
    4. Backend Architecture
    5. Database Design
    6. Main System Components
    7. Data Flow
    8. API Design
    9. Security Considerations
    10. Deployment Recommendations

    Explain how the components interact.

    Make the architecture suitable for the project complexity.
    """

    user_prompt = f"""
    PROJECT NAME:
    {project['name']}

    PROJECT DESCRIPTION:
    {project['description']}

    REQUIREMENT ANALYSIS:
    {requirements}

    PREFERRED TECHNOLOGIES:
    {project['technologies']}
    """

    return generate_response(system_prompt, user_prompt)