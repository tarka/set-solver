
import sys, re, urllib2
from StringIO import StringIO
import logging as log
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

class Colour(object):
    RED = 1
    GREEN = 2
    PURPLE = 3

class SetImage(object):
    
    def __init__(self, giffile, pos=None):
        self.pos = pos

        img = Image.open(giffile)
        self.img = img.convert()     # RGB by default
        self.bwimg = pxfilter(pxfilter(self.img, toGreyscale), partial(threshold, 0.6))

        self._colour = None
        self._count = None
        self._pattern = None
        self._shape = None
        self._spans = None

    def __cmp__(self, other):
        return cmp(self.pos, other.pos)

    @property
    def gridx(self):
        return (self.pos / 4) + 1

    @property
    def gridy(self):
        return (self.pos % 4) + 1

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
                (hue,sat,val) = rgb_to_hsv(*pxToFloat(p))
                if sat > 0.5:
                    if p in d:
                        d[p] += 1
                    else:
                        d[p] = 1
        getter = lambda a:a[1]
        
        col = sorted(d.iteritems(), key=getter, reverse=True)[0][0] 
        (hue,sat,val) = rgb_to_hsv(*pxToFloat(col))

        log.debug("Pos %s rgb = %s, hsv = %s"%(self.pos, col, hue))
        if hue < 0.1:
            self._colour = Colour.RED
        elif hue > 0.3 and hue < 0.35:
            self._colour = Colour.GREEN
        elif hue > 0.77 and hue < 0.81:
            self._colour = Colour.PURPLE
        else:
            # NFI
            raise RuntimeError("Couldn't work out the color for %s: %s - %s"%(self.pos, col, hsv))
        
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

        # Calculate the overall variance trend by reducing contiguous
        # trends to single values
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
        if vdiff == [-1, 1, -1, 1]:
            # Wavy == squiggle:
            self._shape = Shape.SQUIGGLE

        elif vdiff == [-1, 1] and zratio < 0.5:
            # Up then down, but has large contiguous area == oval
            self._shape = Shape.OVAL

        elif vdiff == [-1, 1] and zratio > 0.70:
            # Up then down, but not especially flat == diamond            
            self._shape = Shape.DIAMOND

        else:
            # NFI
            log.error("Couldn't work out the shape of %s: %s, %s" % (self.pos, vdiff, zratio))
            raise RuntimeError("Couldn't work out the shape of %s"%self.pos)

        return self._shape


setbase = "http://www.setgame.com/puzzle/"
setpage = "set.htm"
prevpage = "set_puzzle_yesterdays_solution.htm"
imgre = re.compile("(\.\./images/setcards/small/\d+\.gif)")

def fetch(url):
    log.debug("Fetching %s"%url)
    try:
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla")
        fd = urllib2.build_opener().open(req)
    except IOError, e:
        print "failed:",e
        sys.exit()
    return fd
    
def fetchsets(prev=False):
    log.info("Fetching page")
    if prev:
        url = setbase+prevpage
    else:
        url = setbase+setpage

    pagefd = fetch(url)
    gifs = []
    for line in pagefd:
        match = imgre.search(line)
        if match != None:
            gifpath = match.group(0)
            log.info("Got img %s" % gifpath)
            gifs.append(gifpath)

    if prev:
        # Expect more from this page
        gifs = gifs[:12]

    if len(gifs) != 12:
        raise RuntimeError("Wrong no. of images: %s" % len(gifs))

    imgs = []
    pos = 0
    for i in gifs:
        log.info("Fetching img %s"%i)
        ifd = fetch(setbase+i)
        imgs.append(SetImage(StringIO(ifd.read()), pos=pos))
        pos += 1

    return imgs


def same(attr, a,b,c):
    aa = getattr(a, attr)
    ba = getattr(b, attr)
    ca = getattr(c, attr)
    same = aa == ba == ca
    log.debug("SAME %s: %s == %s == %s -> %s", attr, aa, ba, ca, same)
    return same


def different(attr, a,b,c):
    aa = getattr(a, attr)
    ba = getattr(b, attr)
    ca = getattr(c, attr)
    diff = aa != ba and ba != ca and ca != aa 
    log.debug("DIFF %s: %s != %s != %s -> %s", attr, aa, ba, ca, diff)
    return diff


def printcoords(a, b, c):
    print "(",a.gridx, a.gridy, ") (", b.gridx, b.gridy, ") (", c.gridx, c.gridy,")"


def isset(a,b,c):
    for attr in ["colour", "count", "pattern", "shape"]:
        if (not same(attr, a, b, c)) and (not different(attr, a, b, c)):
            log.debug("Reject (%s,%s,%s): %s"%(a.pos, b.pos, c.pos, attr))
            return False
    return True

def calcsets(prev=False):
    imgs = fetchsets(prev=prev)
    sol = set()
    for a in imgs:
        for b in imgs:
            for c in imgs:
                if a.pos == b.pos or b.pos == c.pos or c.pos == a.pos:
                    continue

                if isset(a,b,c):
                    sol.add(tuple(sorted([a,b,c])))

    for (a, b, c) in sol:
        printcoords( a, b, c)

