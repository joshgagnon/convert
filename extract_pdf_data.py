from pdfrw import PdfReader
from pdfrw.uncompress import uncompress
from pdfrw.findobjs import page_per_xobj,find_objects
from pdfrw.objects import PdfName

import sys
import os
import io
from data_to_png import png_to_string
import json


def find_images(file):
    pages = PdfReader(file).pages
    for page in pages:
        for obj in find_objects(page):
            if obj.Subtype == PdfName.Image and obj['/Height'] == '1':
                try:
                    uncompress([obj], leave_raw=True)
                    result = obj.stream.decode('utf-16be')
                    yield result
                except Exception as e:
                    pass


if __name__ == '__main__':
    results = list(find_images(sys.argv[1]))
    for r in results:
        print(json.loads(r))