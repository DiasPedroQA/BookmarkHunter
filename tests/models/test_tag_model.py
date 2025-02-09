# pylint: disable=C0114, C0115, C0116

import unittest
from bs4 import BeautifulSoup
from app.models.tag_model import AnalisadorHTML


class TestAnalisadorHTML(unittest.TestCase):
    def test_init_with_valid_html(self):
        analisador = self._extracted_from_test_init_with_empty_html_2(
            "<html><body><h1>Test</h1></body></html>"
        )
        self.assertEqual(analisador.soup.h1.string, "Test")

    def test_init_with_empty_html(self):
        analisador = self._extracted_from_test_init_with_empty_html_2("")
        self.assertEqual(analisador.soup.string, None)

    # _TODO Rename this here and in `test_init_with_valid_html` and `test_init_with_empty_html`
    def _extracted_from_test_init_with_empty_html_2(self, arg0):
        html_content = arg0
        result = AnalisadorHTML(html_content)
        self.assertIsInstance(result.soup, BeautifulSoup)
        return result


if __name__ == "__main__":
    unittest.main()
