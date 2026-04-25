import os
import anthropic

# The client reads ANTHROPIC_API_KEY from the environment automatically.
# Set it locally in a .env file or export it in your shell.
# On App Engine, add it to app.yaml under `env_variables`.
client = anthropic.Anthropic()

SYSTEM_PROMPT = (
    "You are a precise summarization assistant. "
    "When given a block of text, return a clear, concise summary in 3–5 sentences. "
    "Preserve the key facts, main argument, and any important conclusions. "
    "Do not add opinions or information that isn't in the source text."
)


def summarize_text(text: str) -> str:
    """
    Send `text` to the Anthropic Claude API and return a summary string.

    Args:
        text: The plain text content to summarize.

    Returns:
        A summary string from the model.

    Raises:
        anthropic.APIError: If the API call fails.
        ValueError: If the response contains no text content.
    """
    # Truncate very long inputs to stay within token limits.
    # Claude's context window is large, but for a summarizer 15k chars is plenty.
    MAX_CHARS = 15_000
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[Content truncated for length]"

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{text}",
            }
        ],
    )

    # Extract the text block from the response
    for block in message.content:
        if block.type == "text":
            return block.text.strip()

    raise ValueError("No text content returned by the API.")
