from ImageMagic.Atesseract import *
from PIL import Image



def image_to_text(filePath,lang='chi_sim',config='',nice=0,output_type=Output.STRING,timeout=0,):

    """
    Gets the text content of the picture
    Args:
        filePath: Image path
        lang: The language of the image text, multi-language please use the plus sign, e.g: 'chi_sim+eng'
        config: Any other custom configuration flags that cannot be used by the Aocr function
        nice: Modify the processor priority that Tesseract runs, which Windows does not support
        output_type: Output type, defaulting to string type | including BYTES, DATAFRAME, DICT, STRING
        timeout: The length of the timeout

    Returns:
        Text content
    """

    image = Image.open(filePath)
    text = imageToString(image,lang=lang,config=config,nice=nice,output_type=output_type,timeout=timeout)
    return text


def check_languages(config=''):

    """
    Gets the installed languages
    Args:
        config: Any other custom configuration flags that cannot be used by the Aocr function

    Returns:
        Supported languages
    """
    languages = getLanguages(config=config)
    return languages


def get_image_boxs(filePath,lang='chi_sim',config='',nice=0,output_type=Output.STRING,timeout=0):

    """
    Gets an estimate of the picture bounding box
    Args:
        filePath: Image path
        lang: The language of the image text, multi-language please use the plus sign, e.g: 'chi_sim+eng'
        config: Any other custom configuration flags that cannot be used by the Aocr function
        nice: Modify the processor priority that Tesseract runs, which Windows does not support
        output_type: Output type, defaulting to string type | including BYTES, DATAFRAME, DICT, STRING
        timeout: The length of the timeout

    Returns:
        Border estimate
    """
    image = Image.open(filePath)
    boxs = imageToBoxes(image,lang=lang,config=config,nice=nice,output_type=output_type,timeout=timeout)
    return boxs


def get_image_osd(filePath,lang='chi_sim',config='',nice=0,output_type=Output.STRING,timeout=0):

    """
    Get information about orientation and script detection
    Args:
        filePath: Image path
        lang: The language of the image text, multi-language please use the plus sign, e.g: 'chi_sim+eng'
        config: Any other custom configuration flags that cannot be used by the Aocr function
        nice: Modify the processor priority that Tesseract runs, which Windows does not support
        output_type: Output type, defaulting to string type | including BYTES, DATAFRAME, DICT, STRING
        timeout: The length of the timeout

    Returns:
        Direction and script detection information
    """

    image = Image.open(filePath)
    osd = imageToOsd(image,lang=lang,config=config,nice=nice,output_type=output_type,timeout=timeout)
    return osd


def get_image_data(filePath,lang='chi_sim',config='',nice=0,output_type=Output.STRING,timeout=0):

    """
    Get image details, including boxes, confidence, line numbers, and page numbers.
    Requires Tesseract 3.05+
    Args:
        filePath: Image path
        lang: The language of the image text, multi-language please use the plus sign, e.g: 'chi_sim+eng'
        config: Any other custom configuration flags that cannot be used by the Aocr function
        nice: Modify the processor priority that Tesseract runs, which Windows does not support
        output_type: Output type, defaulting to string type | including BYTES, DATAFRAME, DICT, STRING
        timeout: The length of the timeout

    Returns:
        Detailed data for the picture, including boxes, confidence, line numbers, and page numbers
    """

    image = Image.open(filePath)
    data = imageToData(image,lang=lang,config=config,nice=nice,output_type=output_type,timeout=timeout)
    return data


def image_to_pdf(imagePath,savePath,lang='chi_sim',config='',nice=0,timeout=0):

    """
    Convert images into searchable PDF files
    Args:
        imagePath: Image path
        savePath: The path where the PDF is saved
        lang: The language of the image text, multi-language please use the plus sign, e.g: 'chi_sim+eng'
        config: Any other custom configuration flags that cannot be used by the Aocr function
        nice: Modify the processor priority that Tesseract runs, which Windows does not support
        timeout: The length of the timeout

    Returns:
        None
    """

    pdf = imageToPdfOrHocr(imagePath,lang=lang,config=config,nice=nice,extension='pdf',timeout=timeout)
    with open(savePath,'wb') as f:
        f.write(pdf)

def image_to_hocr(filePath,lang='chi_sim',config='',nice=0,timeout=0):

    """
    Get the HOCR output
    Args:
        filePath: Image path
        lang: The language of the image text, multi-language please use the plus sign, e.g: 'chi_sim+eng'
        config: Any other custom configuration flags that cannot be used by the Aocr function
        nice: Modify the processor priority that Tesseract runs, which Windows does not support
        timeout: The length of the timeout

    Returns:
        HOCR
    """

    hocr = imageToPdfOrHocr(filePath,lang=lang,config=config,extension='hocr',nice=nice,timeout=timeout)
    return hocr

def image_to_AltoXml(filePath,lang='chi_sim',config='',nice=0,timeout=0):

    """
    Returns the result of a Tesseract OCR run on the provided image to ALTO XML
    Args:
        filePath: Image path
        lang: The language of the image text, multi-language please use the plus sign, e.g: 'chi_sim+eng'
        config: Any other custom configuration flags that cannot be used by the Aocr function
        nice: Modify the processor priority that Tesseract runs, which Windows does not support
        timeout: The length of the timeout

    Returns:
        Returns the result of a Tesseract OCR run on the provided image to ALTO XML
    """

    xml = imageToAltoXml(filePath,lang=lang,config=config,nice=nice,timeout=timeout)
    return xml

