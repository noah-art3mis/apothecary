import re
import logging

from configs import MODEL, MODELS, PROMPT
from utils.estimate_costs import estimate_costs

import anthropic
from anthropic.types import Message, MessageParam
from dotenv import load_dotenv


def ai_cleanup(text: str) -> tuple[str, int]:

    prompt = get_prompt(text)
    model = get_model(MODEL)

    try:
        response = query_claude(model, prompt)
    except Exception as e:
        logging.warning(e)
        return e.__repr__(), 0

    completion = response.content[0].text
    answer = parse_completion(completion)
    costs = estimate_costs(response)

    return answer, costs


def get_prompt(snippet: str) -> str:
    return PROMPT.replace("{snippet}", snippet)


# @retry(tries=10, delay=1, backoff=2)
def query_claude(model: str, prompt: str) -> Message:
    load_dotenv()
    client = anthropic.Anthropic()

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        messages=get_messages(prompt),
    )
    return message


def get_messages(prompt: str) -> list[MessageParam]:
    message: MessageParam = {"role": "user", "content": prompt}
    return [message]


def parse_completion(completion: str) -> str:
    answer_pattern = r"<answer>(.*?)</answer>"
    answer_match = re.search(answer_pattern, completion, re.DOTALL)
    answer_text = answer_match.group(1).strip() if answer_match else "No answer found."
    return answer_text


def get_model(model_name: str) -> str:
    model = next((model["id"] for model in MODELS if model["name"] == model_name), None)
    if model is None:
        raise ValueError(f"Model {model_name} not found in {MODELS}.")
    return model
