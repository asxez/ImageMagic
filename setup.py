from setuptools import setup,find_packages
from ImageMagic import _version

setup(
    name='ImageMagic',
    version=_version.__version__,
    packages=find_packages(),
    url='https://github.com/asxez/ImageMagic',
    license='GNU GPL 3.0',
    author='asxe',
    author_email='2973918177@qq.com',
    description='图像处理库（包括但不限于图像）【Image processing libraries (including but not limited to images)】',
    long_description='It is a neat image processing library, and you can even achieve what you want with just one line of code, such as text-to-image or image content recognition (OCR), and more!',
    install_requires=[
        'Pillow',
        'requests',
        'loguru',
        'numpy',
        'pandas',
    ],
)
