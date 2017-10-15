from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageTk
import os

count = 0

def addIcon(filename, num, company, output_dir):
    # open source file as RGBA
    source = Image.open(filename).convert("RGBA")
    
    # select font
    #fnt = ImageFont.truetype('Open_Sans/OpenSans-bold.ttf', 150)
    fnt = ImageFont.truetype('OpenSans-bold.ttf', 150)

    # resize image
    source_width, source_height = source.size
    source = source.resize((1920, int((source_height / source_width) * 1920)), Image.ANTIALIAS)
    
    # icon size
    Width, Height = (200, 200)

    # define rectangle corners
    top_left = 100
    bottom_left = top_left + Height
    top_right, bottom_right = (top_left + Width, bottom_left + Width)

    # create icon layer
    button_img = Image.new("RGBA", source.size, (0,0,0,0))
    draw = ImageDraw.Draw(button_img)
    # draw the rectangle on our layer
    draw.rectangle(((top_left, bottom_left), (top_right, bottom_right)), fill=(255,0,0,160), outline=(255,255,255,255))
    
    # draw text inside rectangle
    w, h = draw.textsize(str(num), font=fnt)
    draw.text((((top_left + top_right) -w)/2, ((bottom_left + bottom_right)-w)/2 - 17.5), str(num), font=fnt, fill=(255, 255, 255, 255))

    # combine image layer and rectangle layer
    source = Image.alpha_composite(source, button_img)
    source = source.convert("RGB")

    #source.show()
    
    # save as "NUM_COUNT.jpg"
    global count
    count += 1
    outfile = "{}_{}_{}.jpg".format(str(num), str(company), str(count))
    directory = os.path.join(output_dir, "{}_{}".format(str(num), str(company)))

    if not os.path.exists(directory):
        os.makedirs(directory)

    return source, directory, outfile