from PIL import ImageDraw,ImageFont
from PIL import Image as PILImage
import re
import requests
import json
import hashlib
import hmac
import base64
import time
import os
from loguru import logger
import shutil
import numpy as np

#They are used in the Audio class
RESULT = None
ANSWER = None


def word_to_image(text, path, fontPath=r'C:\Windows\Fonts\STXIHEI.TTF', LinesWords=14, fontsize=45, type='png', color=(255, 255, 255)):
    #文字转图片
    """
    Let the text you enter appear on an image,
    Your text word count should preferably be greater than or equal to 10!（In cases where you use the default font size）
    Args:
        text: Your text content
        path: The path where the picture is saved,You will also need to write the full name of your file (including the suffix!).
        fontPath: Font path
        LinesWords: Maximum number of words per line
        fontsize: Font size
        type: The type of picture saved
        color: Cloth background color (RGB color)

    Returns:

        None
    """

    max_len = 0

    text = re.sub(f"(.{{{LinesWords}}})", "\\1\r\n", text)
    if os.path.isfile('temp.txt'):
        pass
    with open('temp.txt','w',encoding='utf-8') as f:
        f.write(text)
    with open('temp.txt','r',encoding='utf-8') as f:
        temp_text=f.readlines()
    for i, s in enumerate(temp_text):
        if len(s) > max_len:
            max_len = len(s)
    fontSize = 50
    liens = text.split('\n')
    image = PILImage.new('RGB', ((fontSize * max_len), len(liens) * (fontSize + 5)), color)
    font = ImageFont.truetype(fontPath,fontsize)
    draw = ImageDraw.Draw(image)
    draw.text((40,5), text=text, font=font,fill='#000000')

    try:
        image.save(path, type)
    except FileNotFoundError as error:
        logger.error(f'Please check your file path, you need to enter a full path, including your file name (even the suffix!).\nerror:{error}')

    os.remove('temp.txt')


def audio_to_image(appid,key,audioPath,imagePath,fontPath=r'C:\Windows\Fonts\STXIHEI.TTF'):
    #音频转图片
    """
    Supports WAV, FLAC, OPUS, M4A, MP3 format audio files,
    Convert audio content into pictures, do you find this method a bit strange?
    Yes, it is the stitching of two other methods! You can use it according to your interests.
    Args:
        appid: your appid from https://console.xfyun.cn/services/lfasr
        key: your secretKey from https://console.xfyun.cn/services/lfasr
        audioPath: your audio file path
        imagePath: The path where the picture is saved,You will also need to write the full name of your file (including the suffix!). ）
        fontPath: Font path

    Returns:
        None
    """

    audio = Audio(appid=appid,key=key,upload_file_path=audioPath)
    get_list = audio.voice_to_word()
    get_text = ''.join(get_list)
    try:
        word_to_image(get_text,imagePath,fontPath)
    except FileNotFoundError as error:
        logger.error(f'Please check your file path, you need to enter a full path, including your file name (even the suffix!).\nerror:{error}')


def convert(originFilePath,format,savePath,mode=None):
    #图片格式转换
    """
    Picture format conversion, the current version supports all possible conversions between "L", "RGB" and "CMYK".
    Args:
        originFilePath: Path to the original file (full path,Includes suffix)
        format: Target format (the format you want)
        savePath: The converted save path, including the file name and even the suffix
        mode: Conversion mode

    Returns:
        None
    """

    image = PILImage.open(originFilePath).convert(mode=mode)
    image.save(savePath,format=format)


def equal_scale_image(filePath,savePath,multiple=1):
    #图片等比例变化
    """
    Change your image in equal proportions
    Args:
        filePath: Original file path
        savePath: The path to the save
        multiple: The multiplier of the change

    Returns:
        None
    """

    img = PILImage.open(filePath)
    width = img.size[0]
    height = img.size[1]
    img = img.resize((int(width * multiple), int(height * multiple)), PILImage.Resampling.LANCZOS)
    img.save(savePath)


def customize_image(filePath,savePath,new_width=None,new_height=None):
    #自定义图片分辨率
    """
    Custom image size (if no input is used, the original parameter will be used)
    Args:
        filePath: Original file path
        savePath: The path to the save
        new_width: width
        new_height: height

    Returns:
        None
    """

    img = PILImage.open(filePath)
    width = img.size[0]
    height = img.size[1]
    if new_width is None:
        img = img.resize((int(width), int(new_height)), PILImage.Resampling.LANCZOS)
    if new_height is None:
        img = img.resize((int(new_width,int(height)),PILImage.Resampling.LANCZOS))
    if new_width is None and new_height is None:
        img = img.resize((int(width),int(height)),PILImage.Resampling.LANCZOS)
    else:
        img = img.resize((int(new_width),int(new_height)),PILImage.Resampling.LANCZOS)
    img.save(savePath)


def lbp_image_hash(imagePath):
    #哈希局部二值算法
    """
    The local binary algorithm calculates the hash value.
    Args:
        imagePath: Image path

    Returns:
        The hash of the image (consisting of 0 and 1)
    """

    # 打开图像并转换为灰度图像
    with PILImage.open(imagePath) as img:
        gray_img = img.convert('L')

    # 缩放图像为8x8大小
    small_img = gray_img.resize((8, 8), resample=PILImage.Resampling.BILINEAR)

    # 计算每个像素的平均值
    pixels = list(small_img.getdata())
    avg_pixel = sum(pixels) // 64

    # 将像素值转换为二进制哈希值
    binary_hash = ''
    for pixel in pixels:
        if pixel >= avg_pixel:
            binary_hash += '1'
        else:
            binary_hash += '0'

    return binary_hash


def p_image_hash(imagePath):
    #哈希感知算法
    """
    Use Perceptual Hash computation to get the image hash.
    Args:
        imagePath: image path

    Returns:
        Image hash value.
    """

    image = PILImage.open(imagePath).convert('L')
    # 缩放图像为8x8的尺寸
    image = image.resize((8, 8), PILImage.Resampling.LANCZOS)
    # 将图像转换为numpy数组
    pixels = np.array(image.getdata()).reshape((8, 8))
    # 计算像素平均值
    avg_pixel = pixels.mean()
    # 将像素值与平均值进行比较，生成64位哈希值
    hash_value = 0
    for row in range(8):
        for col in range(8):
            if pixels[row, col] > avg_pixel:
                hash_value |= 1 << (row * 8 + col)
    return hash_value


def pca_image_hash(imagePath):
    #主成分分析算法
    """
    The principal component analysis algorithm calculates the image hash value.
    Args:
        imagePath: image path
    Returns:
        The hash value of the image.
    """

    image = PILImage.open(imagePath).convert('L')
    image = image.resize((16,16))

    image_array = np.array(image.getdata()).reshape(image.size)
    flattened_array = image_array.flatten()
    flattened_array = np.expand_dims(flattened_array, axis=0)

    num_components = 64
    u, s, vh = np.linalg.svd(flattened_array - flattened_array.mean())
    components = vh[:num_components]

    #转换为二进制
    pca_hash = np.packbits(components >= 0).tobytes()

    return pca_hash


def fft_image_hash(imagePath):
    #离散傅里叶变换算法
    """
    The Fourier transform algorithm finds the hash value.
    Args:
        imagePath: image path
    Returns:
        Image hash value.
    """

    image = PILImage.open(imagePath)
    resized_image = image.resize((32,32)).convert('L')

    #进行离散傅里叶变换
    pixels = np.asarray(resized_image.getdata(),dtype=float).reshape(resized_image.size)
    transformed_image = np.fft.fft2(pixels)

    magnitudes = np.abs(transformed_image)
    average_magnitude = np.mean(magnitudes)
    hash_value = np.zeros_like(magnitudes, dtype=int)
    hash_value[magnitudes >= average_magnitude] = 1

    #返回二进制数据，方便直接比较
    return hash_value.flatten().tobytes()


def average_image_hash(imagePath):
    #哈希平均算法
    """
    The image hash is obtained using the average hash algorithm.

    Args:
        imagePath: image path.
    Returns:
        image hash.
    """

    hash_size = 8
    # 加载图像并调整大小
    with PILImage.open(imagePath) as image:
        image = image.convert('L').resize((hash_size, hash_size), PILImage.Resampling.LANCZOS)

    # 计算平均灰度值
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)

    # 将像素值与平均值进行比较并生成哈希值
    bits = "".join(['1' if pixel > avg else '0' for pixel in pixels])
    hash_value = int(bits, 2)

    return hash_value


def remove_same_images(directoryPath):
    #移除相同图片
    """
    Delete the same image in the directory and keep only one picture (using local binary value algorithm).
    Supports jpg, png, bmp, webp, jpeg, gif, svg, tif, tiff.
    Args:
        directoryPath: The file directory path

    Returns:
        None
    """

    # 保存图像哈希值和路径
    hashes = {}

    # 遍历目录中的所有图像
    for filename in os.listdir(directoryPath):
        if not filename.endswith((".jpg", ".png", ".bmp",".webp",".jpeg",".gif","svg","tif","tiff")):
            continue
        filepath = os.path.join(directoryPath, filename)

        # 计算图像哈希值
        hash_value = lbp_image_hash(filepath)

        # 如果哈希值已经存在，则删除图像
        if hash_value in hashes:
            logger.info(f"Removing duplicate image: {filepath}")
            os.remove(filepath)
        else:
            hashes[hash_value] = filepath

    logger.info("Done removing duplicate images.")


def categorize_image(filePath):
    #图片分类
    """
    Categorize your images, support jpg, jpeg, png, webp, bmp, tif, tiff, gif, svg, wmf
    Args:
        filePath: Your folder path

    Returns:
        None
    """

    for filename in os.listdir(filePath):
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".png":
            try:
                os.makedirs(f'{filePath}/png')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath, filename), f'{filePath}/png')
        elif ext == ".jpg" or ext == 'jpeg':
            try:
                os.makedirs(f'{filePath}/jpg')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath, filename), f'{filePath}/jpg')
        elif ext == '.webp':
            try:
                os.makedirs(f'{filePath}/webp')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath, filename), f'{filePath}/webp')
        elif ext == 'bmp':
            try:
                os.makedirs(f'{filePath}/bmp')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath,filename),f'{filePath}/bmp')
        elif ext == 'tif' or ext == 'tiff':
            try:
                os.makedirs(f'{filePath}/tif')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath,filename),f'{filePath}/tif')
        elif ext == 'gif':
            try:
                os.makedirs(f'{filePath}/gif')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath,filename),f'{filePath}/gif')
        elif ext == 'svg':
            try:
                os.makedirs(f'{filePath}/svg')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath,filename),f'{filePath}/svg')
        elif ext == 'wmf':
            try:
                os.makedirs(f'{filePath}/wmf')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath,filename),f'{filePath}/wmf')
        else:
            try:
                os.makedirs(f'{filePath}/another')
            except FileExistsError:
                pass
            shutil.copy(os.path.join(filePath,filename),f'{filePath}/another')


class Audio:
    #音频类
    """
    You need to pass in the appid, secret-key, and path to the audio file
    """

    def __init__(self,appid,key,upload_file_path):

        """
        Args:
            appid: your appid from https://console.xfyun.cn/services/lfasr
            key: your secretKey from https://console.xfyun.cn/services/lfasr
            upload_file_path: your audio file path
        """

        self.__appid = appid
        self.__key = key
        self.__ts = str(int(time.time()))
        self.__upload_file_path = upload_file_path
        self.__uploadlinks = 'https://raasr.xfyun.cn/v2/api/upload'
        self.__getresult = 'https://raasr.xfyun.cn/v2/api/getResult'
        self.__header = {
            'Content-Type': 'application/json'
        }


    def __get_signa(self):

        """
        get signa
        """

        appid = self.__appid
        ts = self.__ts
        key = self.__key
        base_string = appid + ts
        base_string_md5 = hashlib.md5()
        base_string_md5.update(base_string.encode('utf-8'))
        base_string_md5 = base_string_md5.hexdigest()
        signa = hmac.new(key.encode('utf-8'),bytes(base_string_md5,'utf-8'),hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        return str(signa,'utf-8')

    def __upload(self):

        upload_file_path = self.__upload_file_path
        file_size = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        data = {}
        data['appId'] = self.__appid
        data['signa'] = self.__get_signa()
        data['ts'] = self.__ts
        data['duration'] = '200'
        data['fileSize'] = file_size
        data['fileName'] = file_name

        with open(upload_file_path,'rb') as f:
            documents = f.read(file_size)

        response = requests.post(self.__uploadlinks,params=data,headers=self.__header,data=documents)
        result = json.loads(response.text)
        #print(result)
        return result


    def voice_to_word(self):
        #音频转文字
        """
        Audio to text,Supports WAV, FLAC, OPUS, M4A, MP3 format audio files,
        If you call this method, you need to pass parameters in the class
        Returns:
            A list of results
        """

        global RESULT,ANSWER
        ANSWER_LIST=[]

        upload_result = self.__upload()
        orderId = upload_result['content']['orderId']
        data={}
        data['appId'] = self.__appid
        data['signa'] = self.__get_signa()
        data['ts'] = self.__ts
        data['orderId'] = orderId
        data['resultType'] = "transfer"

        status = 3
        """
        0：订单已创建（The order is created）
        3：订单处理中（Order processing）
        4：订单已完成（The order is completed）
        -1：订单失败（The order failed）
        """
        # 使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(self.__getresult,params=data,headers=self.__header)
            RESULT = json.loads(response.text)
            status = RESULT['content']['orderInfo']['status']
            if status == 4:
                break
            time.sleep(5)

        logger.debug(f'The data returned by the server：{RESULT}')

        b = RESULT.get('content').get('orderResult')
        b = json.loads(b)
        c = b.get('lattice2')
        # print(c[0].get('json_1best'))
        for f in range(0, len(c)):
            d = c[f].get('json_1best').get('st').get('rt')[0].get('ws')
            # print(d)
            for i in d:
                # print(i)
                ANSWER = i.get('cw')[0].get('w')
                #print(ANSWER, end='')
                ANSWER_LIST.append(ANSWER)

        return ANSWER_LIST
