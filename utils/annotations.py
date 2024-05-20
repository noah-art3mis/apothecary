import subprocess
import os
import logging
import nltk
import json
from configs import FILE_NAME


def extract_annotations():
    if not os.path.exists(f"intermediate/{FILE_NAME}_0.json"):
        logging.info(f"0. extracting annotations")
        nltk.download("punkt")
        get_annots_from_pdf(FILE_NAME)  # saves to intermediate file 0
    else:
        logging.info(f"0. {FILE_NAME}_0 exists, skipping annot extraction")

    with open(f"intermediate/{FILE_NAME}_0.json", "r", encoding="utf-8") as f:
        pages = json.load(f)

    return pages


def get_annots_from_pdf(file_name):
    params = [
        "pdfannots",
        "-p",
        "-f",
        "json",
        f"input/{file_name}.pdf",
        "-o",
        f"intermediate/{file_name}_0.json",
    ]

    subprocess.run(params)
