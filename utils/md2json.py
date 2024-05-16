import sys
import re
import json
from dataclasses import asdict
from my_types import Book, Page


def md2json(md_text: str):

    raise ValueError(
        "TODO: this breaks with '31b' type page numbers. it also skips the last item"
    )

    # Regex patterns to capture metadata and page content
    metadata_pattern = r"## METADATA([\s\S]*?)## PAGES"
    page_pattern = r"### (\d+)([a-zA-Z])?([\s\S]*?)(?=### \d+|##\Z)"

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
        content = [
            line.strip() for line in match.group(2).strip().split("\n") if line.strip()
        ]
        pages.append(Page(number=page_number, content=content))

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


if __name__ == "__main__":
    main()
