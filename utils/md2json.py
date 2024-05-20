import sys
import re
import json
from dataclasses import asdict
from my_types import Book, Page

MAX_LENGTH = [275]


def md2json(md_text: str):

    # Regex patterns to capture metadata and page content
    metadata_pattern = r"## METADATA([\s\S]*?)## PAGES"
    page_pattern = r"### (\d+)([a-zA-Z])?([\s\S]*?)(?=[##])"

    # Extract metadata
    metadata_content = re.search(metadata_pattern, md_text, re.MULTILINE)

    if not metadata_content:
        raise ValueError("Metadata not found")

    metadata = {}
    lines = metadata_content.group(1).strip().split("\n")
    metadata["id"] = lines[0].strip()
    metadata["author"] = lines[1].strip()
    metadata["title"] = lines[2].strip()

    # Extract pages
    pages = []
    for match in re.finditer(page_pattern, md_text, re.MULTILINE):
        page_number = match.group(1).strip()
        letter = match.group(2).strip() if match.group(2) else ""
        page_number = str(page_number) + letter

        content = [
            line.strip() for line in match.group(3).strip().split("\n") if line.strip()
        ]

        pages.append(Page(page_number, content))

    # Create Book instance
    book = Book(
        id=metadata["id"],
        author=metadata["author"],
        title=metadata["title"],
        pages=pages,
    )

    return book


def main():
    if len(sys.argv) < 3:
        print("Usage: json2md.py <input_file> <output_file>")
        sys.exit(1)

    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]

    with open(INPUT, "r", encoding="utf-8") as file:
        book_dict = file.read()

    book = md2json(book_dict)

    with open(OUTPUT, "w", encoding="utf-8") as file:
        book_dict = asdict(book)
        json.dump(book_dict, file, indent=2)

    n_pages = len(book.pages)
    max_plates = max(len(page.content) for page in book.pages)
    max_len = max(len(sentence) for page in book.pages for sentence in page.content)

    print(f"== md2json ==")
    print(f"Summary")
    print(f"Book ID: {book.id}")
    print(f"Number of pages: {n_pages}")
    print(f"maximum number of plates in a page: {max_plates}")
    print(f"maximum char length in pages: {max_len}")

    l = []
    for page in book.pages:
        for i, sentence in enumerate(page.content):
            n = page.number
            length = len(sentence)
            item = (n, i, length)
            l.append(item)
    l.sort(key=lambda x: x[2], reverse=True)

    print("Longest sentences:")
    for v in l:
        if v[2] > MAX_LENGTH[0]:
            print("\t" + str(v))


if __name__ == "__main__":
    main()
