import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance



def createIcon(num, size):

	# create directory to hold output files
	directory = "icons/{}/".format(size)
	if not os.path.exists(directory):
		os.makedirs(directory)

	# check for size (properties: sm = small, lg = large, xl = extra-large)
	if size == "sm":
		fnt = ImageFont.truetype("OpenSans-Bold.ttf", size=150)
		W, H = (200,200)
		offset = 20
	elif size == "lg":
		fnt = ImageFont.truetype("OpenSans-Bold.ttf", size=375)
		W, H = (500,500)
		offset = 50
	elif size == "xl":
		fnt = ImageFont.truetype("OpenSans-Bold.ttf", size=750)
		W, H = (1000,1000)
		offset = 100

	# our number format is 01-09 and then 10-25
	# so we need to add a zero-digit to our integers < 10!
	if num < 10:
		msg = "0" + str(num)
	else:
		msg = str(num)

	im = Image.new("RGB",(W,H), (255,0,0))
	draw = ImageDraw.Draw(im)
	draw.rectangle(((0, W-1), (H-1, 0)), outline=(255,255,255))
	w, h = fnt.getsize(msg)
	draw.text(((W-w)/2,(H-h)/2 - offset), msg, font=fnt,fill=(255, 255, 255))

	im.save("icons/{}/{}.png".format(size, msg), "PNG")

for i in range(1, 21):
	createIcon(i, "xl")
	createIcon(i, "lg")
	createIcon(i, "sm")
