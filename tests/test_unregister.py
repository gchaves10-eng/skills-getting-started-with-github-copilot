"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern."""
import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities."""
    
    def test_unregister_successful(self, client, reset_activities):
        """AAA: Registered student should successfully unregister."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        assert email in reset_activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email not in reset_activities[activity_name]["participants"]
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    
    def test_unregister_not_registered_fails(self, client, reset_activities):
        """AAA: Unregistering non-registered student should return 400."""
        # Arrange
        activity_name = "Programming Class"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_nonexistent_activity_fails(self, client, reset_activities):
        """AAA: Unregister from non-existent activity should return 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "alice@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_freeslot_for_others(self, client, reset_activities):
        """AAA: Unregistering should free up a slot for new registrations."""
        # Arrange
        activity_name = "Chess Club"
        student1 = "michael@mergington.edu"
        student2 = "charlie@mergington.edu"
        # Fill the activity first
        reset_activities[activity_name]["participants"].append(student2)
        
        # Can't add more (activity full)
        response_full = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "dave@mergington.edu"}
        )
        assert response_full.status_code == 400
        
        # Act - unregister one student
        response_unregister = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student1}
        )
        
        # Assert - should now be able to signup again
        assert response_unregister.status_code == 200
        response_signup = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "dave@mergington.edu"}
        )
        assert response_signup.status_code == 200
