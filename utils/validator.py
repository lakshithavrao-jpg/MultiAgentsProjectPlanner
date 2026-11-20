def validate_project(project):

    errors = []

    if not project.get("name", "").strip():
        errors.append("Project name is required.")

    if not project.get("description", "").strip():
        errors.append("Project description is required.")

    if not project.get("domain"):
        errors.append("Project domain is required.")

    if project.get("team_size", 0) < 1:
        errors.append("Team size must be at least 1.")

    if not project.get("duration"):
        errors.append("Project duration is required.")

    return errors