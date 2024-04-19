import pdf2image
import tempfile

FILE_NAME = "ksi-pt1"

FILE_PATH = f'./input/{FILE_NAME}.pdf'
OUTPUT_FILE = f'./output/{FILE_NAME}.txt'
# PAGE_RESOLUTION = ~1200x1800

def check_image_resolution(pdf_path, output_path):

    print("Converting PDF to images...")
    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_path(pdf_path, output_folder=path)
        
        with open(output_path, 'w') as file:
            widths = []
            heights = []
            for page in images:

                width, height = page.size
                widths.append(width)
                heights.append(height)
                
                average_w = sum(widths) / len(widths)
                average_h = sum(heights) / len(heights)
                print(f"The resolution of the image is {width}x{height} pixels; average resolution: {average_w:.2f}x{average_h:.2f} pixels")
            print(f"The average resolution is {average_w:.2f}x{average_h:.2f} pixels")

if __name__ == '__main__':
    check_image_resolution(FILE_PATH, OUTPUT_FILE)
    
