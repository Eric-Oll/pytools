import unittest
from pytools.dataframe.display import HTMLConnect

class TestHTMLConnect(unittest.TestCase):

    def test_get_html_model(self):
        self.assertEqual("<!DOCTYPE html>", HTMLConnect.get_html_model()[:15])

    def test_get_default_css(self):
        self.assertEqual("/*CSS For Dataframe*/", HTMLConnect.get_default_css()[:21])

    def test_get_javascript(self):
        self.assertEqual("// Javascript for HTML Connect DataFrame", HTMLConnect.get_javascript()[:40])

if __name__ == '__main__':
    unittest.main()
