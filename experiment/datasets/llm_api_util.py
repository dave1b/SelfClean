def generate_near_duplicate_mistral(
    text: str,
    model: str = "mistral-tiny",
    temperature: float = 0.3,
    max_tokens: int = 100
) -> str:
    """
    Generate a near-duplicate of the input text using Mistral's API.

    Args:
        text (str): Original text to paraphrase.
        model (str): Mistral model to use (e.g., "mistral-tiny", "mistral-small", "mistral-medium").
        temperature (float): Controls randomness (lower = more deterministic).
        max_tokens (int): Maximum number of tokens in the response.

    Returns:
        str: Near-duplicate text.
    """
    from mistralai import Mistral
    import os
    from dotenv import load_dotenv
    load_dotenv()  # Loads the .env file
    return "should be a near duplicate"

    prompt = f"""
          You are a text paraphraser. Your task is to generate a near-duplicate of the given text.
          The near-duplicate should:
          1. Preserve the original meaning.
          2. Make subtle changes (e.g., synonyms, rephrasing, minor restructuring).
          3. Avoid adding or removing major details.

          Original text:
          {text}

          Near-duplicate:
          """

    with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:
        res = mistral.chat.complete(model="mistral-small-latest", messages=[
            {
                "content": prompt,
                "role": "user",
            },
        ], stream=False)

        # Handle response
        return res.choices[-1].message.content
