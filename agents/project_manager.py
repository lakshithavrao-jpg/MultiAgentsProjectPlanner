from llm import generate_response


def create_project_plan(project, requirements, architecture):

    system_prompt = """
    You are an experienced IT Project Manager.

    Create a practical project execution plan.

    Include:

    1. Project Development Phases
    2. Task Breakdown
    3. Task Dependencies
    4. Team Responsibilities
    5. Estimated Timeline
    6. Milestones
    7. Risk Management
    8. Testing Strategy
    9. Deployment Plan

    Divide tasks logically across the project duration.

    Make the timeline realistic for the available team size.
    """

    user_prompt = f"""
    PROJECT NAME:
    {project['name']}

    PROJECT DURATION:
    {project['duration']}

    TEAM SIZE:
    {project['team_size']}

    REQUIREMENTS:
    {requirements}

    SOFTWARE ARCHITECTURE:
    {architecture}
    """

    return generate_response(system_prompt, user_prompt)