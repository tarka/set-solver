
from PIL import Image
from colorsys import rgb_to_hsv, hsv_to_rgb 

def pxToFloat(px):
    return (float(px[0])/255,float(px[1])/255,float(px[2])/255)

def pxToInt(px):
    return (int(px[0]*255), int(px[1]*255), int(px[2]*255))

# Convert to greyscale by removing saturation and hue, and averaging
# RGB to be V
def toGreyscale(px):
    fpx = pxToFloat(px)
    rgb = hsv_to_rgb(0,0, reduce(lambda a,b: a+b, fpx)/3.0)
    return pxToInt(rgb)

class SetImage(object):
    
    def __init__(self, giffile):
        img = Image.open(giffile)
        self.img = img.convert()     # RGB by default
        self.pix = self.img.load()        # Pixel-array representation
        self.gsimg, self.gspix = self.filter(toGreyscale)

    
    # Apply a function to every pixel, returning a new image/pixaccess pair
    def filter(self, fn):
        new = self.img.copy()
        npx = new.load()
        size = new.size
        for x in range(size[0]):
            for y in range(size[1]):
                npx[x,y]=fn(npx[x,y])
        return (new,npx)

    
