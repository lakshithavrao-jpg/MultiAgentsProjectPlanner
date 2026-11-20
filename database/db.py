import sqlite3
import json

from config import DATABASE_PATH


def get_connection():

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            project_name TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            project_data TEXT,

            results TEXT

        )
    """)

    connection.commit()
    connection.close()


def save_project(project, results):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO projects (
            project_name,
            project_data,
            results
        )
        VALUES (?, ?, ?)
    """, (
        project["name"],
        json.dumps(project),
        json.dumps(results)
    ))

    project_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return project_id


def get_all_projects():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, project_name, created_at
        FROM projects
        ORDER BY id DESC
    """)

    projects = cursor.fetchall()

    connection.close()

    return projects


def get_project(project_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM projects
        WHERE id = ?
    """, (project_id,))

    project = cursor.fetchone()

    connection.close()

    if project:

        return {
            "id": project[0],
            "name": project[1],
            "created_at": project[2],
            "project_data": json.loads(project[3]),
            "results": json.loads(project[4])
        }

    return None