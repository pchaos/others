# can all the webp file and convert them to jpg
from PIL import Image
import os

for (dirname, dirs, files) in os.walk("."):
     for filename in files:
         if filename.endswith('.webp'):
             print('found: ' + os.path.splitext(filename)[0])
             print('converting to: ' + os.path.splitext(filename)[0] + '.jpg')
             im = Image.open(filename).convert("RGB")
             im.save(os.path.splitext(filename)[0] + '.jpg', "jpeg")
             print('done converting…')
