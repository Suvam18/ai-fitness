"""
Integration test for no pose detected scenario
Tests that the API correctly handles empty key points and returns neutral feedback
"""
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)


def test_analyze_with_empty_key_points():
    """
    Test that analysis with empty key points returns neutral feedback.
    
    **Requirements: 5.4**
    - WHEN no pose is detected
      THEN the System SHALL display a neutral message prompting the user to enter the camera frame
    """
    # First create a session
    session_response = client.post(
        "/api/v1/sessions/start",
        json={"exercise_type": "bicep_curl"}
    )
    
    # Skip test if session manager not initialized
    if session_response.status_code == 503:
        pytest.skip("Session manager not initialized in test environment")
    
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]
    
    # Now analyze with empty key points (no pose detected)
    analysis_response = client.post(
        "/api/v1/analyze",
        json={
            "session_id": session_id,
            "exercise_type": "bicep_curl",
            "key_points": {}  # Empty key points
        }
    )
    
    assert analysis_response.status_code == 200
    data = analysis_response.json()
    
    # Should have quality feedback fields
    assert "quality_score" in data
    assert "quality_category" in data
    assert "real_time_feedback" in data
    
    # Quality score should be 0 for no pose
    assert data["quality_score"] == 0.0
    
    # Category should be poor
    assert data["quality_category"] == "poor"
    
    # Feedback should prompt user to step into frame
    assert "step into" in data["real_time_feedback"].lower() or \
           "camera frame" in data["real_time_feedback"].lower()


def test_analyze_with_missing_key_points():
    """
    Test that analysis with missing/invalid key points returns neutral scores.
    
    **Requirements: 6.3**
    - WHEN an exercise type is not configured
      THEN the System SHALL use default threshold values
    """
    # First create a session
    session_response = client.post(
        "/api/v1/sessions/start",
        json={"exercise_type": "squat"}
    )
    
    # Skip test if session manager not initialized
    if session_response.status_code == 503:
        pytest.skip("Session manager not initialized in test environment")
    
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]
    
    # Now analyze with invalid key points (all zeros)
    analysis_response = client.post(
        "/api/v1/analyze",
        json={
            "session_id": session_id,
            "exercise_type": "squat",
            "key_points": {
                "right_hip": [0, 0, 0, 0],
                "right_knee": [0, 0, 0, 0],
                "right_ankle": [0, 0, 0, 0],
                "right_shoulder": [0, 0, 0, 0]
            }
        }
    )
    
    assert analysis_response.status_code == 200
    data = analysis_response.json()
    
    # Should have quality feedback fields
    assert "quality_score" in data
    assert "quality_category" in data
    assert "real_time_feedback" in data
    
    # Quality score should be neutral (50.0) for missing key points
    assert data["quality_score"] == 50.0
    
    # Category should be poor (50 < 60 threshold)
    assert data["quality_category"] == "poor"
    
    # Should have some feedback message
    assert len(data["real_time_feedback"]) > 0


def test_analyze_with_valid_key_points_after_empty():
    """
    Test that valid key points work correctly after handling empty ones.
    
    Verifies that the system recovers properly from edge cases.
    """
    # First create a session
    session_response = client.post(
        "/api/v1/sessions/start",
        json={"exercise_type": "bicep_curl"}
    )
    
    # Skip test if session manager not initialized
    if session_response.status_code == 503:
        pytest.skip("Session manager not initialized in test environment")
    
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]
    
    # First analyze with empty key points
    empty_response = client.post(
        "/api/v1/analyze",
        json={
            "session_id": session_id,
            "exercise_type": "bicep_curl",
            "key_points": {}
        }
    )
    
    assert empty_response.status_code == 200
    empty_data = empty_response.json()
    assert empty_data["quality_score"] == 0.0
    
    # Now analyze with valid key points
    valid_response = client.post(
        "/api/v1/analyze",
        json={
            "session_id": session_id,
            "exercise_type": "bicep_curl",
            "key_points": {
                "right_shoulder": [0.5, 0.5, 0.5, 0.9],
                "right_elbow": [0.4, 0.6, 0.5, 0.9],
                "right_wrist": [0.3, 0.7, 0.5, 0.9]
            }
        }
    )
    
    assert valid_response.status_code == 200
    valid_data = valid_response.json()
    
    # Should have quality feedback
    assert "quality_score" in valid_data
    assert "quality_category" in valid_data
    assert "real_time_feedback" in valid_data
    
    # Quality score should be calculated (not 0 or necessarily 50)
    assert isinstance(valid_data["quality_score"], (int, float))
    assert 0.0 <= valid_data["quality_score"] <= 100.0
