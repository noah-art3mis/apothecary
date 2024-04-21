import pathlib
import base64
from PIL import Image
import io
import fitz

# # Function to encode the PIL image
# def pil_to_base64(pil_img):
#     # Create a bytes buffer for the image to save
#     img_byte_arr = io.BytesIO()
#     # Save the image as JPEG to the bytes buffer
#     pil_img.save(img_byte_arr, format="JPEG")
#     # Retrieve the byte data
#     img_byte_arr = img_byte_arr.getvalue()
#     # Encode bytes to base64
#     return base64.b64encode(img_byte_arr).decode("utf-8")


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode("utf-8")
        return base64_string


def pdf_to_base64(pdf_path) -> list[str]:
    pngs = pdf_to_pngs(pdf_path)
    base64 = pngs_to_base64(pngs)
    return base64


def pdf_to_pngs(pdf_path) -> list[Image.Image]:
    file_name = pathlib.Path(pdf_path).stem
    partial_output_path = f"./intermediate/{file_name}"

    doc = fitz.open(pdf_path)

    if not pathlib.Path(partial_output_path).exists():
        pathlib.Path(partial_output_path).mkdir(parents=True)

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        # pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # type: ignore
        for n, annot in enumerate(page.annots()):  # type: ignore
            pix = annot.get_pixmap()

            pix.save(f"{partial_output_path}/{n}.png")

    images = [
        Image.open(f"{partial_output_path}/{page_num}.png")
        for page_num in range(doc.page_count)
    ]

    doc.close()
    return images


def pngs_to_base64(images: list[Image.Image], quality=75, max_size=(1024, 1024)):
    base64_encoded_pngs = []
    for image in images:
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        image_data = io.BytesIO()
        image.save(image_data, format="PNG", optimize=True, quality=quality)
        image_data.seek(0)
        base64_encoded = base64.b64encode(image_data.getvalue()).decode("utf-8")
        base64_encoded_pngs.append(base64_encoded)

    return base64_encoded_pngs
