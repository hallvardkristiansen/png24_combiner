from PIL import Image
from time import sleep
import glob
import os

current_dir = os.getcwd()
image_dir = current_dir + '/_input/images/'
text_dir = current_dir + '/_input/text/'
out_dir = current_dir + '/_output/'

imagesizes = {
  'VER': (768, 1366)
#  'HOR': (1536, 675),
#  'SQR': (800, 800),
#  'DIN': (4961, 3508)
}

imageFiles = [f for f in glob.glob(image_dir + '*.png')]
textFiles = [f for f in glob.glob(text_dir + '*.png')]
imageFiles.sort()
textFiles.sort()

def filename_as_array(filepath):
  s = filepath.split('/')
  fname = s.pop()
  return fname.split('_')


for imageFile in imageFiles:
  raw_grphcimg = Image.open(imageFile)
  imgf = filename_as_array(imageFile)
  
  for size in imagesizes.keys():
    if (imageFile.find(size) != -1):
      bgimg = Image.new('RGBA', imagesizes[size], 'WHITE')
      raw_grphcimg = raw_grphcimg.convert('RGBA')
      raw_grphcimg = raw_grphcimg.crop((0, 0, imagesizes[size][0], imagesizes[size][1]))
      grphcimg = Image.alpha_composite(bgimg, raw_grphcimg)
      
      for textFile in textFiles:
        if (textFile.find(size) != -1):
          raw_textimg = Image.open(textFile)
          raw_textimg = raw_textimg.convert('RGBA')
          textimg = raw_textimg.crop((0, 0, imagesizes[size][0], imagesizes[size][1]))
          
          newimg = Image.alpha_composite(grphcimg, textimg)
          
          textf = filename_as_array(textFile)
          filename = out_dir + imgf[0] + imgf[1] + '_' + textf[0] + textf[1] + '_' + size + '.png'
          
          newimg.save(filename)
          print('produced', filename)
          sleep(0.1)