
import sys, logging, unittest
import setsolver as ss
from setsolver import SetImage, Pattern, Shape


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


class TestShape(unittest.TestCase):

    def testFilledSquiggleShape(self):
        self.assertEqual(SetImage("test/01.gif").shape, Shape.SQUIGGLE)
        self.assertEqual(SetImage("test/02.gif").shape, Shape.SQUIGGLE)
        self.assertEqual(SetImage("test/03.gif").shape, Shape.SQUIGGLE)

    def testFilledDiamondShape(self):
        self.assertEqual(SetImage("test/10.gif").shape, Shape.DIAMOND)
        self.assertEqual(SetImage("test/11.gif").shape, Shape.DIAMOND)
        self.assertEqual(SetImage("test/12.gif").shape, Shape.DIAMOND)

    def testFilledOvalShape(self):
        self.assertEqual(SetImage("test/19.gif").shape, Shape.OVAL)
        self.assertEqual(SetImage("test/20.gif").shape, Shape.OVAL)
        self.assertEqual(SetImage("test/21.gif").shape, Shape.OVAL)


    def testLinesSquiggleShape(self):
        self.assertEqual(SetImage("test/28.gif").shape, Shape.SQUIGGLE)
        self.assertEqual(SetImage("test/29.gif").shape, Shape.SQUIGGLE)
        self.assertEqual(SetImage("test/30.gif").shape, Shape.SQUIGGLE)

    def testLinesDiamondShape(self):
        self.assertEqual(SetImage("test/37.gif").shape, Shape.DIAMOND)
        self.assertEqual(SetImage("test/38.gif").shape, Shape.DIAMOND)
        self.assertEqual(SetImage("test/39.gif").shape, Shape.DIAMOND)

    def testLinesOvalShape(self):
        self.assertEqual(SetImage("test/49.gif").shape, Shape.OVAL)
        self.assertEqual(SetImage("test/50.gif").shape, Shape.OVAL)
        self.assertEqual(SetImage("test/51.gif").shape, Shape.OVAL)


    def testBlankSquiggleShape(self):
        self.assertEqual(SetImage("test/55.gif").shape, Shape.SQUIGGLE)
        self.assertEqual(SetImage("test/56.gif").shape, Shape.SQUIGGLE)
        self.assertEqual(SetImage("test/57.gif").shape, Shape.SQUIGGLE)

    def testBlankDiamondShape(self):
        self.assertEqual(SetImage("test/67.gif").shape, Shape.DIAMOND)
        self.assertEqual(SetImage("test/68.gif").shape, Shape.DIAMOND)
        self.assertEqual(SetImage("test/69.gif").shape, Shape.DIAMOND)

    def testBlankOvalShape(self):
        self.assertEqual(SetImage("test/79.gif").shape, Shape.OVAL)
        self.assertEqual(SetImage("test/80.gif").shape, Shape.OVAL)
        self.assertEqual(SetImage("test/81.gif").shape, Shape.OVAL)


class TestAllImages(unittest.TestCase):

    def testCategoriseAll(self):
        for i in range(1,82):
            img = SetImage("test/%02d.gif"%i)
            self.assertTrue(img.count in [1,2,3])
            self.assertTrue(img.shape in [1,2,3])
            self.assertTrue(img.colour in [1,2,3])
            self.assertTrue(img.pattern in [1,2,3])


class TestSolutions(unittest.TestCase):

    def checkSolutions(self, imgs, ans):
        for i in range(len(imgs)): 
            imgs[i].pos = i

        calc = ss.calcsets(imgs)
        sols = [((a.gridx, a.gridy),(b.gridx, b.gridy), (c.gridx, c.gridy)) 
                 for (a,b,c) in calc]

        for a in ans:
            self.assertTrue(a in sols)

    def test20090920(self):
        imgs = [SetImage("test/76.gif"),
                SetImage("test/36.gif"),
                SetImage("test/09.gif"),
                SetImage("test/38.gif"),
                SetImage("test/52.gif"),
                SetImage("test/47.gif"),
                SetImage("test/51.gif"),
                SetImage("test/43.gif"),
                SetImage("test/33.gif"),
                SetImage("test/60.gif"),
                SetImage("test/02.gif"),
                SetImage("test/11.gif")]
        ans = [((2, 1), (3, 2), (3, 4)),
               ((1, 1), (1, 3), (1, 4)),
               ((1, 4), (2, 1), (3, 1)),
               ((2, 1), (2, 2), (2, 3)),
               ((1, 1), (1, 2), (3, 4)),
               ((2, 2), (2, 4), (3, 1))]
        self.checkSolutions(imgs, ans)


    def test20090919(self):
        imgs = [SetImage("test/17.gif"),
                SetImage("test/74.gif"),
                SetImage("test/33.gif"),
                SetImage("test/04.gif"),
                SetImage("test/73.gif"),
                SetImage("test/05.gif"),
                SetImage("test/13.gif"),
                SetImage("test/71.gif"),
                SetImage("test/24.gif"),
                SetImage("test/16.gif"),
                SetImage("test/58.gif"),
                SetImage("test/44.gif")]
        ans = [((1, 1), (2, 4), (3, 4)),
               ((2, 2), (2, 3), (3, 1)),
               ((1, 2), (2, 2), (3, 4)),
               ((1, 3), (2, 2), (3, 3)),
               ((1, 1), (1, 3), (2, 1)),
               ((1, 2), (1, 3), (3, 2))]
        self.checkSolutions(imgs, ans)


if __name__ == '__main__':
    #logging.root.setLevel(logging.DEBUG)
    unittest.main()
