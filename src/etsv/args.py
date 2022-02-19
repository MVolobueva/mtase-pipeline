"""Some tools to handle ETSV with argparse."""


import argparse
import sys
from contextlib import suppress

from etsv import ETSVReader, ETSVWriter


class ETSVType:
    """"""#TODO

    def __init__(self, fields, mode="r"):
        if mode not in "rwxa":
            raise ValueError(f"unknown mode '{mode}'")
        self._mode = mode
        self._fileobj = None
        self.fields = fields
        self.params = dict()

    def __call__(self, value):
        if value == "-":
            fileobj = sys.stdin if self._mode == "r" else sys.stdout
        else:
            fileobj = open(value, self._mode)
        self._fileobj = fileobj
        return self

    def __iter__(self):
        return iter(self.params)

    def __enter__(self):
        self._fileobj = self._fileobj.__enter__()
        try:
            ETSVFile = ETSVReader if self._mode == "r" else ETSVWriter
            return ETSVFile(self._fileobj, self.fields, **self.params)
        except: # pylint: disable=bare-except
            if self._fileobj.__exit__(*sys.exc_info()):
                raise
            return None

    def __exit__(self, *args, **kwargs):
        return self._fileobj.__exit__(*args, **kwargs)


class _FieldType: # pylint: disable=too-few-public-methods
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        field = self.field
        field.header = value
        # in case of InputField try to assign index
        if hasattr(field, "index"):
            field.index = None
            with suppress(ValueError):
                column_number = int(value)
                field.index = column_number - 1
                field.header = None
        return value


class _NoAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        pass

    def format_usage(self):
        pass


class SetETSVParameter(argparse.Action):
    """"""#TODO

    def __init__(self, *args, master, parameter, **kwargs):
        self.master = master
        self.parameter = parameter
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if hasattr(namespace, self.master):
            obj = getattr(namespace, self.master)
        else:
            obj = dict()
            setattr(namespace, self.master, obj)
        if self.const is not None:
            values = self.const
        obj[self.parameter] = values


class StoreETSVType(argparse.Action):
    """"""#TODO

    def __call__(self, parser, namespace, values, option_string=None):
        if hasattr(namespace, self.dest):
            stub = getattr(namespace, self.dest)
            values.params.update(stub)
        setattr(namespace, self.dest, values)


def add_etsv_options(parser, parent, prefix="--"):
    """"""#TODO

    if not isinstance(parent, StoreETSVType):
        raise ValueError(f"bad `parent` type {type(parent)}")
    parser.add_argument(
        f"{prefix}force-title", master=parent.dest, action=SetETSVParameter,
        parameter="force_title", nargs=0, const=True, default=False,
        help="treat the first data line as a title line if it was not found"
        )
    parser.add_argument(
        f"{prefix}general-tsv", master=parent.dest, action=SetETSVParameter,
        parameter="extended_tsv", nargs=0, const=False, default=True,
        help="do not treat lines starting with '#' in a special way"
        )
    parser.add_argument(
        f"{prefix}maxsplit", master=parent.dest, action=SetETSVParameter,
        parameter="maxsplit", metavar="N", default=-1,
        help="split lines no more than the given number times"
        )


def add_field_options(parser, fields, prefix="--"):
    """"""#TODO

    for field in fields:
        metavar = "HEADER"
        help_ = f"set `{field.name}` column header"
        default = "default is '{field.header}'"
        if hasattr(field, "index"):
            metavar += "|NUMBER"
            help_ += " or number"
            if field.index is not None:
                default = "default is {field.index+1}"
        parser.add_argument(
            f"{prefix}{field.name}-column", action=_NoAction, metavar=metavar,
            type=_FieldType(field), help=f"{help_}, {default}"
            )
