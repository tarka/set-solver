
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


# All pixels not of colour => white
def tocolour(rgb, px):
    if px != rgb:
        return (255,255,255)
    else:
        return px


# Return new copy of image that has been flooded
def flooded(img, target, replacement):    
    i2 = img.copy()

    # 1. If the colour of node is not equal to target-colour, return.
    # 2. If the colour of node is equal to replacement-colour, return.
    # 3. Set the colour of node to replacement-colour.
    # 4. Perform Flood-fill (west of node, target, replacement).
    #    Perform Flood-fill (east of node, target, replacement).
    #    Perform Flood-fill (north of node, target, replacement).
    #    Perform Flood-fill (south of node, target, replacement).
    # 5. Return.
    def flood(img, target, replacement, sx, sy, x=0, y=0):
        if img[x,y] != target: return
        if img[x,y] == replacement: return
        img[x,y] = replacement
        if x-1 >= 0: flood(img, target, replacement, sx, sy, x-1, y)
        if x+1 < sx: flood(img, target, replacement, sx, sy, x+1, y)
        if y-1 >= 0: flood(img, target, replacement, sx, sy, x, y-1)
        if y+1 < sy: flood(img, target, replacement, sx, sy, x, y+1)

    flood(i2.load(), target, replacement, *i2.size)
    return i2


# Quick'n'dirty enum
class Pattern(object):
    LINES = 1
    BLANK = 2
    SOLID = 3

class Shape(object):
    SQUIGGLE = 1
    DIAMOND = 2
    OVAL = 3

class SetImage(object):
    
    def __init__(self, giffile):
        img = Image.open(giffile)
        self.img = img.convert()     # RGB by default
        self.bwimg = pxfilter(pxfilter(self.img, toGreyscale), partial(threshold, 0.6))
        self._colour = None
        self._count = None
        self._pattern = None
        self._shape = None
        self._spans = None

    # FIXME: Make SetImage iterable?
    @property
    def colour(self):
        if self._colour != None: return self._colour

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
        
        self._colour = sorted(d.iteritems(), key=getter, reverse=True)[0][0] 
        return self._colour


    @property
    def count(self):
        if self._count != None: return self._count

        # Cache the spans of the shapes, they're needed for pattern
        # calculation
        self._spans = []

        # To count the shapes we flood-fill the non-shape parts of the
        # BW version of the image with a known color.  We then
        # ray-cast through the middle of the image and count the
        # transitions:
        fcol = (255,0,0)
        fimg = flooded(self.bwimg, (255,255,255), fcol)
        y = fimg.size[1]/2
        trans = 0
        prev = fcol
        span = None
        for x in range(fimg.size[0]):
            p = fimg.getpixel((x,y))
            if p != fcol and prev == fcol:
                # This is a rising edge; count
                trans += 1
                span = [x,None]
            elif p == fcol and prev != fcol:
                # Falling edge, save span
                span[1] = x
                self._spans.append(span)
            prev = p

        self._count = trans
        return self._count


    @property
    def spans(self):
        if self._spans != None: return self._spans

        # Spans are calculated as part of count
        count = self.count
        return self._spans


    @property
    def pattern(self):
        if self._pattern != None: return self._pattern

        # To determine to pattern we find the middle of a shape and
        # ray-cast through the BW image vertically.  The number of
        # transitions to black gives us the pattern.
        # FIXME: Very similar to the count routine, should merge
        span = self.spans[0]
        x = span[0] + ((span[1]-span[0]) / 2)

        white = (255,255,255)
        prev = white
        trans = 0
        for y in range(self.bwimg.size[1]):
            p = self.bwimg.getpixel((x,y))
            if prev == white and p != white:
                # White->Black edge
                trans += 1
            prev = p

        if trans == 1:
            self._pattern = Pattern.SOLID
        elif trans == 2:
            self._pattern = Pattern.BLANK
        elif trans > 5:  # Lines should be between 6-10 transitions
            self._pattern = Pattern.LINES
        else:
            raise RuntimeError("Not enough transitions in shape: %s"%trans)
        return self._pattern


    @property
    def shape(self):
        if self._shape != None: return self._shape

        # Guesstimate the shape; find the top and bottom of one of the
        # shapes, then sample the variance of one side.

        # Find leftmost part of edge
        # def findedge():
        #     for x in range(self.bwimg.size[0]):
        #         for y in range(self.bwimg.size[1]):
        #             if self.bwimg.getpixel((x,y)) != (255,255,255):
        #                 return x
        # lstart = findedge()
        
        # Scan to find top/bottom edge
        span = self.spans[0]
        def findtop(sy, ey, step):
            for y in range(sy, ey, step):
                for x in range(span[0],span[1]+1):
                    if self.bwimg.getpixel((x,y)) != (255,255,255):
                        return y

        top = findtop(0,self.bwimg.size[1], 1)
        bottom = findtop(self.bwimg.size[1]-1, 0, -1)

        # Scan left side, recording values
        def findleft(y):
            #for x in range(span[0],span[1]+1):
            for x in range(0,self.bwimg.size[0]):
                if self.bwimg.getpixel((x,y)) != (255,255,255):
                    return x

        left = []
        for y in range(top, bottom+1):
            left.append(findleft(y))

        # Calc variation
        prev = None
        diff = []
        for x in left:
            if prev != None:
                d = x-prev
                diff.append(d)
            prev = x
        
        # Calc zero to non-zero variation 
        zcount = 0.0
        nzcount = 0.0
        for d in diff:
            if d == 0: 
                zcount += 1
            else:
                nzcount +=1 
        zratio = nzcount / zcount

        # Calculate the overall variance trend 
        vdiff=[]
        prev = 0
        for d in diff:
            if d < 0 and not prev < 0:
                vdiff.append(-1)
                prev = -1
            elif d > 0 and not prev > 0:
                vdiff.append(1)
                prev = 1

        # Guesstimate:
        if vdiff == [-1, 1,-1, 1]:
            # Wavy == squiggle:
            self._shape = Shape.SQUIGGLE

        elif vdiff == [-1, 1] and zratio < 0.5:
            # Up then down, but has large contiguous area == oval
            self._shape = Shape.OVAL

        elif vdiff == [-1, 1] and zratio > 0.75:
            # Up then down, but not especially flat == diamond            
            self._shape = Shape.DIAMOND

        else:
            # NFI
            raise RuntimeError("Couldn't work out the shape")

        return self._shape

    
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

