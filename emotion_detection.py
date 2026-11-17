"""Detect emotions in text with the Watson NLP EmotionPredict service."""

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyse):
    """Return emotion scores and the dominant emotion for a text."""
    empty_result = {emotion: None for emotion in EMOTIONS}
    empty_result["dominant_emotion"] = None

    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return empty_result

    payload = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(URL, headers=HEADERS, json=payload, timeout=20)

    if response.status_code == 400:
        return empty_result

    response.raise_for_status()
    api_data = response.json()
    api_scores = api_data["emotionPredictions"][0]["emotion"]
    scores = {emotion: api_scores[emotion] for emotion in EMOTIONS}
    scores["dominant_emotion"] = max(EMOTIONS, key=scores.get)
    return scores
