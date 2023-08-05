#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import shutil
import os.path

import pytest
import xmltodict

import ltp.ltp as ltp
import ltp.info_composer as icp


# Variables ===================================================================
DIRNAME = os.path.join(os.path.dirname(__file__), "data/")


# Fixtures ====================================================================
@pytest.fixture
def oai_file():
    with open(os.path.join(DIRNAME, "oai_example.oai")) as f:
        return f.read()


@pytest.fixture
def info_xml():
    return icp.compose_info(
        root_dir="/home/root_dir",
        files=[
            "/home/root_dir/data/ebook.epub",
            "/home/root_dir/meta/meta.xml",
        ],
        hash_fn=os.path.join(DIRNAME, "hashfile.md5"),
        aleph_record=oai_file(),
        urn_nbn="urn:nbn:azgabash"
    )


# Tests =======================================================================
def test_get_localized_fn():
    local_path = icp._get_localized_fn("/home/xex/somefile.txt", "/home")
    assert local_path == "/xex/somefile.txt"

    local_path = icp._get_localized_fn("/somefile.txt", "/")
    assert local_path == "/somefile.txt"

    local_path = icp._get_localized_fn("/xex/somefile.txt", "/home")
    assert local_path == "/xex/somefile.txt"

    local_path = icp._get_localized_fn("/home/xex/home/somefile.txt", "/home")
    assert local_path == "/xex/home/somefile.txt"

    local_path = icp._get_localized_fn("somefile.txt", "/azgabash")
    assert local_path == "/somefile.txt"


def test_path_to_id():
    assert icp._path_to_id("/xex/xax") == "xax"
    assert icp._path_to_id("/xex/xax/") == "xax"

    assert os.path.basename("/xex/xax/") == ""


def test_calc_dir_size():
    root_dir, original_dir, metadata_dir = ltp._create_package_hierarchy(
        "/tmp"
    )

    # create 3 files
    with open(os.path.join(root_dir, "root_file.txt"), "w") as f:
        f.write(1024 * "f")

    with open(os.path.join(original_dir, "original_file.txt"), "w") as f:
        f.write(1024 * "f")

    with open(os.path.join(metadata_dir, "meta_file.txt"), "w") as f:
        f.write(1024 * "f")

    # compute size of the files
    assert icp._calc_dir_size(root_dir) >= 3*1024

    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)


def test_order(info_xml):
    xdom = xmltodict.parse(info_xml)
    info = xdom["info"]

    assert info.keys() == [
        "@xmlns:xsi",
        "@xsi:noNamespaceSchemaLocation",
        "created",
        "metadataversion",
        "packageid",
        "titleid",
        "collection",
        "institution",
        "creator",
        "size",
        "itemlist",
        "checksum",
    ]


def test_compose_info(info_xml, oai_file):
    xdom = xmltodict.parse(info_xml)
    info = xdom["info"]
    created = info["created"]

    assert ":" in created
    assert "-" in created
    assert "T" in created
    assert len(created) >= 19
    assert info["metadataversion"] == "1.0"
    assert info["packageid"] == "root_dir"
    assert info["titleid"][0]["#text"] == "80-251-0225-4"
    assert info["titleid"][1]["#text"] == "cnb001492461"
    assert info["titleid"][2]["#text"] == "urn:nbn:azgabash"
    assert info["collection"] == "edeposit"
    assert info["institution"] == "Computer Press"
    assert info["creator"] == "ABA001"
    assert info["size"] == "0"
    assert info["itemlist"]["item"][0] == "/data/ebook.epub"
    assert info["checksum"]["#text"].endswith("hashfile.md5")
    assert info["checksum"]["@checksum"] == "18c0864b36d60f6036bf8eeab5c1fe7d"
