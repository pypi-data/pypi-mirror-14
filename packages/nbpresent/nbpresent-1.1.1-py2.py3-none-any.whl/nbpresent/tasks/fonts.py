import sys
import shutil
from glob import glob
from os.path import exists
from subprocess import Popen

from ._env import (
    FONTS,
    IS_WIN,
    join,
    node_bin,
)


def lato(*bits):
    return


FACES = {
    "lato": {
        "base": node_bin("..", "node_modules", "lato-font"),
        "faces": {
            "medium": glob(lato("fonts", "lato-medium", "*.ttf"))[0]
        }
    }
}


def main(**opts):

    for font_name, font_details in FACES.items():
        font_out_dir = join(FONTS, font_name)

        if not exists(font_out_dir):
            shutil.makedirs(font_out_dir)

        for face, fname in font_details["faces"]:
            with open(join(font_out_dir, "{}.woff2".format(face))) as woff2:
                with open(fname, "b") as ttf:
                    Popen([node_bin("ttf2woff2")],
                          stdin=ttf,
                          stdout=woff2,
                          shell=IS_WIN).wait()

    return 0

if __name__ == "__main__":
    sys.exit(main())
