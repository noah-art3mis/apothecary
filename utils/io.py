import json
from datetime import datetime

from configs import FILE_NAME, MODEL


def save_intermediate(result, save_counter, extension=".json"):
    save_counter += 1

    with open(
        f"intermediate/{FILE_NAME}_{save_counter}{extension}", "w", encoding="utf-8"
    ) as f:
        json.dump(result, f, indent=2)

    return save_counter


def save_result(book):
    id = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"output/{FILE_NAME}_{MODEL}_{id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(book)

    return filename
