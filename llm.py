from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL


def get_client():

    if not GROQ_API_KEY:
        raise ValueError(
            "Groq API key is missing. "
            "Please configure GROQ_API_KEY in your .env file."
        )

    return Groq(api_key=GROQ_API_KEY)


def generate_response(system_prompt, user_prompt):

    client = get_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        max_completion_tokens=2000
    )

    return response.choices[0].message.content