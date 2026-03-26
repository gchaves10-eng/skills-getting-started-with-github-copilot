"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern."""
import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities."""
    
    def test_signup_successful(self, client, reset_activities):
        """AAA: Student should successfully sign up for an activity."""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email in reset_activities[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    def test_signup_duplicate_registration_fails(self, client, reset_activities):
        """AAA: Duplicate registration should return 400 error."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_fails(self, client, reset_activities):
        """AAA: Signup for non-existent activity should return 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "bob@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_activity_full_fails(self, client, reset_activities):
        """AAA: Signup for full activity should return 400."""
        # Arrange
        activity_name = "Chess Club"
        email1 = "bob@mergington.edu"
        email2 = "charlie@mergington.edu"
        
        # Fill the activity (max_participants = 2, but 1 already registered)
        reset_activities[activity_name]["participants"].append(email1)
        # Now at capacity
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response.status_code == 400
        assert "Activity is full" in response.json()["detail"]
    
    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """AAA: Multiple different students should be able to sign up."""
        # Arrange
        activity_name = "Programming Class"
        emails = ["alice@mergington.edu", "bob@mergington.edu"]
        
        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert
        participants = reset_activities[activity_name]["participants"]
        assert len(participants) == 2
        for email in emails:
            assert email in participants
