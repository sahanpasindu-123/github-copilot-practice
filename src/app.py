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

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities"
)

# Mount static files
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(current_dir, "static")),
    name="static"
)

# In-memory activity database
activities = {

    # ORIGINAL ACTIVITIES
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": [
            "michael@mergington.edu",
            "daniel@mergington.edu"
        ]
    },

    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": [
            "emma@mergington.edu",
            "sophia@mergington.edu"
        ]
    },

    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": [
            "john@mergington.edu",
            "olivia@mergington.edu"
        ]
    },

    # NEW SPORTS ACTIVITIES
    "Football Team": {
        "description": "Train and compete in football matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": []
    },

    "Basketball Team": {
        "description": "Practice basketball and compete in tournaments",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },

    # NEW ART ACTIVITIES
    "Art Club": {
        "description": "Explore painting, drawing, and creativity",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    },

    "Music Band": {
        "description": "Learn instruments and perform music",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 12,
        "participants": []
    },

    # NEW INTELLECTUAL ACTIVITIES
    "Math Club": {
        "description": "Solve math problems and participate in competitions",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },

    "Science Club": {
        "description": "Explore science experiments and projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
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

    # Check activity exists
    if activity_name not in activities:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    activity = activities[activity_name]

    # FIX 1: Prevent duplicate registration
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail=f"{email} is already registered for {activity_name}"
        )

    # FIX 2: Prevent over capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=400,
            detail=f"{activity_name} is already full"
        )

    # Add student safely
    activity["participants"].append(email)

    return {
        "message": f"Successfully signed up {email} for {activity_name}",
        "activity": activity_name,
        "total_participants": len(activity["participants"])
    }
