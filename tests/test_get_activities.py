"""Tests for GET /activities endpoint using AAA pattern."""
import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """AAA: Should return all available activities."""
        # Arrange - fixtures provide pre-populated activities
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """AAA: Activity objects should have required fields."""
        # Arrange - no additional setup needed
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_get_activities_shows_current_participants(self, client, reset_activities):
        """AAA: Should display current participants."""
        # Arrange - Chess Club already has a participant from fixture
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert len(data["Chess Club"]["participants"]) == 1
