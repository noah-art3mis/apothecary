import tempfile
import pdf2image
from dotenv import load_dotenv
import anthropic
from utils.encode_image import pil_to_base64
from utils.prompts import PROMPT_EXTRACTION, SYSTEM_EXTRACTION
from utils.models import CLAUDE
from utils.estimate_costs import estimate_costs
from retry import retry
import logging

FILE_NAME = "ksi-pt1"
PAGE_LIMIT = 10
MODEL = CLAUDE.HAIKU.value.id
PROMPT = PROMPT_EXTRACTION
SYSTEM = SYSTEM_EXTRACTION

IMAGE_TYPE = "image/jpeg"
FILE_PATH = f"./input/{FILE_NAME}.pdf"
OUTPUT_FILE = f"./output/{FILE_NAME}-{MODEL}.jsonl"


def convert_and_extract_text(pdf_path, output_path, page_limit):
    print("== APOTHECARY AI TEXT EXTRACTION BEGIN ==")
    print(f"Converting '{FILE_NAME}' PDF to images...")

    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_path(pdf_path, output_folder=path)

        print(f"Extracting text from images using {MODEL}...")
        with open(output_path, "w", encoding="utf-8") as file:
            for page_number, page in enumerate(images):
                if page_number + 1 > page_limit:
                    break

                img = pil_to_base64(page)

                try:

                    response = query_claude_vision(MODEL, img, IMAGE_TYPE)
                    estimate_costs(response)
                    completion = response.content[0].text
                    file.write(completion)
                    file.write("\n")
                    print(f"Page: {page_number + 1} successful")
                except Exception as e:
                    print(f"Page: {page_number + 1} failed")
                    print(e)


@retry(tries=10, delay=1, jitter=1)
def query_claude_vision(model, image_data, image_type):
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
    )
    return message


if __name__ == "__main__":
    logging.basicConfig()
    load_dotenv()
    client = anthropic.Anthropic()
    convert_and_extract_text(FILE_PATH, OUTPUT_FILE, PAGE_LIMIT)
    print("Results in", OUTPUT_FILE)
    print("== APOTHECARY AI TEXT EXTRACTION END ==")
