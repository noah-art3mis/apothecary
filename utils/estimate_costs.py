import logging
from configs import MODELS
from utils.my_types import Model


def find_model_record(target_id) -> Model | None:
    for model in MODELS:
        if target_id.startswith(model.id):
            return model
    return None


def estimate_costs(response) -> float:
    per_million_tokens = 1_000_000

    model = find_model_record(response.model)

    if model is None:
        logging.warning(f"Model not found: {response.model}; skipping cost estimation")
        return 0

    i_tokens = 0
    o_tokens = 0

    if model.provider == "openai":
        i_tokens = response.usage.prompt_tokens
        o_tokens = response.usage.completion_tokens
    if model.provider == "anthropic":
        i_tokens = response.usage.input_tokens
        o_tokens = response.usage.output_tokens

    i_cost = model.input_cost * i_tokens / per_million_tokens
    o_cost = model.output_cost * o_tokens / per_million_tokens
    cost = i_cost + o_cost

    logging.info(
        f"Model: {model.name} | Tokens: {i_tokens + o_tokens} ({i_tokens}+{o_tokens}) | Cost: ${cost:.4f}"
    )
    return cost
