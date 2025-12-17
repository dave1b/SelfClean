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

    prompt = f"""
    You are a text paraphraser. Your task is to generate a close near-duplicate of the given text.
    The near-duplicate needs to:
    1. Preserve the original meaning.
    2. Make only subtle changes (e.g., synonyms, rephrasing, minor restructuring).
    3. Avoid adding or removing details.
    4. Do not add any new information, even when sentences are incomplete.

    Return ONLY the paraphrased text, with no additional commentary:

    Original text:
    {text}
    """

    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY", ""))
    res = client.chat.complete(model="mistral-medium-2508", messages=[
        {
            "content": prompt,
            "role": "user",
        },
    ], stream=False)

    # Handle response
    return res.choices[-1].message.content.replace("\n", " ")
