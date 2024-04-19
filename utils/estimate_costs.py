from utils.models import *


def find_by_id(id):
    for item in CLAUDE:
        if item.value.id == id:
            return item
    return None


def estimate_costs(response):
    model = find_by_id(response.model)

    if model is None:
        print("Model not found")
        return

    per_million_tokens = 1_000_000

    i_tokens = response.usage.input_tokens
    o_tokens = response.usage.output_tokens

    i_cost = model.value.input_cost * i_tokens / per_million_tokens
    o_cost = model.value.output_cost * o_tokens / per_million_tokens
    total_cost = i_cost + o_cost

    print(f"Model: {model.name}")
    print(f"Tokens: {i_tokens + o_tokens} ({i_tokens}+{o_tokens})")
    print(f"Total cost: ${total_cost:.4f}")
