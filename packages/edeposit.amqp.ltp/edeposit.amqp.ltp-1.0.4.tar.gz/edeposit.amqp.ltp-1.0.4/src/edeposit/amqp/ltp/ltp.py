#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import uuid
import shutil
import base64
import os.path

import settings

import fn_composers
import info_composer
import checksum_generator
from marcxml2mods import marcxml2mods


# Functions & objects =========================================================
def _get_package_name(prefix=settings.TEMP_DIR, book_id=None):
    """
    Return package path. Use uuid to generate package's directory name.

    Args:
        book_id (str, default None): UUID of the book.
        prefix (str, default settings.TEMP_DIR): Where the package will be
               stored. Default :attr:`settings.TEMP_DIR`.

    Returns:
        str: Path to the root directory.
    """
    if book_id is None:
        book_id = str(uuid.uuid4())

    return os.path.join(prefix, book_id)


def _create_package_hierarchy(prefix=settings.TEMP_DIR, book_id=None):
    """
    Create hierarchy of directories, at it is required in specification.

    `root_dir` is root of the package generated using :attr:`settings.TEMP_DIR`
    and :func:`_get_package_name`.

    `orig_dir` is path to the directory, where the data files are stored.

    `metadata_dir` is path to the directory with MODS metadata.

    Args:
        book_id (str, default None): UUID of the book.
        prefix (str, default settings.TEMP_DIR): Where the package will be
               stored. Default :attr:`settings.TEMP_DIR`.

    Warning:
        If the `root_dir` exists, it is REMOVED!

    Returns:
        list of str: root_dir, orig_dir, metadata_dir
    """
    root_dir = _get_package_name(book_id=book_id, prefix=prefix)

    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)

    os.mkdir(root_dir)

    original_dir = os.path.join(root_dir, "original")
    metadata_dir = os.path.join(root_dir, "metadata")

    os.mkdir(original_dir)
    os.mkdir(metadata_dir)

    return root_dir, original_dir, metadata_dir


def create_ltp_package(aleph_record, book_id, ebook_fn, data, url,
                       urn_nbn=None):
    """
    Create LTP package as it is specified in specification v1.0 as I understand
    it.

    Args:
        aleph_record (str): XML containing full aleph record.
        book_id (str): UUID of the book.
        ebook_fn (str): Original filename of the ebook.
        data (str/bytes): Ebook's content.
        url (str): URL of the publication used when the URL can't be found in
                   `aleph_record`.
        urn_nbn (str, default None): URN:NBN.

    Returns:
        str: Name of the package's directory in ``/tmp``.
    """
    root_dir, orig_dir, meta_dir = _create_package_hierarchy(book_id=book_id)

    # create original file
    original_fn = os.path.join(
        orig_dir,
        fn_composers.original_fn(book_id, ebook_fn)
    )
    with open(original_fn, "wb") as f:
        f.write(data)

    # create metadata files
    metadata_filenames = []
    records = marcxml2mods(marc_xml=aleph_record, uuid=book_id, url=url)
    for cnt, mods_record in enumerate(records):
        fn = os.path.join(
            meta_dir,
            fn_composers.volume_fn(cnt)
        )

        with open(fn, "w") as f:
            f.write(mods_record)

        metadata_filenames.append(fn)

    # collect md5 sums
    md5_fn = os.path.join(root_dir, fn_composers.checksum_fn(book_id))
    checksums = checksum_generator.generate_hashfile(root_dir)
    with open(md5_fn, "w") as f:
        f.write(checksums)

    # create info file
    info_fn = os.path.join(root_dir, fn_composers.info_fn(book_id))
    with open(info_fn, "w") as f:
        f.write(
            info_composer.compose_info(
                root_dir=root_dir,
                files=[original_fn] + metadata_filenames,
                hash_fn=md5_fn,
                aleph_record=aleph_record,
                urn_nbn=urn_nbn,
            )
        )

    return root_dir
