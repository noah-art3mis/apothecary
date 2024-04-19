import tempfile
import pdf2image
from dotenv import load_dotenv
from utils.encode_image import pil_to_base64
from utils.query_gpt import query_classification, query_extraction

FILE_NAME = "test"
PAGE_LIMIT = 10

FILE_PATH = f"./input/{FILE_NAME}.pdf"
OUTPUT_FILE = f"./output/{FILE_NAME}.jsonl"


def convert_and_extract_text(pdf_path, output_path, page_limit):
    print("== APOTHECARY AI TEXT EXTRACTION BEGIN ==")
    print(f"Converting '{FILE_NAME}' PDF to images...")

    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_path(pdf_path, output_folder=path)

        print("Extracting text from images using gpt4...")
        with open(output_path, "w", encoding="utf-8") as file:
            for page_number, page in enumerate(images):
                if page_number + 1 > page_limit:
                    break

                img = pil_to_base64(page)

                response = query_classification(img)
                if response == "Y":
                    try:
                        print(f"Page {page_number}: Y")
                        response = query_extraction(img)
                        file.write(response)
                        file.write("\n")
                    except Exception as e:
                        print(e)
                else:
                    print(f"Page {page_number} skipped")


if __name__ == "__main__":
    load_dotenv()
    convert_and_extract_text(FILE_PATH, OUTPUT_FILE, PAGE_LIMIT)
    print("== APOTHECARY AI TEXT EXTRACTION END ==")
