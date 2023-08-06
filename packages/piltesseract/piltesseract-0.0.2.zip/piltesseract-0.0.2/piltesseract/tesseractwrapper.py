"""This module contains all of the tesseract wrapping and image-to-text code.

Attributes:
    TESSERACT_DIR (str): The default path to the tesseract install 
        directory.
    DEFAULT_FORMAT (str): The default image format to send to tesseract 
        if an image doesn't not have a declared format. Otherwise, try
        to use the former format if we can.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import platform
import subprocess
from subprocess import PIPE
import sys
from PIL import Image
import six


#If tesseract binary is not on os.environ["PATH"] either the put the path below
#or use the optional tesseract_dir_path of the functions below.
TESSERACT_DIR = ""
DEFAULT_FORMAT = "BMP"


_IS_WINDOWS = platform.system() == "Windows"


def get_text_from_image(image, tesseract_dir_path=TESSERACT_DIR, stderr=None,
                        psm=3, lang="eng", tessdata_dir_path=None,
                        user_words_path=None, user_patterns_path=None,
                        config_name=None, **config_variables):
    """Uses tesseract to get text from an image.
    
    Outside of image, tesseract_dir_path, and stderr, the arguments mirror 
    the official command line's usage. A list of the command line options 
    can be found here:
    https://tesseract-ocr.googlecode.com/svn/trunk/doc/tesseract.1.html

    Args:
        image (Image.Image or str): The image to find text from or a path to
            that image.
        tesseract_dir_path (Optional[str]): The path to the directory 
            with the tesseract binary. Defaults to "", which works if the 
            binary is on the environmental PATH variable.
        stderr (Optional[file]): The file like object (implements `write`) 
            the tesseract stderr stream will write to. Defaults to None. 
            You can set it to sys.stdin to see all output easily.
        psm (Optional[int]): Page Segmentation Mode. Limits Tesseracts layout
            analysis (see the Tesseract docs). Default is 3, full analysis.
        lang (Optional[str]): The language to use. Default is 'eng' for
            English.
        tessdata_dir_path (Optional[str]): The path to the tessdata 
            directory.
        user_words_path (Optional[str]): The path to user words file.
        user_patterns_path (Optional[str]): The path to the user 
            patterns file.
        config_name (Optional[str]): The name of a config file.
        **config_variables: The config variables for tesseract.
            A list of config variables can be found here:
            http://www.sk-spell.sk.cx/tesseract-ocr-parameters-in-302-version

    Returns:
        str: The parsed text.

    Raises:
        subprocess.CalledProcessError: If the tesseract exit status is 
            not a success. 
        
    Examples:
        Examples assume "image" is a picture of the text "ABC123". 
        See piltesseract tests for working code.

        >>> get_text_from_image(image)
        'ABC123'
        >>> get_text_from_image(image, psm=10)  #single character psm
        'A'

        You can use tesseract's default configs or your own:

        >>> get_text_from_image(image, config_name='digits')
        '13123'

        Without a config file, you can set config variables using optional keywords:

        >>> text = get_text_from_image(
                image,
                tessedit_char_whitelist='1'
                tessedit_ocr_engine_mode=1,  #cube mode enum found in Tesseract-OCR docs
                )
        '1  11 '

    """
    if isinstance(image, Image.Image):
        image_input = "stdin"
        use_stdin = True
    elif isinstance(image, six.text_type):
        image_input = image
        use_stdin = False
        if not os.path.exists(image_input):
            raise ValueError("Image file does not exist: {}"
                             "".format(image_input))
    else:
        raise ValueError("image argument type not supported: {}."
                         "".format(type(image)))
    command_start = "{} stdout -psm {} -l {}".format(image_input, psm, lang)
    commands = command_start.split(' ')
    if tessdata_dir_path is not None:
        commands.append('--tessdata-dir"{}"'.format(tessdata_dir_path))
    if user_words_path is not None:
        commands.append('--user-words"{}"'.format(user_words_path))
    if user_patterns_path is not None:
        commands.append('--user-patterns"{}"'.format(user_patterns_path))
    for config_var, value in config_variables.items():
        commands += ['-c', '{}={}'.format(config_var, value)]
    if config_name is not None:
        commands.append(config_name)
    if not use_stdin:
        pipe = get_tesseract_process(
            commands, tesseract_dir_path=tesseract_dir_path,
            stdin=None
            )
    else:
        pipe = get_tesseract_process(commands, tesseract_dir_path=tesseract_dir_path)
        # tesseract doesn't seem to play nice with stdin on many formats
        # on windows.
        if _IS_WINDOWS or not image.format:
            image_format = DEFAULT_FORMAT
        else:
            image_format = image.format
        image.save(pipe.stdin, format=image_format)
        pipe.stdin.close()
    text = pipe.stdout.read()
    error = pipe.stderr.read()
    pipe.terminate()
    if pipe.returncode != 0:
        msg = "get_text_from_image failed while calling tesseract."
        if error:
            msg += ' tesseract stderr: "{}".'.format(error)
        raise subprocess.CalledProcessError(msg)
    elif error and stderr is not None:
        stderr.write(six.text_type(error))
    text =  six.text_type(text, "utf-8", errors="ignore")
    text = text.rstrip('\r\n ')
    return text


def get_tesseract_process(commands, tesseract_dir_path=TESSERACT_DIR,
                      stdin=PIPE, stdout=PIPE, stderr=PIPE):
    """Popen and return tesseract command line utility.
    
    Opens and returns a tesseract process to the tesseract command line 
    utility. Uses Popen to open a process and pipes to tesseract.

    Args:
        commands (List[str]): The command line strings passed into the tesseract 
            binary. Do not include the binary name or path in this variable.
        tesseract_dir_path (Optional[str]): The path to the directory 
            with the tesseract binary. Defaults to "", which works if the 
            binary is on the environmental PATH variable.

    Returns:
        subprocess.Popen: The open subprocess pipe.

    """
    #process environment variables
    if tesseract_dir_path == "":
        bin_path = 'tesseract'
        tess_cwd = None
        tess_env = None
    else:
        bin_path = os.path.join(tesseract_dir_path, 'tesseract')
        tess_cwd = tesseract_dir_path
        #str because python 2 enforces no unicode and 3 defaults to it... bizarre
        tess_env = {str('PATH'): str(tesseract_dir_path)}
    commands.insert(0, bin_path)
    #So console window does not popup on windows
    if not hasattr(subprocess, "STARTUPINFO"):
        console_startup_info = None
    else:
        console_startup_info = subprocess.STARTUPINFO()
        console_startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        console_startup_info.wShowWindow = subprocess.SW_HIDE
    pipe = subprocess.Popen(
        commands,
        stdin=stdin, stdout=stdout, stderr=stderr,
        cwd=tess_cwd,
        env=tess_env,
        startupinfo=console_startup_info,
        )
    return pipe


def test_tesseract_path_version(tesseract_dir_path=TESSERACT_DIR):
    """Tests that the correct version tesseract is installed and on the path.
    
    Use this function to ensure that either tesseract is on a default or 
    specified path. The function raises ImportErrors if tesseract does not work
    or is not the right version. The function is silent if everything passes.
    
    Args:
        tesseract_dir_path (Optional[str]): The path to the directory 
            with the tesseract binary. Defaults to "", which works if the 
            binary is on the environmental PATH variable.
    
    Raises:
        ImportError: If the tesseract requirement is not met.
    
    """
    minimum_version = (3, 3, 0)
    try:
        pipe = get_tesseract_process(
            ['-v'], tesseract_dir_path=tesseract_dir_path,
            stdin=None, stderr=subprocess.STDOUT)
        output = pipe.stdout.readline()
        pipe.terminate()
        version_string = ''.join(c for c in output if c.isdigit() or c == '.')
        version_tuple = tuple(int(c) for c in version_string.split('.'))
        if minimum_version > version_tuple:
            raise ImportError("You have an older version of Tesseract-OCR. PILtesseract "
                              "only works with version (3, 3, 0)+. You have version {}."
                              "".format(version_tuple))
    except (subprocess.CalledProcessError, WindowsError):
        raise ImportError("Tesseract-OCR is either not installed, not on the path variable, "
                          "or the tesseract_dir_path variable is incorrect.\n"
                          "Please fix this issue before importing piltesseract.")
