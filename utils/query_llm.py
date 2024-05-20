import re
import logging
from dotenv import load_dotenv
import anthropic
from openai import OpenAI

from utils.my_types import Model
from configs import MODEL, MODELS, PROMPT
from utils.estimate_costs import estimate_costs


def ai_cleanup(text: str) -> tuple[str, float]:
    load_dotenv()

    model = get_model(MODEL)

    if model.provider == "anthropic":
        return ai_cleanup_anthropic(text)
    if model.provider == "openai":
        return ai_cleanup_openai(text)

    raise ValueError(f"Unknown model provider: {model.provider}")


def ai_cleanup_openai(text: str) -> tuple[str, float]:

    prompt = get_prompt(text)
    model = get_model(MODEL)

    try:
        response = query_gpt(model.id, prompt)
    except Exception as e:
        logging.warning(e)
        return e.__repr__(), 0

    completion = response.choices[0].message.content
    answer = parse_completion(completion)
    costs = estimate_costs(response)

    return answer, costs


# @retry(tries=10, delay=1, backoff=2)
def query_gpt(model: str, prompt: str):
    client = OpenAI()

    message = client.chat.completions.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        messages=get_messages(prompt),  # type: ignore
    )
    return message


def ai_cleanup_anthropic(text: str) -> tuple[str, float]:

    prompt = get_prompt(text)
    model = get_model(MODEL)

    try:
        response = query_claude(model.id, prompt)
    except Exception as e:
        logging.warning(e)
        return e.__repr__(), 0

    completion = response.content[0].text
    answer = parse_completion(completion)
    costs = estimate_costs(response)

    return answer, costs


# @retry(tries=10, delay=1, backoff=2)
def query_claude(model: str, prompt: str):
    client = anthropic.Anthropic()

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        messages=get_messages(prompt),  # type: ignore
    )
    return message


def get_prompt(snippet: str) -> str:
    return PROMPT.replace("{snippet}", snippet)


def get_messages(prompt: str):
    message = {"role": "user", "content": prompt}
    return [message]


def parse_completion(completion) -> str:
    answer_pattern = r"<answer>(.*?)</answer>"
    answer_match = re.search(answer_pattern, completion, re.DOTALL)
    answer_text = answer_match.group(1).strip() if answer_match else "No answer found."
    return answer_text


def get_model(model_name: str) -> Model:
    model = next((model for model in MODELS if model.name == model_name), None)
    if model is None:
        raise ValueError(f"Model {model_name} not found in MODELS.")
    return model
