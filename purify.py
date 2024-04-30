import os
import re
import subprocess
import json
import nltk
from utils.query_claude import ai_cleanup
from configs import *
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
    filename="purify.log",
    encoding="utf-8",
)


def main():
    save_counter = 0

    logging.info(f"purifying {FILE_NAME}.pdf")

    if not os.path.exists(f"intermediate/{FILE_NAME}_0.json"):
        logging.info(f"0. extracting annotations")
        nltk.download("punkt")
        get_annots_from_pdf()
    else:
        logging.info(f"0. {FILE_NAME}_0 exists, skipping annot extraction")

    with open(f"intermediate/{FILE_NAME}_0.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data = [{"page": d["page"], "text": d["text"].strip()} for d in data]
    save_counter = save_intermediate(data, save_counter)
    logging.info(f"1. removed hanging whitespace")

    data = [{"page": d["page"], "text": re.sub(r"\s+", " ", d["text"])} for d in data]
    save_counter = save_intermediate(data, save_counter)
    logging.info(f"2. removed multiple spaces")

    data = [{"page": str(d["page"] + PAGE_OFFSET), "text": d["text"]} for d in data]
    save_counter = save_intermediate(data, save_counter)
    logging.info(f"3. fixed page numbers")

    data = concatenate_text_in_same_page(data)
    save_counter = save_intermediate(data, save_counter)
    logging.info(f"4. concatenated text in same page")

    logging.info(f"5. ai cleanup")
    data = ai_cleanup_and_save_every_time(data, save_counter + 1)
    save_counter = save_intermediate(data, save_counter)

    data = [{"page": d["page"], "text": nltk.sent_tokenize(d["text"])} for d in data]
    save_counter = save_intermediate(data, save_counter)
    logging.info(f"6. separate sentences")


def get_annots_from_pdf():
    params = [
        "pdfannots",
        "-p",
        "-f",
        "json",
        f"input/{FILE_NAME}.pdf",
        "-o",
        f"intermediate/{FILE_NAME}_0.json",
    ]

    subprocess.run(params)


def save_intermediate(result, save_counter):
    save_counter += 1

    with open(
        f"intermediate/{FILE_NAME}_{save_counter}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(result, f, indent=2)

    return save_counter


def concatenate_text_in_same_page(data):
    SEPARATOR = " … "
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

    logging.info(f"queries: {queries}, total cost: ${costs:.4f}")
    return results


if __name__ == "__main__":
    logging.info("== APOTHECARY START == ")
    main()
    logging.info("== APOTHECARY END == ")
