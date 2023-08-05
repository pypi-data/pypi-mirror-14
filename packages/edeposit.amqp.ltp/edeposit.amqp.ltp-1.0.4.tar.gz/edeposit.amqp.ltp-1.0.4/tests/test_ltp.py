#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import shutil
import base64
import os.path


import ltp.settings as settings
from ltp import fn_composers
import ltp.ltp as ltp
import ltp.info_composer as icp


# Variables ===================================================================
DIRNAME = os.path.dirname(__file__) + "/data/"
OAI_FILENAME = DIRNAME + "oai_example.oai"


# Tests =======================================================================
def test_create_package_hierarchy():
    root_dir, original_dir, metadata_dir = ltp._create_package_hierarchy("/tmp")

    assert root_dir.startswith("/tmp")

    assert original_dir.startswith(root_dir)
    assert metadata_dir.startswith(root_dir)

    assert original_dir != metadata_dir

    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)


def test_create_ltp_package():
    aleph_record = open(OAI_FILENAME).read()

    package_path = ltp.create_ltp_package(
        aleph_record=aleph_record,
        book_id="121213",
        ebook_fn="somebook.epub",
        data=aleph_record,
        url="http://kitakitsune.org"
    )

    pid = icp._path_to_id(package_path)

    assert os.path.exists(package_path)
    assert os.path.exists(
        os.path.join(
            package_path,
            fn_composers.info_fn(pid)
        )
    )
    assert os.path.exists(
        os.path.join(
            package_path,
            fn_composers.checksum_fn(pid)
        )
    )

    shutil.rmtree(package_path)
