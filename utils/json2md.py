import sys
import json
from utils.my_types import Book, Page


def json2md(book_dict: dict) -> str:
    """
    Takes a dict representing a Book object and returns a string with the markdown representation.
    """
    book: Book = Book(**book_dict)
    book.pages = [Page(**page) for page in book.pages]

    result = ""

    result += "## METADATA\n"
    result += "\n"
    result += book.id + "\n"
    result += book.author + "\n"
    result += book.title + "\n"
    result += "\n"
    result += "## PAGES\n"
    result += "\n"

    for page in book.pages:
        result += "### " + page.number + "\n"
        result += "\n"

        for line in page.content:
            result += line + "\n"
            result += "\n"

    return result


def main():
    if len(sys.argv) < 3:
        print("Usage: json2md.py <input_file> <output_file>")
        sys.exit(1)

    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]

    with open(INPUT, "r", encoding="utf-8") as file:
        book_dict = json.load(file)

    book = json2md(book_dict)

    with open(OUTPUT, "w", encoding="utf-8") as file:
        file.write(book)


if __name__ == "__main__":
    main()
