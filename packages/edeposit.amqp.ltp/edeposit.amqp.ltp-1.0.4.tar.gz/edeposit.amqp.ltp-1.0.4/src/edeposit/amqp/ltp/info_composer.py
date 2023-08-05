#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import time
import os.path
import hashlib

import xmltodict
from odictliteral import odict
from remove_hairs import remove_hairs
from marcxml_parser import MARCXMLRecord


# Functions & classes =========================================================
def _path_to_id(path):
    """
    Name of the root directory is used as ``<packageid>`` in ``info.xml``.

    This function makes sure, that :func:`os.path.basename` doesn't return
    blank string in case that there is `/` at the end of the `path`.

    Args:
        path (str): Path to the root directory.

    Returns:
        str: Basename of the `path`.
    """
    if path.endswith("/"):
        path = path[:-1]

    return os.path.basename(path)


def _calc_dir_size(path):
    """
    Calculate size of all files in `path`.

    Args:
        path (str): Path to the directory.

    Returns:
        int: Size of the directory in bytes.
    """
    dir_size = 0
    for (root, dirs, files) in os.walk(path):
        for fn in files:
            full_fn = os.path.join(root, fn)
            dir_size += os.path.getsize(full_fn)

    return dir_size


def _get_localized_fn(path, root_dir):
    """
    Return absolute `path` relative to `root_dir`.

    When `path` == ``/home/xex/somefile.txt`` and `root_dir` == ``/home``,
    returned path will be ``/xex/somefile.txt``.

    Args:
        path (str): Absolute path beginning in `root_dir`.
        root_dir (str): Absolute path containing `path` argument.

    Returns:
        str: Local `path` when `root_dir` is considered as root of FS.
    """
    local_fn = path
    if path.startswith(root_dir):
        local_fn = path.replace(root_dir, "", 1)

    if not local_fn.startswith("/"):
        return "/" + local_fn

    return local_fn


def compose_info(root_dir, files, hash_fn, aleph_record, urn_nbn=None):
    """
    Compose `info` XML file.

    Info example::

        <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
        <info>
            <created>2014-07-31T10:58:53</created>
            <metadataversion>1.0</metadataversion>
            <packageid>c88f5a50-7b34-11e2-b930-005056827e51</packageid>
            <mainmets>mets.xml</mainmets>
            <titleid type="ccnb">cnb001852189</titleid>
            <titleid type="isbn">978-80-85979-89-6</titleid>
            <collection>edeposit</collection>
            <institution>nakladatelství Altar</institution>
            <creator>ABA001</creator>
            <size>1530226</size>
            <itemlist itemtotal="1">
                <item>\data\Denik_zajatce_Sramek_CZ_v30f-font.epub</item>
            </itemlist>
            <checksum type="MD5" checksum="ce076548eaade33888005de5d4634a0d">
                \MD5.md5
            </checksum>
        </info>

    Args:
        root_dir (str): Absolute path to the root directory.
        files (list): Absolute paths to all ebook and metadata files.
        hash_fn (str): Absolute path to the MD5 file.
        aleph_record (str): String with Aleph record with metadata.

    Returns:
        str: XML string.
    """
    # compute hash for hashfile
    with open(hash_fn) as f:
        hash_file_md5 = hashlib.md5(f.read()).hexdigest()

    schema_location = "http://www.ndk.cz/standardy-digitalizace/info11.xsd"
    document = odict[
        "info": odict[
            "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "@xsi:noNamespaceSchemaLocation": schema_location,

            "created": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "metadataversion": "1.0",
            "packageid": _path_to_id(root_dir),

            # not used in SIP
            # "mainmets": _get_localized_fn(metadata_fn, root_dir),

            "titleid": None,
            "collection": "edeposit",
            "institution": None,
            "creator": None,
            "size": _calc_dir_size(root_dir) / 1024,  # size in kiB
            "itemlist": odict[
                "@itemtotal": "2",
                "item": map(
                    lambda x: _get_localized_fn(x, root_dir),
                    files
                )
            ],
            "checksum": odict[
                "@type": "MD5",
                "@checksum": hash_file_md5,
                "#text": _get_localized_fn(hash_fn, root_dir)
            ],
        ]
    ]

    # get informations from MARC record
    record = MARCXMLRecord(aleph_record)

    # get publisher info
    publisher = unicode(record.get_publisher(), "utf-8")
    if record.get_publisher(None):
        document["info"]["institution"] = remove_hairs(publisher)

    # get <creator> info
    creator = record.getDataRecords("910", "a", False)
    alt_creator = record.getDataRecords("040", "d", False)
    document["info"]["creator"] = creator[0] if creator else alt_creator[-1]

    # collect informations for <titleid> tags
    isbns = record.get_ISBNs()

    ccnb = record.getDataRecords("015", "a", False)
    ccnb = ccnb[0] if ccnb else None

    if any([isbns, ccnb, urn_nbn]):  # TODO: issn
        document["info"]["titleid"] = []

    for isbn in isbns:
        document["info"]["titleid"].append({
            "@type": "isbn",
            "#text": isbn
        })

    if ccnb:
        document["info"]["titleid"].append({
            "@type": "ccnb",
            "#text": ccnb
        })

    if urn_nbn:
        document["info"]["titleid"].append({
            "@type": "urnnbn",
            "#text": urn_nbn
        })

    # TODO: later
    # if issn:
    #     document["info"]["titleid"].append({
    #         "@type": "issn",
    #         "#text": issn
    #     })

    # remove unset options
    unset_keys = [
        key
        for key in document["info"]
        if key is None
    ]
    for key in unset_keys:
        del document[key]

    xml_document = xmltodict.unparse(document, pretty=True)
    return xml_document.encode("utf-8")
