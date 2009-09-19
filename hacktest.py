
# Quick-hack tests

import sys
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
ss.flooded(si.bwimg, (255,255,255), (255,0,0)).show()


