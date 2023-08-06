PILtesseract
=======
[![](https://img.shields.io/pypi/v/piltesseract.svg?branch=master)](https://pypi.python.org/pypi/piltesseract)

Simple Tesseract wrapper for converting PIL Images to text.

**Warning:** PILtesseract is intended to only work with tesseract 3.03+,
one awesome feature added in 3.03 is the ability to pipe images via stdin,
PILtesseract utilizes this feature.

Features
------------
 - Completely wraps [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) command line optional arguments.
 - Sends [PIL](https://pillow.readthedocs.org/en/latest/) images to tesseract through stdin (avoids creating a temp file).
 - Works for Python 2 and 3.
 - All working code in [one file](https://github.com/Digirolamo/PILtesseract/blob/master/piltesseract/tesseractwrapper.py).
 - [MIT License](https://github.com/Digirolamo/PILtesseract/blob/master/LICENSE)
 - [Documentation](http://piltesseract.readthedocs.org/en/latest/)

Here is a simple example:


    >>> from PIL import Image
    >>> from piltesseract import get_text_from_image
    >>> image = Image.open('quickfox.png')
    >>> get_text_from_image(image)
    'The quick brown fox jumps over the lazy dog'

See [Advanced Example](http://piltesseract.readthedocs.org/en/latest/example.html)  
See [Recipes](http://piltesseract.readthedocs.org/en/latest/recipes.html)

Requirements
------------
More detailed installation instructions can be found [here](http://piltesseract.readthedocs.org/en/latest/install.html).
 - [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract): 3.03 or higher
   - First install either from source or from [binaries](https://github.com/tesseract-ocr/tesseract/wiki).
   - Ensure that the tesseract binary folder is on your [PATH](https://en.wikipedia.org/wiki/PATH_(variable)).
 - [Pillow](https://pillow.readthedocs.org/en/latest/)
   - ```$ pip install Pillow```
 - [Six](https://pythonhosted.org/six/)
   - ```$ pip install six```

Install
------------

    $ pip install piltesseract




