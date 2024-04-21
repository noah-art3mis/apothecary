from dotenv import load_dotenv
from retry import retry
import anthropic
from utils.estimate_costs import estimate_costs

MODEL = ""


def get_prompt(text):
    return f"<text>{text}</text>\n\n This text was transcribed by OCR. Your job is to fix obvious transcription errors, such as problems with word separation, punctuation, encoding. Output a concise log of changes in a <log> tag and then output the answer in a <answer> tag."


def ai_cleanup(text):
    messages = get_messages(text)
    response = query_claude(MODEL, messages)
    print(estimate_costs(response))
    return response.content[0].text


@retry(tries=10, delay=1, backoff=2)
def query_claude(model, messages):
    load_dotenv()
    client = anthropic.Anthropic()

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        messages=messages,
    )
    return message


def get_messages(prompt):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
            ],
        }
    ]
