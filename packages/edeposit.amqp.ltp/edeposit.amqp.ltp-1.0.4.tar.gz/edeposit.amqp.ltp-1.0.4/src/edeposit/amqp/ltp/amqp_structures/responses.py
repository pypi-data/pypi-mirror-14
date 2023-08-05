#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & classes =========================================================
class TrackingResponse(namedtuple("TrackingResponse", ["book_id",
                                                       "exported",
                                                       "error"])):
    """
    Result of the :class:`.TrackingRequest`.

    Attributes:
        book_id (str): ID of the book.
        exported (bool): True if the book was successfully exported.
        error (str): Type of error if the export failed.
    """
