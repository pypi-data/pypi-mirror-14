#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import shutil
import pytest
import tempfile

from ltp import checksum_generator as cg


# Variables ===================================================================
DIRNAME = ""


# Functions & objects =========================================================
def create_dir_structure():
    dirname = tempfile.mkdtemp()
    subdir = dirname + "/xex/"

    os.mkdir(subdir)

    with open(dirname + "/info.xml", "w") as f:
        f.write("hello")

    with open(subdir + "/xex.xx", "w") as f:
        f.write("this is info file")

    with open(dirname + "/somefile.txt", "w") as f:
        f.write("somecontent")

    with open(subdir + "/somefile.txt", "w") as f:
        f.write("somecontent")

    return dirname


# Tests =======================================================================
def setup_module(module):
    global DIRNAME

    DIRNAME = create_dir_structure()


def test_get_required_fn():
    assert cg._get_required_fn("./hello", "./") == "/hello"
    assert cg._get_required_fn("/home/xex/hello", "/home/xex/") == "/hello"

    with pytest.raises(ValueError):
        assert cg._get_required_fn("./hello", "/home") == "/hello"
        assert cg._get_required_fn("/home/xex/hello", "./") == "/hello"


def test_generate_checksums():
    checksums = cg.generate_checksums(DIRNAME)

    assert checksums == {
        '/somefile.txt': '18c0864b36d60f6036bf8eeab5c1fe7d',
        '/xex/somefile.txt': '18c0864b36d60f6036bf8eeab5c1fe7d',
        '/xex/xex.xx': 'e77b911e47bb73f6d69a70d246489fb0'
    }


def test_generate_hashfile():
    hashfile = cg.generate_hashfile(DIRNAME)

    assert hashfile == """18c0864b36d60f6036bf8eeab5c1fe7d /somefile.txt
18c0864b36d60f6036bf8eeab5c1fe7d /xex/somefile.txt
e77b911e47bb73f6d69a70d246489fb0 /xex/xex.xx
"""


def teardown_module(module):
    global DIRNAME

    shutil.rmtree(DIRNAME)
