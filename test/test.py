from ImageMagic import Image
from ImageMagic import Aocr



#Image.word_to_image('这里是你要转成图片的文本','./images/test1.png',fontPath='./fonts/字语时光体.ttf')

#Image.categorize_image('./testimages') #这里输入你的文件夹路径

#Image.convert('./images/test.png','webp','./images/test.webp')  #第一个参数是原文件路径，第二个是转换的格式，第三个是保存路径

#Image.equal_scale_image('./images/test.png','./images/equal.png',2)  #最后一个参数是变化倍数

#Image.customize_image('./images/test.png','./images/customize.png',1960,1080)

'''
text = Aocr.image_to_text('./images/test.png')
print(text)
'''

#Aocr.image_to_pdf('./images/test.png','./pdf/test.pdf')

'''
hocr = Aocr.image_to_hocr('./images/test.png')
print(hocr)
'''

'''
xml = Aocr.image_to_AltoXml('./images/test.png')
print(xml)
'''

'''
data = Aocr.get_image_data('./images/test.png')
print(data)
'''

'''
osd = Aocr.get_image_osd('./images/test.png')
print(osd)
'''

'''
boxs = Aocr.get_image_boxs('./images/test.png')
print(boxs)
'''

'''
lang = Aocr.check_languages()
print(lang)
'''

#Image.remove_same_images('./images')

'''
hash = Image.lbp_image_hash('./images/test.png')
print(hash)
'''

'''
hash = Image.p_image_hash('./images/test.png')
print(hash)
'''

'''
hash = Image.average_image_hash('./images/test.png')
print(hash)
'''
