"""Unit tests for Watson NLP emotion detection."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Check five emotions and invalid input responses."""

    def check_emotion(self, text, expected_emotion):
        """Mock Watson response and validate the dominant emotion."""
        scores = {
            "anger": 0.05,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.05,
            "sadness": 0.05,
        }
        scores[expected_emotion] = 0.80
        fake_response = Mock(status_code=200)
        fake_response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }
        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=fake_response,
        ) as post:
            result = emotion_detector(text)
        self.assertEqual(result["dominant_emotion"], expected_emotion)
        self.assertEqual(set(result), {
            "anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"
        })
        post.assert_called_once()

    def test_joy(self):
        """Test a joyful statement."""
        self.check_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Test an angry statement."""
        self.check_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Test a disgusted statement."""
        self.check_emotion("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """Test a sad statement."""
        self.check_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Test a fearful statement."""
        self.check_emotion("I am really afraid that this will happen", "fear")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, mock_post):
        """Check the return format for invalid Watson API input."""
        mock_post.return_value.status_code = 400
        result = emotion_detector("invalid")
        self.assertTrue(all(value is None for value in result.values()))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_input(self, mock_post):
        """Do not call Watson NLP if the text is blank."""
        result = emotion_detector("   ")
        self.assertTrue(all(value is None for value in result.values()))
        mock_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
