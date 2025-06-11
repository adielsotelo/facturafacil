from PIL import Image
from io import BytesIO
import tesserocr
import os

# Ruta absoluta del tessdata
TESSDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tessdata')

def process_image(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        with tesserocr.PyTessBaseAPI(path=TESSDATA_DIR, lang='spa') as api:
            api.SetImage(image)
            text = api.GetUTF8Text()
            return text
    except Exception as e:
        return f"❌ Error procesando la imagen: {str(e)}"
