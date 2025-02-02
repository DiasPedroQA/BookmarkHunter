# pylint: disable=C

import json
import unittest
from app.models.favorite_model import HtmlTag
from unittest.mock import MagicMock


class TestHtmlTag(unittest.TestCase):

    def setUp(self):
        self.html_line = (
            '<a href="https://example.com" add_date="1609459200">Example Link</a>'
        )
        self.html_tag = HtmlTag(tag_line=self.html_line)
        self.html_tag.timestamp_converter = MagicMock()
        self.html_tag.timestamp_converter.converter_timestamp = MagicMock(
            return_value="01/01/2021 00:00:00"
        )

    def test_process_line(self):
        self.html_tag.process_line()
        expected_data = [
            {
                "tag": "a",
                "attributes": {
                    "text_content": "Example Link",
                    "add_date": "01/01/2021 00:00:00",
                    "href": "https://example.com",
                },
            }
        ]
        self.assertEqual(self.html_tag.get_tags_data(), expected_data)

    def test_to_dict(self):
        self.html_tag.process_line()
        expected_data = [
            {
                "tag": "a",
                "attributes": {
                    "text_content": "Example Link",
                    "add_date": "01/01/2021 00:00:00",
                    "href": "https://example.com",
                },
            }
        ]
        self.assertEqual(self.html_tag.to_dict(), expected_data)

    def test_to_json(self):
        self.html_tag.process_line()
        expected_json = json.dumps(
            [
                {
                    "tag": "a",
                    "attributes": {
                        "text_content": "Example Link",
                        "add_date": "01/01/2021 00:00:00",
                        "href": "https://example.com",
                    },
                }
            ],
            indent=4,
            ensure_ascii=False,
        )
        self.assertEqual(self.html_tag.to_json(), expected_json)

    def test_process_line_with_h3_tag(self):
        html_line = '<h3 last_modified="1609459200" personal_toolbar_folder="true">Example Header</h3>'
        html_tag = HtmlTag(tag_line=html_line)
        html_tag.timestamp_converter = MagicMock()
        html_tag.timestamp_converter.converter_timestamp = MagicMock(
            return_value="01/01/2021 00:00:00"
        )
        html_tag.process_line()
        expected_data = [
            {
                "tag": "h3",
                "attributes": {
                    "text_content": "Example Header",
                    "add_date": "",
                    "last_modified": "01/01/2021 00:00:00",
                    "personal_toolbar_folder": "true",
                },
            }
        ]
        self.assertEqual(html_tag.get_tags_data(), expected_data)


if __name__ == "__main__":
    unittest.main()
