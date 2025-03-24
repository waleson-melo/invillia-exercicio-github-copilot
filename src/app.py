"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Aprenda estratégias e participe de torneios de xadrez",
        "schedule": "Sextas-feiras, 15:30 - 17:00",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Aprenda fundamentos de programação e desenvolva projetos de software",
        "schedule": "Terças e Quintas-feiras, 15:30 - 16:30",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Educação física e atividades esportivas",
        "schedule": "Segundas, Quartas e Sextas-feiras, 14:00 - 15:00",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Treinamento e competições de futebol",
        "schedule": "Terças e Quintas-feiras, 16:00 - 17:30",
        "max_participants": 25,
        "participants": []
    },
    "Basketball Team": {
        "description": "Treinamento e competições de basquete",
        "schedule": "Segundas e Quartas-feiras, 16:00 - 17:30",
        "max_participants": 20,
        "participants": []
    },
    "Art Class": {
        "description": "Aulas de desenho e pintura",
        "schedule": "Quartas-feiras, 15:00 - 16:30",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Atuação e produção de peças teatrais",
        "schedule": "Sextas-feiras, 16:00 - 17:30",
        "max_participants": 20,
        "participants": []
    },
    "Math Club": {
        "description": "Resolução de problemas matemáticos e competições",
        "schedule": "Terças-feiras, 15:00 - 16:00",
        "max_participants": 15,
        "participants": []
    },
    "Science Club": {
        "description": "Experimentos e projetos científicos",
        "schedule": "Quintas-feiras, 15:00 - 16:30",
        "max_participants": 15,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
