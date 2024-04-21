import logging
from dotenv import load_dotenv
from retry import retry
import anthropic
from utils.encode_image import pdf_to_base64
from utils.estimate_costs import estimate_costs
from configs import *


def convert_and_extract_text(pdf_path, output_path, page_limit):
    print("== APOTHECARY AI TEXT EXTRACTION BEGIN ==")
    print(f"Converting '{FILE_NAME}' PDF to images...")

    images = pdf_to_base64(pdf_path)

    print(f"Extracting text from images using {MODEL}...")
    with open(output_path, "w", encoding="utf-8") as file:
        for page_number, page in enumerate(images):
            if page_number + 1 > page_limit * 2:
                continue

            if page_number + 1 < page_limit:
                continue

            try:
                messages = get_messages(PROMPT, IMAGE_TYPE, page)
                response = query_claude_vision(MODEL, messages, SYSTEM)
                estimate_costs(response)
                completion = response.content[0].text
                file.write(completion)
                file.write("\n")
                print(f"Page: {page_number + 1} successful")
            except Exception as e:
                print(f"Page: {page_number + 1} failed: {e}")


@retry(tries=10, delay=1, backoff=2)
def query_claude_vision(model, messages, system):
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        system=system,
        messages=messages,
    )
    return message


def get_messages(prompt, image_type, image_data):
    return [
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
                {"type": "text", "text": prompt},
            ],
        }
    ]


if __name__ == "__main__":
    logging.basicConfig()
    load_dotenv()
    client = anthropic.Anthropic()
    convert_and_extract_text(FILE_PATH, OUTPUT_FILE, PAGE_LIMIT)
    print("Results in", OUTPUT_FILE)
    print("== APOTHECARY AI TEXT EXTRACTION END ==")
