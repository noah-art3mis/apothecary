FILE_NAME = "ksi-pt1"
FILE_NAME = "test"
PAGE_OFFSET = -9
MAX_CHARACTERS_PER_PLATE = [300, 350, 400]
MODEL = "haiku"

MODELS = [
    {
        "name": "opus",
        "id": "claude-3-opus-20240229",
        "input_cost": 15,
        "output_cost": 75,
    },
    {
        "name": "sonnet",
        "id": "claude-3-sonnet-20240229",
        "input_cost": 3,
        "output_cost": 15,
    },
    {
        "name": "haiku",
        "id": "claude-3-haiku-20240307",
        "input_cost": 0.25,
        "output_cost": 1.25,
    },
]
