"""
Almost of this code is written by github copilot, wow.
"""

import argparse
import glob
import os
import sys
import tkinter as tk
import logging
from logging import getLogger
from tkinter.filedialog import askdirectory
from typing import List

from PIL import Image

logger = getLogger('gifmaker')
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(
    logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', "%Y-%m-%dT%H:%M:%S"))
logger.addHandler(sh)
logger.setLevel(logging.INFO)

supported_formats = ['png', 'jpg', 'jpeg', 'bmp', 'tiff']

def warn_print(message: str, level: str='WARNING'):
    if level == 'WARNING':
        logger.warning('\033[38;5;009m' + message + '\033[0m')
    elif level == 'ERROR':
        logger.error('\033[38;5;009m' + message + '\033[0m')

def create_gif(
    input_dir: List[str],
    output_file: str,
    fps: int,
    force_rescale: bool):
    """
    Creates a gif from a directory of images.
    """
    images = []
    resolution = None
    for filename in glob.iglob(input_dir + '/*'):
        ext = os.path.splitext(filename)[1][1:]
        if os.path.isfile(filename) and ext.lower() in supported_formats:
            image = Image.open(os.path.join(input_dir, filename))
            if resolution is None:
                resolution = image.size        
            elif image.size != resolution:
                if force_rescale:
                    image = image.resize(resolution)
                else:
                    filename = filename.replace('\\', '/')
                    warn_print('Resolution of image \'{}\' does not match the resolution of the first image. Skipping image.'.format(filename))
                    continue
            images.append(image)
    if len(images) == 0:
        warn_print('No images found in {}'.format(input_dir), level='ERROR')
        sys.exit(1)
    elif len(images) == 1:
        warn_print('Only one image found in {}'.format(input_dir), level='ERROR')
        sys.exit(1)
    images[0].save(output_file, save_all=True, append_images=images[1:], duration=1000//fps, loop=0)
    logger.info('\033[38;5;010mCreated gif {} with {} frames at {} fps\033[0m'.format(output_file, len(images), fps))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--output_file", "-o", help="name of output gif file", type=str, default="output.gif")
    parser.add_argument("--force_rescale", '-f',
                        help="If set, the image will be resized to the same resolution as the first image, even if it is a different image size. ",
                        action="store_true")
    parser.add_argument("--fps", help="frames per second", type=int, default=1)
    args = parser.parse_args()

    root = tk.Tk()
    root.withdraw()
    dirpath = askdirectory(title='Select directory with images', initialdir=os.getcwd())

    if dirpath:
        opath, filename = os.path.split(args.output_file)
        if opath:
            create_gif(dirpath, args.output_file, args.fps, args.force_rescale)
        else:
            create_gif(dirpath, os.path.join(dirpath, args.output_file), args.fps, args.force_rescale)

