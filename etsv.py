"""ETSV file wrappers.

ETSV (extended TSV) format:
#  - comments, skipped by the parser;
## - metadata (only before title line), stored separately;
#: - a title line (the last one before TSV data), TAB-separated;
all other lines are ordinary TSV (TAB-separated values) data.

The module contains wrappers for file objects which allows to read
specified fields from a TSV line into a dict, and to write values from
a dict to a file. `InputField` and `OutputField` objects describe column
positions, names and value formats.
"""


from contextlib import suppress
from typing import Callable, Dict, Iterable
from typing import Any, Optional, Union


class Field:
    """"""#TODO

    name: str
    header: Optional[str]

    def __init__(self, name, header=None):
        self.name = name
        self.header = header

    def __str__(self):
        return self.header

    def __eq__(self, obj: Any) -> bool:
        return self.name == obj

    def __hash__(self) -> int:
        return hash(self.name)


class InputField(Field):
    """Input TSV field.

    Keeps information about a column of an input TSV file,
    requred to parse values from this column.
    """

    index: int

    def __init__(self, name: str, index_or_header: Union[int, str],
                 value_type: Callable[[str], Any] = str) -> None:
        super().__init__(name, header=index_or_header)
        if isinstance(index_or_header, int):
            self.index = index_or_header
            self.header = None
        else:
            self.index = None
        self._value_type = value_type

    def take_index(self, column_headers: Iterable[str]) -> None:
        """Determine the column index by the column header."""
        for index, header in enumerate(column_headers):
            if header == self.header:
                self.index = index
                break
        else:
            raise ValueError(f"can't find the column named '{self.header}'")

    def parse_value(self, values) -> Any:
        """Find the value, transform and return it as a (key, value) pair."""
        return self.name, self._value_type(values[self.index])


class OutputField(Field): # pylint: disable=too-few-public-methods
    """Output TSV field.

    Keeps information about a column of an output TSV file,
    requred to format values for printing.
    """

    def __init__(self, name: str, header: str,
                 value_format: Union[str, Callable[[Any], str]] = str) -> None:
        super().__init__(name, header=header)
        if hasattr(value_format, "format"):
            self._value_format = value_format.format
        else:
            self._value_format = value_format

    def format_value(self, values):
        """"""#TODO
        return self._value_format(values[self.name])


class _OneStepBackIterator:
    """Iterator wrapper that allows to take one step back."""

    def __init__(self, iterator):
        self._iterator = iterator
        self._stepped_back = False
        self._last = None

    def __next__(self):
        if self._stepped_back:
            self._stepped_back = False
        else:
            self._last = next(self._iterator)
        return self._last

    def step_back(self):
        """"""#TODO
        if self._stepped_back:
            raise TypeError("only one step back is allowed")
        self._stepped_back = True


class ETSVReader:
    """ETSV reader class."""

    def __init__(self, fileobj, fields, **kwargs: Any) -> None:
        self.metadata = kwargs.pop("metadata", [])
        self.title = None
        self._params = dict()
        self._params["force_title"] = kwargs.pop("force_title", False)
        self._params["extended_tsv"] = kwargs.pop("extended_tsv", True)
        self._params["maxsplit"] = kwargs.pop("maxsplit", -1)
        if kwargs:
            args = ", ".join(kwargs)
            end = "" if len(kwargs) == 1 else "s"
            raise TypeError(f"unknown keyword argument{end}: {args}")
        for field in fields:
            if field.index is None:
                self._params["force_title"] = True
                break
        self._fileobj = fileobj
        self._fields = fields
        self._iterator = None
        with suppress(StopIteration):
            self._prepare()

    def _prepare(self) -> None:
        # prepare the object for parsing TSV data
        self._iterator = _OneStepBackIterator(iter(self._fileobj))
        if self._params["extended_tsv"]:
            line = next(self._iterator)
            while line.startswith("#"):
                if line.startswith("#:"):
                    self.title = self._split_line(line[2:])
                elif line.startswith("##"):
                    self.metadata.append(line[2:])
                line = next(self._iterator)
            self._iterator.step_back()
        if not self.title and self._params["force_title"]:
            self.title = self._split_line(next(self._iterator))
        for field in self._fields:
            if field.index is None:
                field.take_index(self.title or [])

    def _split_line(self, line):
        return line.strip("\n").split("\t", self._params["maxsplit"])

    def __iter__(self):
        return self

    def __next__(self) -> Dict[str, Any]:
        line = next(self._iterator)
        if self._params["extended_tsv"]:
            while line.startswith("#"):
                line = next(self._iterator)
        vals = self._split_line(line)
        return dict(field.parse_value(vals) for field in self._fields)

    def readline(self):
        """Read a next line and parse it."""
        return next(self, None)


class ETSVWriter: # pylint: disable=too-few-public-methods
    """ETSV writer class."""

    def __init__(self, fileobj, fields, **kwargs) -> None:
        self.metadata = kwargs.pop("metadata", [])
        self._params = dict()
        self._params["print_title"] = kwargs.pop("print_title", True)
        self._params["extended_tsv"] = kwargs.pop("extended_tsv", True)
        if kwargs:
            args = ", ".join(kwargs)
            end = "" if len(kwargs) == 1 else "s"
            raise TypeError(f"unknown keyword argument{end}: {args}")
        if self._params["extended_tsv"]:
            for line in self.metadata:
                print("##" + line, file=fileobj)
        if self._params["print_title"]:
            if self._params["extended_tsv"]:
                print("#:", end="", file=fileobj)
            print(*fields, sep="\t", file=fileobj)
        self._fileobj = fileobj
        self._fields = fields

    def writeline(self, vals):
        """Write TSV values to the file as a line."""
        print(*(field.format_value(vals) for field in self._fields),
              sep="\t", file=self._fileobj)
