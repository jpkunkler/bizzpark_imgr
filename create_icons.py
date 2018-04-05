import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

# create directory to hold output files
directory = "icons/"
if not os.path.exists(directory):
    os.makedirs(directory)

def createIcon(num):
	fnt = ImageFont.truetype("OpenSans-Bold.ttf", size=150)

	W, H = (200,200)

	# our number format is 01-09 and then 10-25
	# so we need to add a zero-digit to our integers < 10!
	if num < 10:
		msg = "0" + str(num)
	else:
		msg = str(num)

	im = Image.new("RGB",(W,H), (255,0,0))
	draw = ImageDraw.Draw(im)
	draw.rectangle(((0, 199), (199, 0)), outline=(255,255,255))
	w, h = fnt.getsize(msg)
	draw.text(((W-w)/2,(H-h)/2 - 20), msg, font=fnt,fill=(255, 255, 255))

	im.save("icons/{}.png".format(msg), "PNG")

for i in range(1, 25):
	createIcon(i)
