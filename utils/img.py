import base64
import io

# Function to encode the PIL image
def encode_image(pil_img):
    # Create a bytes buffer for the image to save
    img_byte_arr = io.BytesIO()
    # Save the image as JPEG to the bytes buffer
    pil_img.save(img_byte_arr, format='JPEG')
    # Retrieve the byte data
    img_byte_arr = img_byte_arr.getvalue()
    # Encode bytes to base64
    return base64.b64encode(img_byte_arr).decode('utf-8')