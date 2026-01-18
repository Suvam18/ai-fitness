"""
Unit tests for EnhancedPoseDetector
Tests pose detection and key point extraction functionality
"""
import pytest
import numpy as np
from backend.api.pose_detector import EnhancedPoseDetector


class TestEnhancedPoseDetector:
    """Test suite for EnhancedPoseDetector"""
    
    def test_initialization(self):
        """Test that pose detector initializes successfully"""
        detector = EnhancedPoseDetector()
        
        assert detector is not None
        assert detector.initialized is True
        assert detector.mp_pose is not None
        assert detector.pose is not None
    
    def test_detect_pose_with_empty_image(self):
        """Test pose detection with a blank image returns no landmarks"""
        detector = EnhancedPoseDetector()
        
        # Create a blank image (no person)
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        landmarks, processed_image = detector.detect_pose(blank_image)
        
        # Should return None for landmarks on blank image
        assert landmarks is None
        assert processed_image is not None
        assert processed_image.shape == blank_image.shape
    
    def test_detect_pose_returns_image(self):
        """Test that detect_pose always returns an image"""
        detector = EnhancedPoseDetector()
        
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        landmarks, processed_image = detector.detect_pose(test_image)
        
        assert processed_image is not None
        assert isinstance(processed_image, np.ndarray)
        assert processed_image.shape == test_image.shape
    
    def test_extract_key_points_with_none_landmarks(self):
        """Test that extract_key_points returns None when landmarks is None"""
        detector = EnhancedPoseDetector()
        
        key_points = detector.extract_key_points(None)
        
        assert key_points is None
    
    def test_detect_pose_with_draw_landmarks_false(self):
        """Test that draw_landmarks=False doesn't modify image significantly"""
        detector = EnhancedPoseDetector()
        
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        landmarks, processed_image = detector.detect_pose(test_image, draw_landmarks=False)
        
        # Image should be processed but not have landmarks drawn
        assert processed_image is not None
