from configs import MODELS


def find_by_id(id, models):
    for item in models:
        if item["id"] == id:
            return item
    return None


def estimate_costs(response) -> str:
    model = find_by_id(response.model, MODELS)

    if model is None:
        return f"Was not able to find model {response.model} in saved models. Skipping cost estimation"

    per_million_tokens = 1_000_000

    i_tokens = response.usage.input_tokens
    o_tokens = response.usage.output_tokens

    i_cost = model["input_cost"] * i_tokens / per_million_tokens
    o_cost = model["output_cost"] * o_tokens / per_million_tokens
    total_cost = i_cost + o_cost

    return f"Model: {model['name']} | Tokens: {i_tokens + o_tokens} ({i_tokens}+{o_tokens}) | Total cost: ${total_cost:.4f}"
