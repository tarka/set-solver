
import sys, logging, unittest
import setsolver as ss
from setsolver import SetImage




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

    def testEmptySquiggleCount(self):
        self.assertEqual(SetImage("test/55.gif").count, 1)
        self.assertEqual(SetImage("test/56.gif").count, 2)
        self.assertEqual(SetImage("test/57.gif").count, 3)

    def testEmptyDiamondCount(self):
        self.assertEqual(SetImage("test/67.gif").count, 1)
        self.assertEqual(SetImage("test/68.gif").count, 2)
        self.assertEqual(SetImage("test/69.gif").count, 3)

    def testEmptyOvalCount(self):
        self.assertEqual(SetImage("test/79.gif").count, 1)
        self.assertEqual(SetImage("test/80.gif").count, 2)
        self.assertEqual(SetImage("test/81.gif").count, 3)


if __name__ == '__main__':
    #logging.root.setLevel(logging.DEBUG)
    unittest.main()
