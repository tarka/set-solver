
import sys, logging, unittest
import setsolver as ss
from setsolver import SetImage, Pattern




class TestCount(unittest.TestCase):

    def testFilledSquiggleCount(self):
        self.assertEqual(SetImage("test/01.gif").count, 1)
        self.assertEqual(SetImage("test/02.gif").count, 2)
        self.assertEqual(SetImage("test/03.gif").count, 3)

    def testFilledDiamondCount(self):
        self.assertEqual(SetImage("test/10.gif").count, 1)
        self.assertEqual(SetImage("test/11.gif").count, 2)
        self.assertEqual(SetImage("test/12.gif").count, 3)

    def testFilledOvalCount(self):
        self.assertEqual(SetImage("test/19.gif").count, 1)
        self.assertEqual(SetImage("test/20.gif").count, 2)
        self.assertEqual(SetImage("test/21.gif").count, 3)

    def testBlankSquiggleCount(self):
        self.assertEqual(SetImage("test/55.gif").count, 1)
        self.assertEqual(SetImage("test/56.gif").count, 2)
        self.assertEqual(SetImage("test/57.gif").count, 3)

    def testBlankDiamondCount(self):
        self.assertEqual(SetImage("test/67.gif").count, 1)
        self.assertEqual(SetImage("test/68.gif").count, 2)
        self.assertEqual(SetImage("test/69.gif").count, 3)

    def testBlankOvalCount(self):
        self.assertEqual(SetImage("test/79.gif").count, 1)
        self.assertEqual(SetImage("test/80.gif").count, 2)
        self.assertEqual(SetImage("test/81.gif").count, 3)

class TestPattern(unittest.TestCase):

    def testFilledSquigglePattern(self):
        self.assertEqual(SetImage("test/01.gif").pattern, Pattern.SOLID)
        self.assertEqual(SetImage("test/02.gif").pattern, Pattern.SOLID)
        self.assertEqual(SetImage("test/03.gif").pattern, Pattern.SOLID)

    def testFilledDiamondPattern(self):
        self.assertEqual(SetImage("test/10.gif").pattern, Pattern.SOLID)
        self.assertEqual(SetImage("test/11.gif").pattern, Pattern.SOLID)
        self.assertEqual(SetImage("test/12.gif").pattern, Pattern.SOLID)

    def testFilledOvalPattern(self):
        self.assertEqual(SetImage("test/19.gif").pattern, Pattern.SOLID)
        self.assertEqual(SetImage("test/20.gif").pattern, Pattern.SOLID)
        self.assertEqual(SetImage("test/21.gif").pattern, Pattern.SOLID)


    def testLinesSquigglePattern(self):
        self.assertEqual(SetImage("test/28.gif").pattern, Pattern.LINES)
        self.assertEqual(SetImage("test/29.gif").pattern, Pattern.LINES)
        self.assertEqual(SetImage("test/30.gif").pattern, Pattern.LINES)

    def testLinesDiamondPattern(self):
        self.assertEqual(SetImage("test/37.gif").pattern, Pattern.LINES)
        self.assertEqual(SetImage("test/38.gif").pattern, Pattern.LINES)
        self.assertEqual(SetImage("test/39.gif").pattern, Pattern.LINES)

    def testLinesOvalPattern(self):
        self.assertEqual(SetImage("test/49.gif").pattern, Pattern.LINES)
        self.assertEqual(SetImage("test/50.gif").pattern, Pattern.LINES)
        self.assertEqual(SetImage("test/51.gif").pattern, Pattern.LINES)


    def testBlankSquigglePattern(self):
        self.assertEqual(SetImage("test/55.gif").pattern, Pattern.BLANK)
        self.assertEqual(SetImage("test/56.gif").pattern, Pattern.BLANK)
        self.assertEqual(SetImage("test/57.gif").pattern, Pattern.BLANK)

    def testBlankDiamondPattern(self):
        self.assertEqual(SetImage("test/67.gif").pattern, Pattern.BLANK)
        self.assertEqual(SetImage("test/68.gif").pattern, Pattern.BLANK)
        self.assertEqual(SetImage("test/69.gif").pattern, Pattern.BLANK)

    def testBlankOvalPattern(self):
        self.assertEqual(SetImage("test/79.gif").pattern, Pattern.BLANK)
        self.assertEqual(SetImage("test/80.gif").pattern, Pattern.BLANK)
        self.assertEqual(SetImage("test/81.gif").pattern, Pattern.BLANK)


if __name__ == '__main__':
    #logging.root.setLevel(logging.DEBUG)
    unittest.main()
