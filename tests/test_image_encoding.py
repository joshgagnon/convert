#!/usr/bin/env python
# -*- coding: utf-8 -*-
import data_to_png
import json
from io import BytesIO
import unittest


class TestImageEncoding(unittest.TestCase):

    def test_image_encoding(self):
        test_obj = {
            "message": "value∂"
        }
        string = json.dumps(test_obj)
        output = BytesIO()
        data_to_png.string_to_png(string, output)
        output.seek(0)
        result = data_to_png.png_to_string(output)

        self.assertEqual(test_obj['message'], json.loads(result)['message'])

