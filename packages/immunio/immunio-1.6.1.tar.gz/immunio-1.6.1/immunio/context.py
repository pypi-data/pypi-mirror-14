"""
Utility functions to calculate context hashes and a stack trace.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
import sys
import hashlib

from immunio.logger import log


THIS_DIR = os.path.dirname(__file__)

CONTEXT_CACHE = {}


def get_stack(limit=None):
    """
    Returns the current call stack.

    Based on CPython traceback.py & inspect.py but without the I/O operations
    to read the line of code.
    """
    f = sys._getframe(1)
    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    stack = []
    n = 0
    while f is not None and (limit is None or n < limit):
        lineno = f.f_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        stack.append((filename, lineno, name))
        f = f.f_back
        n = n + 1
    return stack


def get_context(additional_data=None, log_context_data=False, offset=0):
    def is_immunio_frame(frame):
        if "/immunio/" in frame[0]:
            path_part = frame[0].split("/immunio/")[-1]
            path = os.path.join(THIS_DIR, path_part)
            if os.path.exists(path):
                return True

        return False

    # Change the lineno of the first frame by offset; useful in unit tests.
    stack = [frame for frame in get_stack() if not is_immunio_frame(frame)]
    stack[0] = (stack[0][0], stack[0][1] + offset, stack[0][2],)
    stack_string = "\n".join(
        ":".join(str(s) for s in frame) for frame in stack)
    cache_key = hashlib.sha1(stack_string).hexdigest()
    if cache_key in CONTEXT_CACHE:
        loose_context = CONTEXT_CACHE[cache_key]["loose_context"]
        strict_context = CONTEXT_CACHE[cache_key]["strict_context"]
        stack = CONTEXT_CACHE[cache_key]["stack"]
        loose_stack = CONTEXT_CACHE[cache_key]["loose_stack"]

        if log_context_data:
            log.info("Stack contexts from cache")
    else:
        # Use ropes as they're faster than string concatenation
        loose_stack_rope = []
        loose_context_rope = []
        stack_rope = []
        strict_context_rope = []

        # drop the top frame as it's us, but retain the rest. Immunio frames
        # are filtered by the Gem regex.
        for frame in stack[0:]:
            # Reduce paths to just use the filename part.
            strict_path = os.path.basename(frame[0])

            stack_rope.append(
                ":".join([frame[0], str(frame[1]), frame[2]]))
            strict_context_rope.append(
                ":".join([strict_path, str(frame[1]), frame[2]]))

            # Remove pathname from the loose context. The goal here
            # is to prevent upgrading package versions from changing the
            # loose context key, so for instance users don't have to
            # rebuild their whitelists every time they update a package.
            loose_context_rope.append(
                ":".join([os.path.basename(frame[0]), frame[2]]))

            # Build a second seperate rope for the stack that
            # determines ou loose context key. This includes filenames
            # for usability -- just method names not being very good
            # for display purposes...
            loose_stack_rope.append(
                ":".join([frame[0], frame[2]]))

        stack = "\n".join(stack_rope)
        strict_stack = "\n".join(strict_context_rope)
        loose_stack = "\n".join(loose_stack_rope)

        if log_context_data:
            log.info("Strict context stack:\n%s", strict_stack)
            log.info("Loose context stack:\n%s", loose_stack)

        strict_context = hashlib.sha1(strict_stack).hexdigest()
        loose_context = hashlib.sha1(
            "\n".join(loose_context_rope)).hexdigest()

        CONTEXT_CACHE[cache_key] = {
            "strict_context": strict_context,
            "loose_context": loose_context,
            "stack": stack,
            "loose_stack": loose_stack,
        }

    # Mix in additional context data
    if additional_data:
        if log_context_data:
            log.info("Additional context data:\n%s", additional_data)

        strict_context = hashlib.sha1(
            strict_context + additional_data).hexdigest()

    return strict_context, loose_context, stack, loose_stack
