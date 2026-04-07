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
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer training and league play",
        "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim practice, stroke improvement, and water fitness",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu", "jack@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and theatrical productions",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "harper@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare for debates and build public speaking skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["amelia@mergington.edu", "ethan@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science and engineering challenges",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["sophia@mergington.edu", "mason@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "bella@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis lessons and matches",
        "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["charlie@mergington.edu", "diana@mergington.edu"]
    },
    "Music Club": {
        "description": "Learn instruments and perform music",
        "schedule": "Fridays, 3:00 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["eve@mergington.edu", "frank@mergington.edu"]
    },
    "Photography Club": {
        "description": "Capture and edit photos",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["grace@mergington.edu", "henry@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve math problems and puzzles",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ivy@mergington.edu", "jack@mergington.edu"]
    },
    "History Club": {
        "description": "Study historical events and debates",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["kate@mergington.edu", "leo@mergington.edu"]
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
        raise HTTPException(status_code=400, detail="Student already signed up")    
    
    # Validate student is not already signed up
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full") 

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
