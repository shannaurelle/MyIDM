# 
#
#

import filecmp
import os

CURRENT_WORKING_DIR = os.path.dirname(__file__)

def test(dir):
    for file in os.listdir(dir):
        if not os.path.isfile(file): continue
        if file.endswith('.py'): continue
        if not filecmp.cmp(file, f'expected/{file}'): return f'Failed at {file}'

    return "Ran successfully"

if __name__ == '__main__':
    print(test(CURRENT_WORKING_DIR))