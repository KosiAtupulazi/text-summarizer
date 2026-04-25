import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Timeout for outbound HTTP requests (seconds)
REQUEST_TIMEOUT = 10

# Tags whose text content we want to extract
CONTENT_TAGS = ["p", "h1", "h2", "h3", "h4", "article", "section", "li"]

# Tags to strip entirely before extraction (nav, ads, scripts, etc.)
NOISE_TAGS = ["script", "style", "nav", "header", "footer", "aside", "form", "iframe"]


def scrape_url(url: str) -> str:
    """
    Fetch a web page at `url`, strip boilerplate, and return its readable text.

    Args:
        url: A fully-qualified URL (must include http:// or https://).

    Returns:
        A single string of extracted text content.

    Raises:
        ValueError: If the URL is invalid, the page returns an error status,
                    or no readable content could be extracted.
        requests.RequestException: For network-level errors (timeouts, DNS, etc.).
    """
    # Basic URL validation
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(
            f"Invalid URL '{url}'. Must start with http:// or https://."
        )

    headers = {
        # Mimic a real browser so sites don't block us outright
        "User-Agent": (
            "Mozilla/5.0 (compatible; TextSummarizerBot/1.0; "
            "+https://your-app.appspot.com)"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise ValueError(f"Request to '{url}' timed out after {REQUEST_TIMEOUT}s.")
    except requests.exceptions.ConnectionError:
        raise ValueError(f"Could not connect to '{url}'. Check the URL and try again.")

    if response.status_code != 200:
        raise ValueError(
            f"'{url}' returned HTTP {response.status_code}. Cannot scrape this page."
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noise tags in-place
    for tag in soup(NOISE_TAGS):
        tag.decompose()

    # Extract readable text from content tags
    chunks = []
    for tag in soup.find_all(CONTENT_TAGS):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            chunks.append(text)

    # Fall back to all body text if the targeted tags yielded nothing
    if not chunks and soup.body:
        chunks = [soup.body.get_text(separator=" ", strip=True)]

    full_text = "\n".join(chunks).strip()

    if not full_text:
        raise ValueError(f"No readable text content found at '{url}'.")

    return full_text
