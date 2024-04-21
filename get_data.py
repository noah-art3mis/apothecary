import re
import subprocess
import json
import nltk
from utils.query_claude import ai_cleanup

FILE_NAME = "ksi-pt1"
FILE_NAME = "test"
PAGE_OFFSET = -9
MAX_CHARACTERS_PER_PLATE = [300, 350, 400]


def main():

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

    # turn json into just page and text
    with open(f"intermediate/{FILE_NAME}_0.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(f"intermediate/{FILE_NAME}_1.json", "w", encoding="utf-8") as f:
        result = [{"page": d["page"], "text": d["text"].strip()} for d in data]
        json.dump(result, f, indent=2)

    # fix spacing
    with open(f"intermediate/{FILE_NAME}_1.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(f"intermediate/{FILE_NAME}_2.json", "w", encoding="utf-8") as f:
        result = [
            {"page": d["page"], "text": re.sub(r"\s+", " ", d["text"])} for d in data
        ]
        json.dump(result, f, indent=2)

    # fix pagination
    with open(f"intermediate/{FILE_NAME}_2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(f"intermediate/{FILE_NAME}_3.json", "w", encoding="utf-8") as f:
        result = [
            {"page": str(d["page"] + PAGE_OFFSET), "text": d["text"]} for d in data
        ]
        json.dump(result, f, indent=2)

    # collapse pages
    with open(f"intermediate/{FILE_NAME}_3.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(f"intermediate/{FILE_NAME}_4.json", "w", encoding="utf-8") as f:
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
        json.dump(result, f, indent=2)

    # ai cleanup
    with open(f"intermediate/{FILE_NAME}_4.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(f"intermediate/{FILE_NAME}_5.json", "w", encoding="utf-8") as f:
        result = [{"page": d["page"], "text": ai_cleanup(d["text"])} for d in data]
        json.dump(result, f, indent=2)

    # separate sentences
    with open(f"intermediate/{FILE_NAME}_4.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(f"intermediate/{FILE_NAME}_5.json", "w", encoding="utf-8") as f:
        result = [
            {"page": d["page"], "text": nltk.sent_tokenize(d["text"])} for d in data
        ]
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    nltk.download("punkt")
    main()
