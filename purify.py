import os
import re
import json
import logging

import nltk

from utils.io import save_intermediate, save_result
from utils.json2md import json2md
from utils.extract_annotations import get_annots_from_pdf
from utils.text_cleanup import (
    fix_ellipses,
    fix_quotes,
    ai_cleanup_and_save_every_time,
    concatenate_text_in_same_page,
)
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
        get_annots_from_pdf(FILE_NAME)
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

    pages = [{"page": d["page"], "text": fix_quotes(d["text"])} for d in pages]
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

    savefile = save_result(book)
    logging.info(f"saved result at {savefile}")


if __name__ == "__main__":
    logging.info("== APOTHECARY START == ")
    main()
    logging.info("== APOTHECARY END == ")
