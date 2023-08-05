import unittest

from pyprint.Printer import Printer


class TestPrinter(Printer):

    def _print(self, output, somearg=""):
        return output + somearg


class PrinterTest(unittest.TestCase):

    def test_printer_interface(self):
        self.uut = Printer()
        self.assertRaises(NotImplementedError, self.uut.print, "test")

    def test_printer_concatenation(self):
        self.uut = TestPrinter()
        self.assertEqual(self.uut.print("hello",
                                        "world",
                                        delimiter=" ",
                                        end="-",
                                        somearg="then"), "hello world-then")
        self.assertEqual(self.uut.print("",
                                        "world",
                                        delimiter=" ",
                                        end="-",
                                        somearg="then"), " world-then")
        self.assertEqual(self.uut.print("hello",
                                        "world",
                                        delimiter="",
                                        end="-",
                                        somearg="then"), "helloworld-then")
        self.assertEqual(self.uut.print(end=""), "")
        self.assertEqual(self.uut.print(NotImplementedError, end=""),
                         "<class 'NotImplementedError'>")
        self.assertEqual(
            self.uut.print("", "", delimiter=NotImplementedError, end=""),
            "<class 'NotImplementedError'>")
        self.assertEqual(self.uut.print("", end=NotImplementedError),
                         "<class 'NotImplementedError'>")
