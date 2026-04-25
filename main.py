import os
from flask import Flask, request, jsonify, render_template
from summarizer import summarize_text
from scraper import scrape_url

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize/text", methods=["POST"])
def summarize_plain_text():
    """
    Accepts plain text in the request body and returns an AI-generated summary.

    Request JSON:
        { "text": "your long text here..." }

    Response JSON:
        { "summary": "..." }
    """
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field in request body."}), 400

    raw_text = data["text"].strip()
    if not raw_text:
        return jsonify({"error": "'text' field cannot be empty."}), 400

    try:
        summary = summarize_text(raw_text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/summarize/url", methods=["POST"])
def summarize_from_url():
    """
    Accepts a URL, scrapes its text content, and returns an AI-generated summary.

    Request JSON:
        { "url": "https://example.com/article" }

    Response JSON:
        { "url": "...", "summary": "..." }
    """
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field in request body."}), 400

    url = data["url"].strip()
    if not url:
        return jsonify({"error": "'url' field cannot be empty."}), 400

    try:
        scraped_text = scrape_url(url)
        summary = summarize_text(scraped_text)
        return jsonify({"url": url, "summary": summary})
    except ValueError as e:
        # Raised by scraper for bad URLs or no content
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Local development only — App Engine uses gunicorn
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
