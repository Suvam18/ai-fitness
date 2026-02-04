"""
Integration test for quality feedback in analysis endpoint.

Verifies that the /api/v1/analyze endpoint properly integrates with
PoseQualityEvaluator to return quality scores and feedback messages.
"""
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)


def test_analysis_endpoint_returns_quality_feedback():
    """
    Test that analysis endpoint returns quality feedback fields.
    
    **Requirements: 2.1, 4.1, 4.2, 8.2, 8.3**
    - Verifies that quality_score, quality_category, real_time_feedback,
      and historical_average are included in the response
    """
    # First, create a session
    session_response = client.post(
        "/api/v1/sessions/start",
        json={"exercise_type": "bicep_curl"}
    )
    
    # Skip test if session manager not initialized
    if session_response.status_code == 503:
        pytest.skip("Session manager not initialized in test environment")
    
    assert session_response.status_code == 200
    session_data = session_response.json()
    session_id = session_data["session_id"]
    
    # Create sample key points for bicep curl
    key_points = {
        "right_shoulder": [0.5, 0.3, 0.0, 0.9],
        "right_elbow": [0.6, 0.5, 0.0, 0.9],
        "right_wrist": [0.7, 0.7, 0.0, 0.9],
        "left_shoulder": [0.4, 0.3, 0.0, 0.9],
        "left_elbow": [0.3, 0.5, 0.0, 0.9],
        "left_wrist": [0.2, 0.7, 0.0, 0.9],
        "right_hip": [0.5, 0.6, 0.0, 0.9],
        "left_hip": [0.4, 0.6, 0.0, 0.9],
        "right_knee": [0.5, 0.8, 0.0, 0.9],
        "left_knee": [0.4, 0.8, 0.0, 0.9],
        "right_ankle": [0.5, 1.0, 0.0, 0.9],
        "left_ankle": [0.4, 1.0, 0.0, 0.9]
    }
    
    # Send analysis request
    analysis_response = client.post(
        "/api/v1/analyze",
        json={
            "session_id": session_id,
            "exercise_type": "bicep_curl",
            "key_points": key_points
        }
    )
    
    assert analysis_response.status_code == 200
    analysis_data = analysis_response.json()
    
    # Verify quality feedback fields are present
    assert "quality_score" in analysis_data
    assert "quality_category" in analysis_data
    assert "real_time_feedback" in analysis_data
    assert "historical_average" in analysis_data
    
    # Verify quality score is in valid range
    assert 0 <= analysis_data["quality_score"] <= 100
    
    # Verify quality category is valid
    assert analysis_data["quality_category"] in ["poor", "average", "excellent"]
    
    # Verify feedback message is not empty
    assert len(analysis_data["real_time_feedback"]) > 0
    
    # Historical average should be present after first frame
    assert analysis_data["historical_average"] is not None
    assert 0 <= analysis_data["historical_average"] <= 100


def test_quality_feedback_updates_with_multiple_frames():
    """
    Test that quality feedback updates across multiple frames.
    
    **Requirements: 4.1, 8.2**
    - Verifies that historical average is calculated after multiple frames
    """
    # Create a session
    session_response = client.post(
        "/api/v1/sessions/start",
        json={"exercise_type": "squat"}
    )
    
    if session_response.status_code == 503:
        pytest.skip("Session manager not initialized in test environment")
    
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]
    
    # Sample key points for squat
    key_points = {
        "right_shoulder": [0.5, 0.2, 0.0, 0.9],
        "right_elbow": [0.6, 0.4, 0.0, 0.9],
        "right_wrist": [0.7, 0.5, 0.0, 0.9],
        "left_shoulder": [0.4, 0.2, 0.0, 0.9],
        "left_elbow": [0.3, 0.4, 0.0, 0.9],
        "left_wrist": [0.2, 0.5, 0.0, 0.9],
        "right_hip": [0.5, 0.5, 0.0, 0.9],
        "left_hip": [0.4, 0.5, 0.0, 0.9],
        "right_knee": [0.5, 0.7, 0.0, 0.9],
        "left_knee": [0.4, 0.7, 0.0, 0.9],
        "right_ankle": [0.5, 0.9, 0.0, 0.9],
        "left_ankle": [0.4, 0.9, 0.0, 0.9]
    }
    
    # Send multiple analysis requests
    quality_scores = []
    for _ in range(5):
        response = client.post(
            "/api/v1/analyze",
            json={
                "session_id": session_id,
                "exercise_type": "squat",
                "key_points": key_points
            }
        )
        assert response.status_code == 200
        data = response.json()
        quality_scores.append(data["quality_score"])
    
    # Verify historical average is calculated
    final_response = client.post(
        "/api/v1/analyze",
        json={
            "session_id": session_id,
            "exercise_type": "squat",
            "key_points": key_points
        }
    )
    
    assert final_response.status_code == 200
    final_data = final_response.json()
    
    # Historical average should be present
    assert final_data["historical_average"] is not None
    
    # Historical average should be reasonable (within range of scores)
    assert 0 <= final_data["historical_average"] <= 100


def test_quality_category_matches_score():
    """
    Test that quality category correctly reflects the quality score.
    
    **Requirements: 1.2, 1.3, 1.4, 1.5**
    - Verifies threshold-based categorization
    """
    # Create a session
    session_response = client.post(
        "/api/v1/sessions/start",
        json={"exercise_type": "push_up"}
    )
    
    if session_response.status_code == 503:
        pytest.skip("Session manager not initialized in test environment")
    
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]
    
    # Sample key points
    key_points = {
        "right_shoulder": [0.5, 0.3, 0.0, 0.9],
        "right_elbow": [0.6, 0.5, 0.0, 0.9],
        "right_wrist": [0.7, 0.6, 0.0, 0.9],
        "left_shoulder": [0.4, 0.3, 0.0, 0.9],
        "left_elbow": [0.3, 0.5, 0.0, 0.9],
        "left_wrist": [0.2, 0.6, 0.0, 0.9],
        "right_hip": [0.5, 0.5, 0.0, 0.9],
        "left_hip": [0.4, 0.5, 0.0, 0.9],
        "right_knee": [0.5, 0.7, 0.0, 0.9],
        "left_knee": [0.4, 0.7, 0.0, 0.9],
        "right_ankle": [0.5, 0.8, 0.0, 0.9],
        "left_ankle": [0.4, 0.8, 0.0, 0.9]
    }
    
    response = client.post(
        "/api/v1/analyze",
        json={
            "session_id": session_id,
            "exercise_type": "push_up",
            "key_points": key_points
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    quality_score = data["quality_score"]
    quality_category = data["quality_category"]
    
    # Verify category matches score thresholds
    # Default thresholds: poor < 60, average 60-85, excellent >= 85
    if quality_score < 60:
        assert quality_category == "poor"
    elif quality_score < 85:
        assert quality_category == "average"
    else:
        assert quality_category == "excellent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
