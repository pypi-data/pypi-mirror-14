from PIL import Image
from pyLibrary import convert
from pyLibrary.maths import Math

im = Image.open("C:/Users/kyle/Desktop/colorwheel.png")
pix = im.load()
print im.size


for y in Math.range(44.0, 670.0, 31.3):
    line = ""
    coord=""
    for x in Math.range(61.0, 1188.0, 31.3):
        xy=int(Math.round(x, decimal=0)), int(Math.round(y, decimal=0))
        c = pix[xy[0], xy[1]]
        coord += str(xy)+",   "
        line += '"' + convert.int2hex(c[0], 2) + convert.int2hex(c[1], 2) + convert.int2hex(c[2], 2) + '", '
    # print coord+"\n"+line + "\n"
    print "["+line[:-2]+"],"


