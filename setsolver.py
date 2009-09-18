
from PIL import Image
from colorsys import rgb_to_hsv, hsv_to_rgb
from functools import partial

def pxToFloat(px):
    return (float(px[0])/255,float(px[1])/255,float(px[2])/255)

def pxToInt(px):
    return (int(px[0]*255), int(px[1]*255), int(px[2]*255))

# Apply a function to every pixel, returning a new image/pixaccess pair
def filter(img, fn):
    new = img.copy()
    size = new.size
    for x in range(size[0]):
        for y in range(size[1]):
            new.putpixel((x,y), fn(new.getpixel((x,y))))
    return new

# Convert to greyscale by removing saturation and hue, and averaging
# RGB to be V
def toGreyscale(px):
    fpx = pxToFloat(px)
    rgb = hsv_to_rgb(0,0, reduce(lambda a,b: a+b, fpx)/3.0)
    return pxToInt(rgb)

# All px above val == white, all below == black
def threshold(th, px):
    v = rgb_to_hsv(*pxToFloat(px))[2]
    if v < th:
        return (0,0,0)
    else:
        return (255,255,255)


class SetImage(object):
    
    def __init__(self, giffile):
        img = Image.open(giffile)
        self.img = img.convert()     # RGB by default
        self.gsimg = filter(self.img, toGreyscale)
        self.thimg = filter(self.gsimg, partial(threshold, 0.6))

    # FIXME: Make SetImage iterable?
    def color(self):
        # Count colour occurences, ignoring white. Return most common.
        d={}
        size = self.img.size
        for x in range(size[0]):
            for y in range(size[1]):
                p = self.img.getpixel((x,y))
                if p != (255,255,255):
                    if p in d:
                        d[p] += 1
                    else:
                        d[p] = 1
        getter = lambda a:a[1]
        return sorted(d.iteritems(), key=getter, reverse=True)[0][0] 

            

    
