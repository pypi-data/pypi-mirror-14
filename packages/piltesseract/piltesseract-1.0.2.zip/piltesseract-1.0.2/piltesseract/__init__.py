"""The piltesseract package is a simple Tesseract-OCR command line wrapper.

piltesseract allows quick conversion of PIL Image.Image instances to text using
Tesseract-OCR.

Warning:
    piltesseract is intended to only work with tesseract 3.03+, one awesome 
    feature added in 3.03 is the ability to pipe images via stdin, 
    piltesseract utilizes this feature.

Examples:
    >>> from PIL import Image
    >>> from piltesseract import get_text_from_image
    >>> image = Image.open('quickfox.png')
    >>> get_text_from_image(image)
    'The quick brown fox jumps over the lazy dog'
    
    Without a config file, you can set config variables using optional keywords.

    >>> text = get_text_from_image(
            image,
            tessedit_ocr_engine_mode=1,  # cube mode enum found in Tesseract-OCR docs
            cube_debug_level=1
            )

"""
from piltesseract.tesseractwrapper import get_text_from_image


__all__ = ['get_text_from_image']
