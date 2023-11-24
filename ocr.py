from PIL import Image
import pytesseract

def ts(image_path):
    img = Image.open(image_path)
    custom_config = r'--oem 3 --psm 6 -l rus+eng'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text.replace('®', '•'). replace('©', '•')
