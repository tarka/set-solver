
import sys
import setsolver as ss
from setsolver import SetImage



si = SetImage("test/03.gif")
#si.img.show()
#si.gsimg.show()
#si.bwimg.show()
#print si.color()
#print si.linecount()

s2 = si.bwimg.copy()
#sx,sy = s2.size
ss.flood(s2.load(), (255,255,255), (255,0,0), *s2.size)
s2.show()

