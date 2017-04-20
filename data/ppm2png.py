#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Boyuan Deng <bryanhsudeng@gmail.com>

"""
convert all ppm images to png format in GTSDB folder (recursively)
and delete the original ppm files.
"""

import argparse
import fileinput
import os
import sys

from wand.image import Image

parser = argparse.ArgumentParser()
parser.add_argument("path",
                    help="directory containing ppm images (and subfolders)")
args = parser.parse_args()

for root, dirs, files in os.walk(args.path):
    for name in files:
        file_path = os.path.join(root, name)
        file_path_without_ext, file_extension = os.path.splitext(file_path)

        if file_extension == '.ppm':
            with Image(filename=file_path) as img:
                img.format = 'png'
                img.save(filename=file_path_without_ext+'.'+'png')

            os.remove(file_path)

# replace all "ppm" with "png" in label file "gt.txt"
label_file_path = os.path.join(args.path, 'TrainIJCNN2013', 'gt.txt')

for line in fileinput.input(label_file_path, inplace=True):
    line = line.replace('ppm', 'png')
    print line
    sys.stdout.write(line)

# remove ReadMe.txt in testing set
readme_full_path = os.path.join(args.path, 'TestIJCNN2013', 'ReadMe.txt')

if os.path.exists(readme_full_path):
    os.remove(readme_full_path)
