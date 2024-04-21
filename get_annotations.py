import fitz
from configs import *
from fitz import Annot


def main():
    doc = fitz.open(FILE_PATH)
    for page in doc:
        print(page.get_text())
        for annot in page.annots():  # type: ignore
            print(f"{page.number}: {annot.get_textbox(Annot.rect)}")  # type: ignore


if __name__ == "__main__":
    main()
