"""Flask web application for text emotion detection."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the emotion detector interface."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    """Analyze text passed in the textToAnalyze query parameter."""
    text_to_analyse = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text_to_analyse)
    except (RequestException, KeyError, ValueError, IndexError) as error:
        app.logger.error("Emotion detection failed: %s", error)
        return "Emotion detection service is temporarily unavailable.", 502

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
