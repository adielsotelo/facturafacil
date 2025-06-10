from PIL import Image
from io import BytesIO
import tesserocr

def process_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    text = tesserocr.image_to_text(image, lang='spa')
    return text
