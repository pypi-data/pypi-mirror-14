#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from ltp import fn_composers


# Variables ===================================================================
# Functions & objects =========================================================


# Tests =======================================================================
def test_get_suffix():
    assert fn_composers._get_suffix("/home/xex/somefile.txt") == "txt"
    assert fn_composers._get_suffix("somefile.txt") == "txt"
    assert fn_composers._get_suffix("/somefile.txt") == "txt"
    assert fn_composers._get_suffix("somefile") == "somefile"
    assert fn_composers._get_suffix("/home/xex/somefile") == "somefile"


def test_get_original_fn():
    assert fn_composers.original_fn("111", "somebook.epub") == "oc_111.epub"
    assert fn_composers.original_fn(111, "somebook.pdf") == "oc_111.pdf"


def test_get_metadata_fn():
    assert fn_composers.metadata_fn("111") == "mods_111.xml"
    assert fn_composers.metadata_fn(111) == "mods_111.xml"


def test_get_checksum_fn():
    assert fn_composers.checksum_fn("111") == "MD5_111.md5"
    assert fn_composers.checksum_fn(111) == "MD5_111.md5"


def test_get_info_fn():
    assert fn_composers.info_fn("111") == "info_111.xml"
    assert fn_composers.info_fn(111) == "info_111.xml"
