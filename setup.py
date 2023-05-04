from setuptools import setup,find_packages


setup(
    name='ImageMagic',
    version='0.1.5',
    packages=find_packages(),
    url='https://github.com/asxez/ImageMagic',
    license='MIT',
    author='asxe',
    author_email='2973918177@qq.com',
    description='图像处理库（包括但不限于图像）',
    install_requires=[
        'Pillow',
        'requests',
        'loguru',
        'numpy',
        'pandas',
    ]
)
