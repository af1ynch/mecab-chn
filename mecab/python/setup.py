#!/usr/bin/env python

from distutils.core import setup, Extension, os


def cmd1(s):
    return os.popen(s).readlines()[0][:-1]


def cmd2(s):
    return cmd1(s).split()

setup(
    name="mecab",
    version="0.1",
    author="lynch",
    author_email="aflynch@126.com",
    description="chinese segmentation",
    packages=["mecab"],
    package_dir={"mecab": "mecab"},
    package_data={"mecab":["*.*"]},
    ext_modules=[
        Extension("_MeCab",
                  ["MeCab_wrap.cxx",],
                  include_dirs=cmd2("mecab-config --inc-dir"),
                  library_dirs=cmd2("mecab-config --libs-only-L"),
                  libraries=cmd2("mecab-config --libs-only-l"))]
)

