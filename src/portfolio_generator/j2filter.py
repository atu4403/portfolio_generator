from datetime import datetime
import arrow
from arrow.parser import ParserError


def _ar(s):
    if type(s) is list:
        return arrow.get(datetime(*s[:6]))
    return arrow.get(s)


def to(s: str, tz: str = "local"):
    try:
        a = _ar(s)
        return a.to(tz)
    except ParserError:
        return s


def fmt(s: str, f: str = "YYYY-MM-DD"):
    try:
        a = _ar(s)
        return a.format(f)
    except ParserError:
        return s


filters = {"to": to, "fmt": fmt}
