#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import traceback
from slacker import Slacker

from logging import getLogger
logger = getLogger(__name__)

__KEYS = ["EXCEPTION_SLACKER_%s" % k for k in ["TOKEN", "CHANNEL", "NAME"]]

def notification(type, value, stacktrace):
    if not all([k in os.environ.keys() for k in __KEYS]):
        # original error shown after this
        raise StandardError("exception_slacker is imported, but %s aren't found in ENV." % ','.join(__KEYS))

    slack = Slacker(token=os.environ["EXCEPTION_SLACKER_TOKEN"])
    slack.chat.post_message(channel=os.environ["EXCEPTION_SLACKER_CHANNEL"],
                            text="*%s*\n%s\n%s\n```\n%s\n```"
                            % (value, __file__, type, ''.join(traceback.format_tb(stacktrace))),
                            icon_emoji=":exclamation:",
                            username=os.environ["EXCEPTION_SLACKER_NAME"])

sys.excepthook = notification
