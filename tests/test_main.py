#! /usr/bin/env python3


import pytest
import etsv


#class ContextManagerStub:
#    def __init__(self, exc_type, exc_val, exc_tb):
#        self.exc_type = exc_type
#        self.exc_val = exc_val
#        self.exc_tb = exc_tb
#        self.entered = False
#        self.exited = False
#
#    def __enter__(self):
#        self.entered = True
#
#    def __exit__(self, exc_type, exc_val, exc_tb):
#        self.exited = (self.exc_type is exc_type
#                       and self.exc_val is exc_val
#                       and self.exc_tb is exc_tb)
#
#
class TestField:
    def test_all(self):
        name = "test"
        header = "Test field"
        field = etsv.Field(name, header)
        # __init__()
        assert field.name == name
        assert field.header == header
        # __str__()
        assert str(field) == header
        # __eq__()
        name2 = "test2"
        header2 = "Test field2"
        assert field == etsv.Field(name, header2)
        assert field != etsv.Field(name2, header)
        # __hash__()
        assert {field: header}


class TestInputField:
    def test_init(self):
        name = "test"
        header = "Test field"
        index = 0
        value_type = int
        field = etsv.InputField(name, header)
        assert field.name == name
        assert field.index is None
        assert field.header == header
        field = etsv.InputField(name, index)
        assert field.name == name
        assert field.index == index
        assert field.header is None

    def test_take_index(self):
        name = "test"
        header = "Test field"
        field = etsv.InputField(name, header)
        field.take_index("Test\tTest field\tExample".split("\t"))
        assert field.index == 1
        with pytest.raises(ValueError):
            field.take_index("Test\tNo field\tExample".split("\t"))

    def test_parse_value(self):
        name = "test"
        index = 0
        value_type = int
        field = etsv.InputField(name, index, value_type)
        values = ["12", "qwerty"]
        assert field.parse_value(values) == (name, value_type(values[index]))
        with pytest.raises(ValueError):
            field.parse_value(values[index+1:])


class TestOutputField:
    def test_all(self):
        name = "test"
        header = "Test field"
        value_format = repr
        value_format2 = "{:.2f}"
        value = 12.345
        values = {name: value}
        # __init__()
        field = etsv.OutputField(name, header)
        assert field.name == name
        assert field.header == header
        # format_value()
        assert field.format_value(values) == str(value)
        field = etsv.OutputField(name, header, value_format)
        assert field.format_value(values) == value_format(value)
        field = etsv.OutputField(name, header, value_format2)
        assert field.format_value(values) == value_format2.format(value)


class TestETSVReader:
    def test_main(self):
        intsv_path = "tests/test_input.tsv"
        fields = [
            etsv.InputField("id", "ID"),
            etsv.InputField("names", 4),
            etsv.InputField("length", "Length", int),
            etsv.InputField("ec", "EC number"),
        ]
        with open(intsv_path) as intsv:
            reader = etsv.ETSVReader(intsv, fields)
            entries = list(etsv.ETSVReader(intsv, fields))
        assert len(entries) == 6
        assert entries[-1]["length"] == 421
        assert entries[-1]["id"] == ""
        assert entries[-1]["ec"] == ""
        assert reader.metadata == [
            " Metadata line",
            "   one more metadata line"
            ]

    def test_force_title(self):
        intsv_path = "tests/test_input_general.tsv"
        fields = [
            etsv.InputField("first", 0),
            etsv.InputField("second", 1),
            etsv.InputField("third", 2),
        ]
        with open(intsv_path) as intsv:
            entries = list(etsv.ETSVReader(intsv, fields, extended_tsv=False))
        assert len(entries) == 5
        with open(intsv_path) as intsv:
            entries = list(etsv.ETSVReader(intsv, fields, extended_tsv=False,
                                           force_title=True))
        assert len(entries) == 4
        fields = [
            etsv.InputField("first", 0),
            etsv.InputField("second", 1),
            etsv.InputField("third", "Third"),
        ]
        with open(intsv_path) as intsv:
            entries = list(etsv.ETSVReader(intsv, fields, extended_tsv=False))
        assert len(entries) == 4

    def test_general_tsv(self):
        intsv_path = "tests/test_input_general.tsv"
        fields = [
            etsv.InputField("first", 0),
            etsv.InputField("second", 1),
            etsv.InputField("third", 2),
        ]
        with open(intsv_path) as intsv:
            entries = list(etsv.ETSVReader(intsv, fields, extended_tsv=False))
        assert len(entries) == 5

    def test_maxsplit(self):
        intsv_path = "tests/test_input_general.tsv"
        fields = [
            etsv.InputField("first", 0),
            etsv.InputField("second", "Second\tThird"),
        ]
        with open(intsv_path) as intsv:
            entries = list(etsv.ETSVReader(intsv, fields, extended_tsv=False,
                                           maxsplit=1))
        assert len(entries) == 4
        assert entries[-1]["second"] == "second\t"


#class TestETSVWriter:
