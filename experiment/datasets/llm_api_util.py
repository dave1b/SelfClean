def generate_near_duplicate_mistral(
    text: str,
    model: str = "mistral-large-2512",
) -> str:
    """
    Generate a near-duplicate of the input text using Mistral's API.

    Args:
        text (str): Original text to paraphrase.
        model (str): Mistral model to use (e.g., "mistral-tiny", "mistral-small", "mistral-medium").

    Returns:
        str: Near-duplicate text.
    """
    from mistralai import Mistral
    import os
    from dotenv import load_dotenv
    load_dotenv()  # Loads the .env file

    prompt = f"""
    You are a text paraphraser. Your task is to generate a near-duplicate of the given text, adhering strictly to the following rules:

    1. The paraphrased text must retain the exact original meaning.
    2. Make only subtle changes (e.g. synonyms, minor restructuring).
    3. Do not add or remove any information, even if sentences are incomplete or ambiguous.
    5. Only use special characters (e.g., brackets, symbols, punctuation marks) that exist in the original text. Do not introduce new ones!
    6. Keep artefacts suche as [step] or [header] in the near-duplicate text.

    Return ONLY the paraphrased text, with no additional commentary:

    Original text:
    {text}
    """

    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY", ""))
    res = client.chat.complete(model=model, messages=[
        {
            "content": prompt,
            "role": "user",
        },
    ], stream=False)

    # Handle response
    return res.choices[-1].message.content.replace("\n", " ")
