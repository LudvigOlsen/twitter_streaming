"""
Specific errors I know how to handle.

"""

from collections import defaultdict

SPECIFIC_MSG = defaultdict(str, {
    420: " You are being rate limited by Twitter.",
    500: " Someone broke twitter...! Maybe Doomsday?",
    502: " Missing description of error.",
    503: " Missing description of error.",
    504: " Missing description of error.",
    "dump_error": "Could not dump database.",
    "unknown": " Unknown exception!"})
