import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# API key: prefer the environment variable (safe for sharing the repo).
# For local-only use, you may paste your key into _LOCAL_GEMINI_API_KEY below.
# Never commit a real key to a public repository.
_LOCAL_GEMINI_API_KEY = ""

# Google retires model IDs often (gemini-1.5-flash → 404 on current API).
# Stable text model for generateContent — see https://ai.google.dev/gemini-api/docs/models/gemini
_DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"

api_key = (
    os.environ.get("GEMINI_API_KEY", "").strip() or _LOCAL_GEMINI_API_KEY.strip()
)
model = None
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(_DEFAULT_GEMINI_MODEL)


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        idea = request.form.get("idea", "").strip()
        if not idea:
            result = "Please enter a startup idea."
        elif model is None:
            result = (
                "Set GEMINI_API_KEY in your environment, or paste your key into "
                "_LOCAL_GEMINI_API_KEY in app.py for local use only, then restart the app."
            )
        else:
            prompt = f"""
        Generate:
        1. Startup Pitch
        2. Tagline
        3. Business Model
        4. Marketing Strategy

        Startup Idea: {idea}
        """
            try:
                response = model.generate_content(prompt)
                if not getattr(response, "candidates", None):
                    result = (
                        "No response was generated. Try rephrasing your idea "
                        "or check if the response was blocked by safety filters."
                    )
                else:
                    result = response.text or ""
            except Exception as exc:
                result = f"Could not generate content: {exc}"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
