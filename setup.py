from setuptools import setup,find_packages
from ImageMagic import _version

setup(
    name='ImageMagic',
    version=_version.__version__,
    packages=find_packages(),
    url='https://github.com/asxez/ImageMagic',
    license='GNU GPL',
    author='asxe',
    author_email='2973918177@qq.com',
    description='图像处理库（包括但不限于图像）【Image processing libraries (including but not limited to images)】',
    long_description='For image processing, it currently supports text to picture,audio to text, and a combination of the two audio content to picture,image format conversion, image classification and OCR functions',
    install_requires=[
        'Pillow',
        'requests',
        'loguru',
        'numpy',
        'pandas',
    ]
)
