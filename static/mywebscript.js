"use strict";

async function detectEmotion() {
  const text = document.getElementById("textToAnalyze").value;
  const result = document.getElementById("result");
  result.textContent = "Analyzing...";
  try {
    const response = await fetch(
      `/emotionDetector?textToAnalyze=${encodeURIComponent(text)}`
    );
    result.textContent = await response.text();
  } catch (error) {
    result.textContent = "Unable to contact the server. Please try again.";
  }
}

document.getElementById("analyzeButton").addEventListener("click", detectEmotion);
