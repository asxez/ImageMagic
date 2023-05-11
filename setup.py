from setuptools import setup,find_packages
from ImageMagic import _version



with open('README_EN.md','r',encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ImageMagic',
    version=_version.__version__,
    packages=find_packages(exclude='test'),
    url='https://github.com/asxez/ImageMagic',
    license='GNU GPL 3.0',
    author='asxe',
    author_email='2973918177@qq.com',
    description='图像处理库（包括但不限于图像）【Image processing libraries (including but not limited to images)】',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Python library, image process, imagemagic, ocr function and more! ',
    install_requires=[
        'Pillow',
        'requests',
        'loguru',
        'numpy',
        'pandas',
    ],
)
