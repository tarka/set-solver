
import sys
from PIL import Image
from colorsys import rgb_to_hsv, hsv_to_rgb
from functools import partial

sys.setrecursionlimit(10000)

def pxToFloat(px):
    return (float(px[0])/255,float(px[1])/255,float(px[2])/255)

def pxToInt(px):
    return (int(px[0]*255), int(px[1]*255), int(px[2]*255))

# Return a new image which has had fn applied to each pixel
def pxfilter(img, fn):
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

# All pixels not of color => white
def tocolor(rgb, px):
    if px != rgb:
        return (255,255,255)
    else:
        return px

 # 1. If the color of node is not equal to target-color, return.
 # 2. If the color of node is equal to replacement-color, return.
 # 3. Set the color of node to replacement-color.
 # 4. Perform Flood-fill (west of node, target-color, replacement-color).
 #    Perform Flood-fill (east of node, target-color, replacement-color).
 #    Perform Flood-fill (north of node, target-color, replacement-color).
 #    Perform Flood-fill (south of node, target-color, replacement-color).
 # 5. Return.
def flood(img, target, replacement, sx, sy, x=0, y=0):
    if img[x,y] != target: return
    if img[x,y] == replacement: return
    img[x,y] = replacement
    if x-1 >= 0: flood(img, target, replacement, sx, sy, x-1, y)
    if x+1 < sx: flood(img, target, replacement, sx, sy, x+1, y)
    if y-1 >= 0: flood(img, target, replacement, sx, sy, x, y-1)
    if y+1 < sy: flood(img, target, replacement, sx, sy, x, y+1)

class SetImage(object):
    
    def __init__(self, giffile):
        img = Image.open(giffile)
        self.img = img.convert()     # RGB by default
        self.bwimg = pxfilter(pxfilter(self.img, toGreyscale), partial(threshold, 0.6))

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

    def linecount(self):
        trans = 0
        size = self.bwimg.size
        for x in range(size[0]):
            prev = self.bwimg.getpixel((x,0))
            ttrans = 0
            for y in range(size[1]):
                p = self.bwimg.getpixel((x,y))
                if prev != p:
                    print x,prev,p
                    ttrans += 1
                    prev = p

            if ttrans > trans:
                trans = ttrans

        return trans

