import pdf2image
from PIL import Image
import pytesseract
import tempfile

FILE_NAME = "test"

FILE_PATH = f'./input/{FILE_NAME}.pdf'
OUTPUT_FILE = f'./output/{FILE_NAME}.txt'
# PAGE_RESOLUTION = ~1200x1800

def convert_and_extract_text(pdf_path, output_path):

    print("Converting PDF to images...")
    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_path(pdf_path, output_folder=path)
        

        print("Extracting text from images using tesseract...")
        with open(output_path, 'w') as file:
            for page_number, page in enumerate(images):
                if page_number > 20:
                    break

                width, height = page.size
                print(f"The resolution of the image is {width}x{height} pixels.")
                
                detected_text = pytesseract.image_to_string(page)
                result = f"<<Page {page_number + 1}>>\n{detected_text}\n"
                print(result)
                file.write(result)

if __name__ == '__main__':
    convert_and_extract_text(FILE_PATH, OUTPUT_FILE)
    
