"""Tests ``data`` module."""

from pathlib import Path

import pytest

from uranie_launcher import data


def test_conversion():
    """Test type conversion"""

    assert 1.0 == data.Data.Types.convert("1.0", data.Data.Types.DOUBLE)
    assert "azerty" == data.Data.Types.convert("azerty", data.Data.Types.STRING)
    assert [1.0, 2.0 ,3.0] == data.Data.Types.convert("[1, 2 ,3]", data.Data.Types.VECTOR)


def test_header():
    """Test data header content"""

    header = data.Data.Header(
        name="test_header", value_type=data.Data.Types.DOUBLE, value_unit="None")

    assert header.name == "test_header"
    assert header.value_type == data.Data.Types.DOUBLE
    assert header.value_unit == "None"


def test_data(simple_data: data.Data):
    """Test data content"""

    with pytest.raises(ValueError) as error:
        simple_data.add_values(values=["toto", 1.0, [1.0, 2.0]])
    assert "Type is not correct: found" in str(error.value)

    with pytest.raises(ValueError) as error:
        simple_data.add_values(values=[1.0, "toto", [1.0, "2.0"]])
    assert "Element of vector is not correct: found" in str(error.value)

    assert simple_data.name == "test_data"
    assert simple_data.description == "test"
    assert simple_data.headers
    assert simple_data.names == ["x", "y", "z"]
    assert simple_data.types == [
        data.Data.Types.DOUBLE, data.Data.Types.STRING, data.Data.Types.VECTOR]
    assert simple_data.units == ["u_x", "u_y", "u_z"]
    assert simple_data.values == [[1.0], ["toto"], [[1.0, 2.0]]]
    assert simple_data.nb_rows == 1
    assert simple_data.nb_columns == 3
    assert simple_data.get_values(index=0) == [1.0, "toto", [1.0, 2.0]]


def test_data_to_csv(simple_data: data.Data):
    """Test conversion data <-> csv"""

    output_dirname = Path(__file__).absolute().parent / "test_data_to_csv"
    output_dirname.mkdir(parents=True, exist_ok=True)

    csv_filepath = output_dirname / "simple_data.csv"
    data.data_to_csv(data=simple_data, filepath=csv_filepath)

    simple_data_2 = data.csv_to_data(csv_filepath)

    assert simple_data.name == simple_data_2.name
    assert simple_data.description == simple_data_2.description
    assert len(simple_data.headers) == len(simple_data_2.headers)
    assert simple_data.names == simple_data_2.names
    assert simple_data.types == simple_data_2.types
    assert simple_data.units == simple_data_2.units
    assert simple_data.values == simple_data_2.values
    assert simple_data.nb_rows == simple_data_2.nb_rows
    assert simple_data.nb_columns == simple_data_2.nb_columns
    assert simple_data.get_values(index=0) == simple_data_2.get_values(index=0)


def test_data_to_json(simple_data: data.Data):
    """Test conversion data <-> json"""

    output_dirname = Path(__file__).absolute().parent / "test_data_to_json"
    output_dirname.mkdir(parents=True, exist_ok=True)

    json_filepath = output_dirname / "simple_data.json"
    data.data_to_json(data=simple_data, filepath=json_filepath)

    simple_data_2 = data.json_to_data(json_filepath)

    assert simple_data.name == simple_data_2.name
    assert simple_data.description == simple_data_2.description
    assert len(simple_data.headers) == len(simple_data_2.headers)
    assert simple_data.names == simple_data_2.names
    assert simple_data.types == simple_data_2.types
    assert simple_data.units == simple_data_2.units
    assert simple_data.values == simple_data_2.values
    assert simple_data.nb_rows == simple_data_2.nb_rows
    assert simple_data.nb_columns == simple_data_2.nb_columns
    assert simple_data.get_values(index=0) == simple_data_2.get_values(index=0)


def test_data_to_ascii(simple_data: data.Data):
    """Test conversion data <-> ascii"""

    output_dirname = Path(__file__).absolute().parent / "test_data_to_ascii"
    output_dirname.mkdir(parents=True, exist_ok=True)

    ascii_filepath = output_dirname / "simple_data.dat"
    data.data_to_ascii(data=simple_data, filepath=ascii_filepath)

    simple_data_2 = data.ascii_to_data(ascii_filepath)

    assert simple_data.name == simple_data_2.name
    assert simple_data.description == simple_data_2.description
    assert len(simple_data.headers) == len(simple_data_2.headers)
    assert simple_data.names == simple_data_2.names
    assert simple_data.types == simple_data_2.types
    assert simple_data.units == simple_data_2.units
    assert simple_data.values == simple_data_2.values
    assert simple_data.nb_rows == simple_data_2.nb_rows
    assert simple_data.nb_columns == simple_data_2.nb_columns
    assert simple_data.get_values(index=0) == simple_data_2.get_values(index=0)


def test_no_meta_data():
    """Test file without meta data"""

    output_dirname = Path(__file__).absolute().parent / "test_no_meta_data"
    output_dirname.mkdir(parents=True, exist_ok=True)

    ascii_filepath = output_dirname / "no_meta_data.dat"
    ascii_filepath.write_text("1.0 2.0 3.0", encoding="utf-8")

    no_meta_data = data.ascii_to_data(ascii_filepath)

    ascii_filepath_2 = output_dirname / "no_meta_data_2.dat"
    data.data_to_ascii(data=no_meta_data, filepath=ascii_filepath_2)
