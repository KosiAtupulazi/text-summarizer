# Text Summarizer — Flask + Anthropic + Google App Engine

A REST API that accepts plain text or a URL and returns an AI-generated summary using Claude.

---

## Project Structure

```
text-summarizer/
├── main.py              # Flask app + route definitions
├── summarizer.py        # Anthropic Claude API integration
├── scraper.py           # BeautifulSoup URL scraper
├── requirements.txt     # Python dependencies
├── app.yaml             # Google App Engine configuration
├── .gitignore
└── templates/
    └── index.html       # Simple browser UI
```
## Additional Improvements

- Enhanced UI styling for summary display
- Improved input validation and error handling
- Optimized user experience for better interaction
---

## Local Setup

### 1. Prerequisites
- Python 3.12+
- A Google Cloud project with App Engine enabled
- An Anthropic API key

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key
```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

### 5. Run locally
```bash
python main.py
```
Visit http://localhost:8080 in your browser.

---

## API Endpoints

### POST /summarize/text
Summarize plain text.

**Request:**
```json
{ "text": "Your long article or document content here..." }
```

**Response:**
```json
{ "summary": "Three to five sentence summary..." }
```

---

### POST /summarize/url
Scrape a URL and summarize its content.

**Request:**
```json
{ "url": "https://example.com/article" }
```

**Response:**
```json
{ "url": "https://example.com/article", "summary": "..." }
```

---

## Deploy to Google App Engine

### 1. Install the Google Cloud CLI
https://cloud.google.com/sdk/docs/install

### 2. Authenticate and set your project
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Add your API key to app.yaml
Open `app.yaml` and replace `YOUR_API_KEY_HERE` with your actual key.

> Security tip: For production, use Google Cloud Secret Manager instead of hardcoding
> the key in app.yaml. See: https://cloud.google.com/secret-manager/docs

### 4. Deploy
```bash
gcloud app deploy
```

### 5. Open the deployed app
```bash
gcloud app browse
```

---

## How It Works

```
Browser / API Client
       |
       v
  Flask (main.py)
   /summarize/text  ──>  summarizer.py  ──>  Anthropic Claude API
   /summarize/url   ──>  scraper.py (BeautifulSoup)
                              |
                              v
                         summarizer.py  ──>  Anthropic Claude API
```

1. Flask receives the POST request and validates input.
2. For text requests, the raw text is passed directly to the Anthropic API.
3. For URL requests, BeautifulSoup fetches and parses the page first, stripping
   nav/footer/script noise, then passes the clean text to the Anthropic API.
4. The Claude model returns a 3-5 sentence summary, which Flask sends back as JSON.
5. On Google App Engine, gunicorn serves the Flask app; App Engine handles
   auto-scaling, HTTPS, and infrastructure automatically.
