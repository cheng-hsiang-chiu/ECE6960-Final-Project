# Halftone CMYK Decomposition for Colour Image

import numpy as np
from PIL import Image
import sys
import os

#Decomposition the input image to three color shares
def CMY_DeColor(input_image,outputDireName):
  input_matrix = np.asarray(input_image)
  outfile1 = Image.new("CMYK", [dimension for dimension in input_image.size])
  outfile2 = Image.new("CMYK", [dimension for dimension in input_image.size])
  outfile3 = Image.new("CMYK", [dimension for dimension in input_image.size])


  for x in range(0, input_image.size[0], 1):
    for y in range(0, input_image.size[1], 1):
      sourcepixel = input_image.getpixel((x, y))
      #print("sourcepixel:",sourcepixel)
      #print("input_image:",input_image.getpixel)
      outfile1.putpixel((x, y),(sourcepixel[0],0,0,0))
      outfile2.putpixel((x, y),(0,sourcepixel[1],0,0))
      outfile3.putpixel((x, y),(0,0,sourcepixel[2],0))

  outfile1.save(outputDireName+'/C.jpg')
  outfile2.save(outputDireName+'/M.jpg')
  outfile3.save(outputDireName+'/Y.jpg')

  print("CMY color Decomposition Done!")

  return input_matrix



#Convert c, m, k images to halfton image
def ConvertToHalftone(outputDireName):
  image1 = Image.open(outputDireName+"/C.jpg").convert('1')
  image2 = Image.open(outputDireName+"/M.jpg").convert('1')
  image3 = Image.open(outputDireName+"/Y.jpg").convert('1')

  hf1 = Image.new("CMYK", [dimension for dimension in image1.size])
  hf2 = Image.new("CMYK", [dimension for dimension in image1.size])
  hf3 = Image.new("CMYK", [dimension for dimension in image1.size])

  for x in range(0, image1.size[0]):
    for y in range(0, image1.size[1]):
      pixel_color1 = image1.getpixel((x, y))
      pixel_color2 = image2.getpixel((x, y))
      pixel_color3 = image3.getpixel((x, y))
      if pixel_color1 == 255:
        hf1.putpixel((x, y),(255,0,0,0))
      else:
        hf1.putpixel((x, y),(0,0,0,0))

      if pixel_color2 == 255:
        hf2.putpixel((x, y),(0,255,0,0))
      else:
        hf2.putpixel((x, y),(0,0,0,0))

      if pixel_color3 == 255:
        hf3.putpixel((x, y),(0,0,255,0))
      else:
        hf3.putpixel((x, y),(0,0,0,0))

  hf1.save(outputDireName+'/C_halftone.jpg')
  hf2.save(outputDireName+'/M_halftone.jpg')
  hf3.save(outputDireName+'/Y_halftone.jpg')

  print("Halftone Conversion Done!")



def generateShares(outputDireName):
  image1 = Image.open(outputDireName+'/C_halftone.jpg').convert('CMYK')
  image2 = Image.open(outputDireName+'/M_halftone.jpg').convert('CMYK')
  image3 = Image.open(outputDireName+'/Y_halftone.jpg').convert('CMYK')

  share1 = Image.new("CMYK", [dimension * 2 for dimension in image1.size])
  share2 = Image.new("CMYK", [dimension * 2 for dimension in image2.size])
  share3 = Image.new("CMYK", [dimension * 2 for dimension in image3.size])
  shareMask = Image.new("CMYK", [dimension * 2 for dimension in image3.size])

  for x in range(0, image1.size[0]):
    for y in range(0, image1.size[1]):

      #print("image 1 C:",image1.getpixel((x,y))[0])
      #print("image 1 M:",image1.getpixel((x,y))[1])
      #print("image 1 Y:",image1.getpixel((x,y))[2])
      #print("image 1 K:",image1.getpixel((x,y))[3])
      
      shareMask.putpixel((x * 2, y * 2), (0,0,0,255))
      shareMask.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
      shareMask.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
      shareMask.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,255))
      
      pixelcolor = image1.getpixel((x, y))

      if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] <= 100:
        share1.putpixel((x * 2, y * 2), (255,0,0,0))
        share1.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
        share1.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
        share1.putpixel((x * 2 + 1, y * 2 + 1), (255,0,0,0))

      else:
        share1.putpixel((x * 2, y * 2), (0,0,0,0))
        share1.putpixel((x * 2 + 1, y * 2), (255,0,0,0))
        share1.putpixel((x * 2, y * 2 + 1), (255,0,0,0))
        share1.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

      pixelcolor = image2.getpixel((x, y))

      if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] <= 100:
        share2.putpixel((x * 2, y * 2), (0,255,0,0))
        share2.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
        share2.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
        share2.putpixel((x * 2 + 1, y * 2 + 1), (0,255,0,0))

      else:
        share2.putpixel((x * 2, y * 2), (0,0,0,0))
        share2.putpixel((x * 2 + 1, y * 2), (0,255,0,0))
        share2.putpixel((x * 2, y * 2 + 1), (0,255,0,0))
        share2.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

      pixelcolor = image3.getpixel((x, y))

      if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] <= 100:
        share3.putpixel((x * 2, y * 2), (0,0,255,0))
        share3.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
        share3.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
        share3.putpixel((x * 2 + 1, y * 2 + 1), (0,0,255,0))

      else:
        share3.putpixel((x * 2, y * 2), (0,0,0,0))
        share3.putpixel((x * 2 + 1, y * 2), (0,0,255,0))
        share3.putpixel((x * 2, y * 2 + 1), (0,0,255,0))
        share3.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

  share1.save(outputDireName+'/C_share.jpg')
  share2.save(outputDireName+'/M_share.jpg')
  share3.save(outputDireName+'/Y_share.jpg')
  shareMask.save(outputDireName+'/shareMask.jpg')

  print("Generated Shares!")

if __name__ == "__main__":
    
    #print("Save input image as 'Input.png' in the same folder as this file\n")
    n = len(sys.argv)
    if(n <= 1):
         sys.exit("Please select an input file") 
    inputFile = sys.argv[1]
    try:
     
        input_image = Image.open(inputFile)

    except FileNotFoundError:
    	print("Input file not found!")
    	exit(0)

    print("Image uploaded successfully!")
    print("Input image size (in pixels) : ", input_image.size)   
    #create a folder to put outfiles
    directory = "outputs"
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, directory)
    if not os.path.exists(final_directory):
      os.makedirs(final_directory)

    input_matrix = CMY_DeColor(input_image,directory)
    ConvertToHalftone(directory)
    generateShares(directory)
