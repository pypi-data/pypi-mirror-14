# PILtesseract
Simple Tesseract wrapper for converting PIL Images to text.

**Warning:** PILtesseract is intended to only work with tesseract 3.03+,
one awesome feature added in 3.03 is the ability to pipe images via stdin,
PILtesseract utilizes this feature.

Here is a simple example:


    >>> from PIL import Image
    >>> from piltesseract import get_text_from_image
    >>> image = Image.open('quickfox.png')
    >>> get_text_from_image(image)
    'The quick brown fox jumps over the lazy dog'

See more advanced examples.  
See recipes.



