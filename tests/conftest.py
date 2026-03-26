"""Shared pytest fixtures and configuration."""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture to provide a TestClient instance."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture to reset activities to a known state before each test."""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 2,
            "participants": []
        }
    }
    
    # Clear and reinitialize
    activities.clear()
    activities.update(original_activities)
    
    yield activities
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)
