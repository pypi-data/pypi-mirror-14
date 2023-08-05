"""
The deadbeef module produces hexspeak for nefarious purposes.
For more information on hexspeak, read: https://en.wikipedia.org/wiki/Hexspeak.
"""

from .deadbeef import DEADBEEF, BADC0DE
_deadbeef = DEADBEEF()
get_string = _deadbeef.get_string
get_int = _deadbeef.get_int
skip = _deadbeef.skip
candidate_count = _deadbeef.candidate_count
