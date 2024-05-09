import re
import json
import logging

from configs import FILE_NAME
from utils.query_claude import ai_cleanup


def fix_ellipses(text):
    result = re.sub(r"(?<!\s)\.\.\.", " …", text)
    result = result.replace("...", "…")
    return result


def fix_quotes(text):
    # Pattern to match a string starting and ending with double quotes
    text = re.sub(r'"([^"]*)"', r"«\1»", text)
    return text


def ai_cleanup_and_save_every_time(data, save_counter):
    results = []
    costs = 0
    queries = 0

    for d in data:
        text, cost = ai_cleanup(d["text"])
        results.append({"page": d["page"], "text": text})
        costs += cost
        queries += 1

        with open(
            f"intermediate/{FILE_NAME}_{save_counter}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(results, f, indent=2)

    logging.info(f"queries: {queries}, total cost: ${costs:.2f}")
    return results


def concatenate_text_in_same_page(data):
    SEPARATOR = " ... "
    pages = {}
    for d in data:
        page = d["page"]
        text = d["text"]
        if page in pages:
            pages[page] += SEPARATOR + text
        else:
            pages[page] = text

    result = [{"page": page, "text": text} for page, text in pages.items()]
    return result
