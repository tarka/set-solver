
# Quick-hack tests

import sys, logging
import setsolver as ss
from setsolver import SetImage


si = SetImage("test/55.gif")
#si.img.show()
#si.gsimg.show()
#si.bwimg.show()
#print si.color()
#print si.linecount()

#s2 = si.bwimg.copy()
#sx,sy = s2.size
#ss.flood(s2.load(), (255,255,255), (255,0,0), *s2.size)
#ss.flooded(si.bwimg, (255,255,255), (255,0,0)).show()


#SetImage("test/67.gif").bwimg.show()
#SetImage("test/57.gif").bwimg.show()
#print SetImage("test/57.gif").shape
#print SetImage("test/67.gif").shape
#print SetImage("test/49.gif").shape

logging.root.setLevel(logging.INFO)
#logging.root.setLevel(logging.DEBUG)

#imgs = ss.fetchsets()
#for i in imgs:
#    print getattr(i,"colour")

#cl = [i.colour for i in imgs]
#print cl


ss.calcsets(prev=False)
