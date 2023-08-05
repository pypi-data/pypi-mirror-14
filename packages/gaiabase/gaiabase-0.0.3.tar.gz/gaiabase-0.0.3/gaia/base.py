# -*- coding: utf-8 -*-

import os

def find_path():
    testpath = os.path.join(os.path.dirname(__file__), '..')
    while True:
        testpath = os.path.join(testpath, '..')
        venvpath = os.path.join(testpath, '.py')
        if os.path.exists(venvpath):
            break
    return testpath


