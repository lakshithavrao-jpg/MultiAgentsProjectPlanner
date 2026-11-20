import streamlit as st
import json
import html
import re
from datetime import datetime
from pathlib import Path
from io import BytesIO

from config import GROQ_API_KEY, GROQ_MODEL, AGENTS_ASSETS_DIR
from workflow import generate_project
from database.db import (
    initialize_database,
    save_project,
    get_all_projects,
    get_project
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NEXUS | Agentic AI Project Command Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session():

    defaults = {
        "current_page": "Command Center",
        "navigation": "Command Center",
        "pending_navigation": None,
        "project": None,
        "results": None,
        "project_id": None,
        "agent_status": {},
        "generation_error": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session()


# ============================================================
# NAVIGATION
# ============================================================

PAGES = [
    "Command Center",
    "Create Project",
    "Agent Control Room",
    "Deliverables",
    "Project History"
]


def navigate_to(page):

    # This callback runs before Streamlit creates the widgets
    # during the next rerun.

    st.session_state.pending_navigation = page


def apply_pending_navigation():

    page = st.session_state.get("pending_navigation")

    if page:

        if page in PAGES:

            st.session_state.current_page = page

            # Update the radio key BEFORE creating the radio widget.
            st.session_state.navigation = page

        st.session_state.pending_navigation = None


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

try:
    initialize_database()
except Exception as error:
    st.error(f"Database initialization failed: {error}")


# ============================================================
# AGENT INFORMATION
# ============================================================

AGENTS = [
    {
        "name": "Requirement Analyst",
        "number": "01",
        "icon": "🔍",
        "file": "requirement_analyst.svg",
        "description": "Analyzes project requirements, objectives and scope."
    },
    {
        "name": "Software Architect",
        "number": "02",
        "icon": "🏗️",
        "file": "software_architect.svg",
        "description": "Designs system architecture and technology stack."
    },
    {
        "name": "Project Manager",
        "number": "03",
        "icon": "📊",
        "file": "project_manager.svg",
        "description": "Plans tasks, milestones, resources and timelines."
    },
    {
        "name": "Proposal Generator",
        "number": "04",
        "icon": "📄",
        "file": "proposal_generator.svg",
        "description": "Creates the final technical project proposal."
    }
]


# ============================================================
# CUSTOM CSS
# ============================================================

def load_css():

    st.markdown(
        """
        <style>

        @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #0B1020;
            color: #F1F5F9;
        }

        section[data-testid="stSidebar"] {
            background-color: #11182B;
            border-right: 1px solid #25304A;
        }

        section[data-testid="stSidebar"] * {
            color: #E2E8F0;
        }

        .main-title {
            font-size: 34px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 4px;
        }

        .subtitle {
            color: #94A3B8;
            font-size: 14px;
            margin-bottom: 25px;
        }

        .brand {
            font-size: 27px;
            font-weight: 800;
            color: #A78BFA;
            letter-spacing: 2px;
        }

        .brand-caption {
            color: #94A3B8;
            font-size: 10px;
            letter-spacing: 2px;
        }

        .glass-card {
            background: linear-gradient(
                135deg,
                #19233B,
                #141B30
            );
            border: 1px solid #2D3A58;
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 15px;
        }

        .metric-card {
            background: #151E34;
            border: 1px solid #2B3855;
            border-radius: 15px;
            padding: 20px;
            min-height: 125px;
        }

        .metric-label {
            color: #94A3B8;
            font-size: 13px;
        }

        .metric-value {
            color: #FFFFFF;
            font-size: 30px;
            font-weight: 800;
            margin-top: 10px;
        }

        .agent-card {
            background: #151E34;
            border: 1px solid #2B3855;
            border-radius: 15px;
            padding: 18px;
            min-height: 175px;
        }

        .agent-number {
            color: #A78BFA;
            font-size: 12px;
            font-weight: 700;
        }

        .agent-name {
            color: #FFFFFF;
            font-size: 17px;
            font-weight: 700;
            margin-top: 12px;
        }

        .agent-description {
            color: #94A3B8;
            font-size: 12px;
            margin-top: 8px;
        }

        .welcome-card {
            background: linear-gradient(
                110deg,
                #312E81,
                #4338CA,
                #155E75
            );
            border-radius: 18px;
            padding: 32px;
            margin: 15px 0 25px 0;
        }

        .welcome-title {
            font-size: 28px;
            font-weight: 800;
            color: white;
        }

        .welcome-text {
            color: #E0E7FF;
            font-size: 14px;
            margin-top: 10px;
        }

        .section-title {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 700;
            margin-top: 15px;
            margin-bottom: 15px;
        }

        .status-text {
            color: #94A3B8;
            font-size: 12px;
        }

        div.stButton > button {
            background: linear-gradient(
                90deg,
                #7C3AED,
                #4F46E5
            );
            color: white;
            border: none;
            border-radius: 9px;
            padding: 9px 18px;
            font-weight: 600;
            transition: 0.2s;
        }

        div.stButton > button:hover {
            border: 1px solid #A78BFA;
            color: white;
            background: #6D28D9;
        }

        div[data-testid="stForm"] {
            background: #141D32;
            border: 1px solid #2B3855;
            border-radius: 15px;
            padding: 22px;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] {
            background-color: #1B2740;
            color: white;
        }

        hr {
            border-color: #293650;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


load_css()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_text(value):

    if value is None:
        return ""

    return str(value)


def clean_filename(filename):

    filename = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        filename
    )

    return filename[:80]


def get_current_results():

    return st.session_state.get("results") or {}


def get_project_name():

    project = st.session_state.get("project") or {}

    return project.get(
        "project_name",
        project.get("name", "Untitled Project")
    )


def get_agent_status(agent_name):

    return st.session_state.agent_status.get(
        agent_name,
        "Not Started"
    )


def set_all_agents_status(status):

    st.session_state.agent_status = {
        agent["name"]: status
        for agent in AGENTS
    }


def format_output(value):

    if isinstance(value, dict):
        return json.dumps(value, indent=4, ensure_ascii=False)

    if isinstance(value, list):
        return json.dumps(value, indent=4, ensure_ascii=False)

    return safe_text(value)


# ============================================================
# SIDEBAR
# ============================================================

def show_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="brand">NEXUS</div>
            <div class="brand-caption">
                AGENTIC AI PROJECT COMMAND CENTER
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.caption("WORKSPACE NAVIGATION")

        # The pending navigation is applied before this widget
        # is created. Do not assign to navigation below this point.

        selected_page = st.radio(
            "Navigation",
            PAGES,
            key="navigation",
            label_visibility="collapsed"
        )

        st.session_state.current_page = selected_page

        st.markdown("---")

        st.caption("AI AGENT SYSTEM")

        st.markdown("🟢 Groq API")

        st.caption(f"Model: {GROQ_MODEL}")

        st.markdown("---")

        st.caption("NEXUS VERSION 1.0")

        st.caption("Powered by Agentic AI")


# ============================================================
# METRIC CARD
# ============================================================

def metric_card(label, value, icon):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                {icon} &nbsp; {html.escape(str(label))}
            </div>
            <div class="metric-value">
                {html.escape(str(value))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AGENT CARD
# ============================================================

def show_agent_card(agent):

    st.markdown(
        f"""
        <div class="agent-card">
            <div class="agent-number">
                AGENT {agent["number"]}
            </div>
            <div style="font-size:30px;margin-top:10px;">
                {agent["icon"]}
            </div>
            <div class="agent-name">
                {html.escape(agent["name"])}
            </div>
            <div class="agent-description">
                {html.escape(agent["description"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COMMAND CENTER
# ============================================================

def show_dashboard():

    st.markdown(
        '<div class="main-title">Command Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor your AI agents and manage project generation.'
        '</div>',
        unsafe_allow_html=True
    )

    try:
        projects = get_all_projects() or []
        total_projects = len(projects)
    except Exception:
        projects = []
        total_projects = 0

    completed_agents = sum(
        1 for agent in AGENTS
        if get_agent_status(agent["name"]) == "Completed"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("Total Projects", total_projects, "📁")

    with c2:
        metric_card("AI Agents", 4, "🤖")

    with c3:
        metric_card("Agents Completed", completed_agents, "✅")

    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">
                Welcome to NEXUS 🚀
            </div>
            <div class="welcome-text">
                Your intelligent multi-agent project planning
                workspace. Transform your ideas into structured
                technical project plans.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "＋  Start a New Project",
        key="dashboard_start_project",
        use_container_width=True
    ):
        navigate_to("Create Project")
        st.rerun()

    st.markdown(
        '<div class="section-title">Your AI Agent Team</div>',
        unsafe_allow_html=True
    )

    columns = st.columns(4)

    for index, agent in enumerate(AGENTS):

        with columns[index]:
            show_agent_card(agent)

    st.markdown(
        '<div class="section-title">Quick Actions</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button(
            "Create Project",
            key="quick_create",
            use_container_width=True
        ):
            navigate_to("Create Project")
            st.rerun()

    with q2:
        if st.button(
            "Explore Agents",
            key="quick_agents",
            use_container_width=True
        ):
            navigate_to("Agent Control Room")
            st.rerun()

    with q3:
        if st.button(
            "View Reports",
            key="quick_reports",
            use_container_width=True
        ):
            navigate_to("Deliverables")
            st.rerun()

    st.markdown(
        '<div class="section-title">Recent Projects</div>',
        unsafe_allow_html=True
    )

    try:

        if projects:

            for item in projects[-5:][::-1]:

                if isinstance(item, dict):

                    name = (
                        item.get("project_name")
                        or item.get("name")
                        or "Untitled Project"
                    )

                    created = item.get("created_at", "")

                elif isinstance(item, (tuple, list)):

                    name = item[1] if len(item) > 1 else "Project"
                    created = item[2] if len(item) > 2 else ""

                else:
                    name = str(item)
                    created = ""

                st.markdown(
                    f"""
                    <div class="glass-card">
                        <b>📁 {html.escape(str(name))}</b>
                        <div class="status-text">
                            {html.escape(str(created))}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.info("No projects have been generated yet.")

    except Exception as error:
        st.warning(f"Unable to load recent projects: {error}")


# ============================================================
# CREATE PROJECT
# ============================================================

def show_create_project():

    st.markdown(
        '<div class="main-title">Create New Project</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Provide your project details and let the four AI agents '
        'build your project plan.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("create_project_form"):

        st.markdown("### Project Information")

        project_name = st.text_input(
            "Project Name",
            placeholder="Example: Smart Campus Management System"
        )

        problem_statement = st.text_area(
            "Problem Statement",
            placeholder="Describe the problem your project will solve...",
            height=120
        )

        objectives = st.text_area(
            "Project Objectives",
            placeholder="Describe the main objectives...",
            height=100
        )

        additional_requirements = st.text_area(
            "Additional Requirements",
            placeholder="Mention any extra features or requirements...",
            height=100
        )

        col1, col2 = st.columns(2)

        with col1:

            domain = st.selectbox(
                "Project Domain",
                [
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Healthcare",
                    "Education",
                    "FinTech",
                    "Web Development",
                    "Data Science",
                    "Other"
                ]
            )

            level = st.selectbox(
                "Complexity Level",
                [
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ]
            )

            team_size = st.number_input(
                "Team Size",
                min_value=1,
                max_value=20,
                value=4
            )

        with col2:

            duration = st.selectbox(
                "Project Duration",
                [
                    "2 Weeks",
                    "4 Weeks",
                    "6 Weeks",
                    "8 Weeks",
                    "10 Weeks",
                    "12 Weeks",
                    "16 Weeks"
                ]
            )

            technologies = st.text_input(
                "Preferred Technologies",
                placeholder="Python, React, Flask, MongoDB"
            )

        submitted = st.form_submit_button(
            "🚀 Generate Project",
            use_container_width=True
        )

    if submitted:

        if not project_name.strip():
            st.error("Please enter a project name.")

        elif not problem_statement.strip():
            st.error("Please enter the problem statement.")

        else:

            # Important: This dictionary includes the keys
            # expected by the existing Requirement Analyst.

            project = {

                "name": project_name.strip(),

                "project_name": project_name.strip(),

                "problem_statement": problem_statement.strip(),

                "description": problem_statement.strip(),

                "objectives": objectives.strip(),

                "additional_requirements":
                    additional_requirements.strip(),

                "domain": domain,

                "complexity": level,

                "level": level,

                "difficulty": level,

                "team_size": int(team_size),

                "duration": duration,

                "technologies": technologies.strip()
            }

            st.session_state.project = project
            st.session_state.results = None
            st.session_state.project_id = None
            st.session_state.generation_error = None

            set_all_agents_status("Pending")

            st.markdown("---")

            st.markdown("### ⚡ Agent Workflow")

            try:

                with st.status(
                    "Starting the four-agent workflow...",
                    expanded=True
                ) as status:

                    st.write(
                        "🔍 Requirement Analyst is processing the project..."
                    )

                    st.session_state.agent_status[
                        "Requirement Analyst"
                    ] = "Running"

                    # Run the existing four-agent workflow.
                    results = generate_project(project)

                    # Mark agents completed after successful workflow.
                    for agent in AGENTS:

                        st.session_state.agent_status[
                            agent["name"]
                        ] = "Completed"

                    st.write("✅ Requirement Analyst completed.")
                    st.write("✅ Software Architect completed.")
                    st.write("✅ Project Manager completed.")
                    st.write("✅ Proposal Generator completed.")

                    st.session_state.results = results

                    status.update(
                        label="All four AI agents completed successfully!",
                        state="complete",
                        expanded=False
                    )

                # Save project and results in SQLite.

                try:

                    project_id = save_project(
                        project,
                        results
                    )

                    st.session_state.project_id = project_id

                except Exception as db_error:

                    st.warning(
                        "Project generated successfully, but "
                        f"database saving failed: {db_error}"
                    )

                st.success(
                    "Your project has been generated successfully!"
                )

                # Do not directly modify the navigation widget here.
                # Schedule navigation for the next rerun.

                navigate_to("Deliverables")
                st.rerun()

            except Exception as error:

                st.session_state.generation_error = str(error)

                st.error("Project generation failed.")

                st.exception(error)

                st.info(
                    "Check the missing fields expected by the "
                    "four agent modules if another KeyError occurs."
                )


# ============================================================
# AGENT CONTROL ROOM
# ============================================================

def show_agent_control_room():

    st.markdown(
        '<div class="main-title">Agent Control Room</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor the four specialized AI agents in NEXUS.'
        '</div>',
        unsafe_allow_html=True
    )

    for agent in AGENTS:

        status_value = get_agent_status(agent["name"])

        with st.container():

            st.markdown(
                f"""
                <div class="glass-card">
                    <h3>
                        {agent["icon"]} &nbsp;
                        {html.escape(agent["name"])}
                    </h3>
                    <p style="color:#94A3B8;">
                        {html.escape(agent["description"])}
                    </p>
                    <p>
                        <b>Status:</b>
                        {html.escape(status_value)}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.caption(
        "Agent statuses are updated after the workflow completes. "
        "This page does not display token-by-token live execution."
    )


# ============================================================
# DELIVERABLE CONTENT
# ============================================================

def get_deliverable_sections():

    results = get_current_results()

    return [
        ("Requirement Analysis", results.get("requirements", "")),
        ("Software Architecture", results.get("architecture", "")),
        ("Project Plan", results.get("project_plan", "")),
        ("Technical Project Proposal", results.get("proposal", ""))
    ]


def create_markdown_report():

    project = st.session_state.get("project") or {}

    sections = get_deliverable_sections()

    content = [
        f"# {get_project_name()}",
        "",
        "## Project Details",
        "",
        f"- **Domain:** {project.get('domain', '')}",
        f"- **Complexity:** {project.get('complexity', '')}",
        f"- **Team Size:** {project.get('team_size', '')}",
        f"- **Duration:** {project.get('duration', '')}",
        f"- **Technologies:** {project.get('technologies', '')}",
        "",
        "## Problem Statement",
        "",
        project.get("problem_statement", ""),
        "",
        "## Objectives",
        "",
        project.get("objectives", ""),
        "",
        "## Additional Requirements",
        "",
        project.get("additional_requirements", ""),
        ""
    ]

    for title, body in sections:

        content.extend([
            f"## {title}",
            "",
            format_output(body),
            ""
        ])

    return "\n".join(content)


# ============================================================
# PDF GENERATION
# ============================================================

def create_pdf_report():

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer
    )
    from reportlab.lib.units import inch

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "NexusTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#4338CA"),
        fontSize=22,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "NexusHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#4338CA"),
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "NexusBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        spaceAfter=8
    )

    story = []

    story.append(
        Paragraph(
            html.escape(get_project_name()),
            title_style
        )
    )

    project = st.session_state.get("project") or {}

    details = [
        ("Domain", project.get("domain", "")),
        ("Complexity", project.get("complexity", "")),
        ("Team Size", project.get("team_size", "")),
        ("Duration", project.get("duration", "")),
        ("Technologies", project.get("technologies", ""))
    ]

    story.append(
        Paragraph("Project Details", heading_style)
    )

    for label, value in details:

        story.append(
            Paragraph(
                f"<b>{html.escape(str(label))}:</b> "
                f"{html.escape(str(value))}",
                body_style
            )
        )

    sections = [
        ("Problem Statement", project.get("problem_statement", "")),
        ("Objectives", project.get("objectives", "")),
        (
            "Additional Requirements",
            project.get("additional_requirements", "")
        )
    ]

    sections.extend(get_deliverable_sections())

    for heading, body in sections:

        story.append(
            Paragraph(
                html.escape(str(heading)),
                heading_style
            )
        )

        safe_body = html.escape(format_output(body))
        safe_body = safe_body.replace("\n", "<br/>")

        story.append(
            Paragraph(
                safe_body,
                body_style
            )
        )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# DELIVERABLES PAGE
# ============================================================

def show_deliverables():

    st.markdown(
        '<div class="main-title">Project Deliverables</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View and download the outputs generated by your four AI agents.'
        '</div>',
        unsafe_allow_html=True
    )

    results = get_current_results()

    if not results:

        st.info("No generated deliverables are available yet.")

        if st.button(
            "Create a Project",
            key="deliverables_create"
        ):
            navigate_to("Create Project")
            st.rerun()

        return

    st.success(
        f"Deliverables for: {get_project_name()}"
    )

    sections = get_deliverable_sections()

    for title, content in sections:

        with st.expander(title, expanded=False):

            st.markdown(format_output(content))

    st.markdown("---")

    st.markdown("### Download Your Project")

    col1, col2 = st.columns(2)

    markdown_content = create_markdown_report()

    with col1:

        st.download_button(
            label="⬇ Download Markdown Report",
            data=markdown_content,
            file_name=(
                clean_filename(get_project_name())
                + "_report.md"
            ),
            mime="text/markdown",
            use_container_width=True
        )

    with col2:

        try:

            pdf_content = create_pdf_report()

            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_content,
                file_name=(
                    clean_filename(get_project_name())
                    + "_report.pdf"
                ),
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as error:

            st.error(f"PDF generation failed: {error}")


# ============================================================
# PROJECT HISTORY
# ============================================================

def open_saved_project(project_id):

    try:

        record = get_project(project_id)

        if not record:
            st.error("Project not found.")
            return

        if isinstance(record, dict):

            project = (
                record.get("project")
                or record.get("project_data")
                or record.get("project_details")
                or {}
            )

            results = record.get("results") or {}

        else:

            st.error(
                "Unexpected database record format. "
                "Please check database/db.py."
            )
            return

        if isinstance(project, str):
            project = json.loads(project)

        if isinstance(results, str):
            results = json.loads(results)

        st.session_state.project = project
        st.session_state.results = results
        st.session_state.project_id = project_id

        set_all_agents_status("Completed")

        navigate_to("Deliverables")
        st.rerun()

    except Exception as error:

        st.error(f"Unable to open project: {error}")


def show_project_history():

    st.markdown(
        '<div class="main-title">Project History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Access previously generated projects.'
        '</div>',
        unsafe_allow_html=True
    )

    try:

        projects = get_all_projects() or []

        if not projects:

            st.info("No saved projects found.")

            if st.button(
                "Create Your First Project",
                key="history_create"
            ):
                navigate_to("Create Project")
                st.rerun()

            return

        for index, item in enumerate(projects):

            if isinstance(item, dict):

                project_id = item.get("id")

                project_name = (
                    item.get("project_name")
                    or item.get("name")
                    or "Untitled Project"
                )

                created_at = item.get("created_at", "")

            elif isinstance(item, (tuple, list)):

                project_id = item[0] if len(item) > 0 else None

                project_name = (
                    item[1] if len(item) > 1 else "Untitled Project"
                )

                created_at = (
                    item[2] if len(item) > 2 else ""
                )

            else:

                continue

            with st.container():

                st.markdown(
                    f"""
                    <div class="glass-card">
                        <h4>
                            📁 {html.escape(str(project_name))}
                        </h4>
                        <div class="status-text">
                            Created: {html.escape(str(created_at))}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if project_id is not None:

                    if st.button(
                        "Open Project",
                        key=f"open_project_{project_id}_{index}"
                    ):

                        open_saved_project(project_id)

    except Exception as error:

        st.error(f"Unable to retrieve project history: {error}")


# ============================================================
# FOOTER
# ============================================================

def show_footer():

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#64748B;
            font-size:11px;
            padding:10px;
        ">
            NEXUS | AGENTIC AI PROJECT COMMAND CENTER
            <br>
            Powered by Groq and Multi-Agent AI
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    # Apply pending navigation BEFORE creating the sidebar radio.
    apply_pending_navigation()

    show_sidebar()

    page = st.session_state.current_page

    if page == "Command Center":

        show_dashboard()

    elif page == "Create Project":

        show_create_project()

    elif page == "Agent Control Room":

        show_agent_control_room()

    elif page == "Deliverables":

        show_deliverables()

    elif page == "Project History":

        show_project_history()

    show_footer()


if __name__ == "__main__":

    main()