import os
import re
import json
import logging
import datetime
import subprocess

import nltk

from utils.json2md import json2md
from utils.query_claude import ai_cleanup
from configs import FILE_NAME, AUTHOR, TITLE, BOOK_ID, MODEL, PAGE_OFFSET

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
        pages = json.load(f)

    pages = [{"page": d["page"], "text": d["text"].strip()} for d in pages]
    save_counter = save_intermediate(pages, save_counter)
    logging.info(f"1. removed hanging whitespace")

    pages = [{"page": d["page"], "text": re.sub(r"\s+", " ", d["text"])} for d in pages]
    save_counter = save_intermediate(pages, save_counter)
    logging.info(f"2. removed multiple spaces")

    pages = [{"page": str(d["page"] + PAGE_OFFSET), "text": d["text"]} for d in pages]
    save_counter = save_intermediate(pages, save_counter)
    logging.info(f"3. fixed page numbers")

    pages = concatenate_text_in_same_page(pages)
    save_counter = save_intermediate(pages, save_counter)
    logging.info(f"4. concatenated text in same page")

    logging.info(f"5. ai cleanup")
    pages = ai_cleanup_and_save_every_time(pages, save_counter + 1)
    save_counter = save_intermediate(pages, save_counter)

    pages = [{"page": d["page"], "text": fix_ellipses(d["text"])} for d in pages]
    save_counter = save_intermediate(pages, save_counter)
    logging.info(f"6. sub ... for …")

    pages = [
        {"number": d["page"], "content": nltk.sent_tokenize(d["text"])} for d in pages
    ]
    save_counter = save_intermediate(pages, save_counter)
    logging.info(f"7. separate sentences")

    book = {"id": BOOK_ID, "title": TITLE, "author": AUTHOR, "pages": pages}
    save_counter = save_intermediate(book, save_counter)
    logging.info(f"8. fit pages into book")

    book = json2md(book)
    logging.info(f"9. convert to SADSL (.md)")

    save_result(book)


def save_result(book):
    id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"output/{FILE_NAME}_{MODEL}_{id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(book)
        logging.info(f"saved result at {filename}")


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


def save_intermediate(result, save_counter, extension=".json"):
    save_counter += 1

    with open(
        f"intermediate/{FILE_NAME}_{save_counter}{extension}", "w", encoding="utf-8"
    ) as f:
        json.dump(result, f, indent=2)

    return save_counter


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


def fix_ellipses(text):
    result = re.sub(r"(?<!\s)\.\.\.", " …", text)
    result = result.replace("...", "…")
    return result


if __name__ == "__main__":
    logging.info("== APOTHECARY START == ")
    main()
    logging.info("== APOTHECARY END == ")
