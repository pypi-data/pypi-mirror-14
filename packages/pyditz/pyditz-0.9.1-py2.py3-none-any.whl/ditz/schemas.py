"""
Data validation schemas.
"""

from voluptuous import (Schema, Any, All, MultipleInvalid,
                        ExactSequence, Length, In, Coerce)

from datetime import datetime
from six import text_type

from .flags import TYPE, STATUS, RELSTATUS, DISPOSITION
from .util import DitzError


def validate(obj, schema, filename=None):
    "Check a DitzObject is a valid Ditz object."

    try:
        data = to_dict(obj)
        data = schema(data)
        set_data(obj, data)

    except MultipleInvalid as e:
        path = '.'.join(map(text_type, e.path))
        err = "%s: %s" % (path, e.msg)

        if filename:
            raise DitzError("%s: %s" % (filename, err))
        else:
            raise DitzError(err)


def to_dict(obj):
    "Convert object to a dict, recursively."

    if hasattr(obj, "__dict__"):
        obj = {attr: to_dict(value) for attr, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        obj = [to_dict(item) for item in obj]

    return obj


def set_data(obj, data):
    "Set object attributes from data, recursively."

    if hasattr(obj, "__dict__"):
        for attr, value in data.items():
            subobj = getattr(obj, attr)
            if not set_data(subobj, value):
                obj.__dict__[attr] = value

        return True

    elif isinstance(obj, list):
        for idx, value in enumerate(data):
            subobj = obj[idx]
            if not set_data(subobj, value):
                obj[idx] = value

        return True

    return False


def Option(options, **kw):
    "Validator for one of a set of options."
    msg = kw.pop('msg', None)
    names = [str(v) for v in options]
    return In(options, msg=msg or "expected one of " + ", ".join(names))


def TypeOrNone(type, **kw):
    "Validator for a particular type, or None."
    return Any(type, None, msg=kw.pop('msg', None))


def Text(value):
    "Convert value to text."
    return None if value is None else text_type(value)


# Declare basic Ditz types.
text = Coerce(Text)
issuetype = Option(TYPE.keys())
status = Option(STATUS.keys())
relstatus = Option([None] + list(RELSTATUS.keys()))
disposition = Option([None] + list(DISPOSITION.keys()))
event = All(Length(min=4, max=4, msg="expected a list of length 4"),
            ExactSequence([datetime, text, text, text]))

# Declare schemas for each file object.
issue = Schema({'title': text,
                'desc': text,
                'type': issuetype,
                'component': text,
                'release': TypeOrNone(text),
                'reporter': text,
                'status': status,
                'disposition': disposition,
                'creation_time': datetime,
                'references': [text],
                'id': text,
                'log_events': [event]}, required=True)

component = Schema({'name': text}, required=True)

release = Schema({'name': text,
                  'status': relstatus,
                  'release_time': TypeOrNone(datetime),
                  'log_events': [event]}, required=True)

project = Schema({'name': text,
                  'version': text,
                  'components': [component],
                  'releases': [release]}, required=True)
