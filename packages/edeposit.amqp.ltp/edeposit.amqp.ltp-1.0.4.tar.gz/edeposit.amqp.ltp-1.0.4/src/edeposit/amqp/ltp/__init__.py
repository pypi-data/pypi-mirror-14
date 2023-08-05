#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import base64
import shutil
import os.path

import ltp
import settings

from amqp_structures import ExportRequest
from amqp_structures import TrackingRequest
from amqp_structures import TrackingResponse


# Functions & objects =========================================================
def _instanceof(instance, cls):
    """
    Check type of `instance` by matching ``.__name__`` with `cls.__name__`.
    """
    return type(instance).__name__ == cls.__name__


# Main program ================================================================
def reactToAMQPMessage(message, send_back):
    """
    React to given (AMQP) message. `message` is expected to be
    :py:func:`collections.namedtuple` structure from :mod:`.structures` filled
    with all necessary data.

    Args:
        message (object): One of the request objects defined in
                          :mod:`.structures`.
        send_back (fn reference): Reference to function for responding. This is
                  useful for progress monitoring for example. Function takes
                  one parameter, which may be response structure/namedtuple, or
                  string or whatever would be normally returned.

    Returns:
        object: Response class from :mod:`.structures`.

    Raises:
        ValueError: if bad type of `message` structure is given.
    """
    if _instanceof(message, ExportRequest):
        tmp_folder = ltp.create_ltp_package(
            aleph_record=message.aleph_record,
            book_id=message.book_uuid,
            urn_nbn=message.urn_nbn,
            ebook_fn=message.filename,
            url=message.url,
            data=base64.b64decode(message.b64_data)
        )

        # remove directory from export dir, if already there
        out_dir = os.path.join(
            settings.EXPORT_DIR,
            os.path.basename(message.book_uuid)
        )

        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

        shutil.move(tmp_folder, settings.EXPORT_PREFIX + out_dir)
        return True

    elif _instanceof(message, TrackingRequest):
        uuid = message.book_uuid

        status = [
            item.replace(uuid, "").replace("/", "")
            for item in os.listdir(settings.EXPORT_DIR)
            if uuid in item
        ]

        if not status:
            raise ValueError("UUID %s not found!" % uuid)

        status = status[0]

        success = ["ok", "success", "done"]
        success = sum(([x, x + "_"] for x in success), [])  # add _ to the end

        return TrackingResponse(
            book_id=uuid,
            exported=status.lower() in success,
            error=status,
        )

    raise ValueError(
        "Unknown type of request: '" + str(type(message)) + "'!"
    )
