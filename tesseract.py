import tempfile
import pdf2image
import pytesseract

FILE_NAME = "test"
PAGE_LIMIT = 20

FILE_PATH = f"./input/{FILE_NAME}.pdf"
OUTPUT_FILE = f"./output/{FILE_NAME}.txt"
# PAGE_RESOLUTION = ~1200x1800


def convert_and_extract_text(pdf_path, output_path):
    print("== APOTHECARY TESSERACT TEXT EXTRACTION BEGIN ==")
    print("Converting PDF to images...")
    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_path(pdf_path, output_folder=path)

        print("Extracting text from images using tesseract...")
        with open(output_path, "w", encoding="utf-8") as file:
            for page_number, page in enumerate(images):
                if page_number + 1 > PAGE_LIMIT:
                    break

                detected_text = pytesseract.image_to_string(page)
                result = f"<<Page {page_number + 1}>>\n{detected_text}\n"
                print(result)
                file.write(result)


if __name__ == "__main__":
    convert_and_extract_text(FILE_PATH, OUTPUT_FILE)
    print("== APOTHECARY TESSERACT TEXT EXTRACTION END ==")
