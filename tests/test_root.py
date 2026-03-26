"""Tests for GET / endpoint using AAA pattern."""


class TestRootEndpoint:
    """Test suite for root endpoint."""
    
    def test_root_redirects_to_index(self, client):
        """AAA: Root endpoint should redirect to static/index.html."""
        # Arrange - no setup needed
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]
