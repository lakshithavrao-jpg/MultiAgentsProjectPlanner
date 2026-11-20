from agents.requirement_analyst import analyze_requirements
from agents.software_architect import design_architecture
from agents.project_manager import create_project_plan
from agents.proposal_generator import generate_proposal


def generate_project(project, progress_callback=None):

    results = {}

    agents = [
        "Requirement Analyst",
        "Software Architect",
        "Project Manager",
        "Proposal Generator"
    ]

    def update_progress(agent_name, status):

        if progress_callback:
            progress_callback(agent_name, status)

    # AGENT 1
    update_progress(agents[0], "Processing")

    results["requirements"] = analyze_requirements(project)

    update_progress(agents[0], "Completed")

    # AGENT 2
    update_progress(agents[1], "Processing")

    results["architecture"] = design_architecture(
        project,
        results["requirements"]
    )

    update_progress(agents[1], "Completed")

    # AGENT 3
    update_progress(agents[2], "Processing")

    results["project_plan"] = create_project_plan(
        project,
        results["requirements"],
        results["architecture"]
    )

    update_progress(agents[2], "Completed")

    # AGENT 4
    update_progress(agents[3], "Processing")

    results["proposal"] = generate_proposal(
        project,
        results["requirements"],
        results["architecture"],
        results["project_plan"]
    )

    update_progress(agents[3], "Completed")

    return results