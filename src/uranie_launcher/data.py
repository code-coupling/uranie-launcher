"""Module to load, parse and write data based on uranie file format (ascii or json).
"""
import csv
from datetime import datetime
import json
from pathlib import Path
from typing import Any, List


class Data():
    """Class containing the data."""

    class Types:
        """Class defining the type available in ``Data``."""

        STRING = "S"
        """Value of type ``str``."""
        DOUBLE = "D"
        """Value of type ``float``."""
        VECTOR = "V"
        """Value of type ``list``."""

        @staticmethod
        def convert(value: str, value_type: str) -> Any:
            """Convert from string to Uranie type

            Parameters
            ----------
            value : str
                Value as string.
            value_type : str
                Type of the value

            Returns
            -------
            Any
                Value casted as expected type
            """
            return {
                Data.Types.STRING: str,
                Data.Types.DOUBLE: float,
                Data.Types.VECTOR: lambda val: [float(v) for v in val.strip('][').split(',')],
            }[value_type](value)

        @staticmethod
        def check_type(value: Any, value_type: str, var_name: str, row_index: int):
            """Check the type of a value.

            Parameters
            ----------
            value : Any
                Value to test
            value_type : str
                Uranie ``Data.Types``
            var_name : str
                Name associated to the variable
            row_index : int
                Row in the Data

            Raises
            ------
            ValueError
                The type is not in ``Data.Types``.
            ValueError
                The type of an element of ``Data.Types.VECTOR`` is not float.
            """

            types = {
                Data.Types.STRING: str,
                Data.Types.DOUBLE: (float, int),
                Data.Types.VECTOR: list,
            }
            if not isinstance(value, types[value_type]):
                raise ValueError(
                    f"Type is not correct: found {type(value)},"
                    f"expected {types[value_type]} for '{var_name}' at row {row_index}.")

            if value_type == Data.Types.VECTOR:
                for elt, val in enumerate(value):
                    if not isinstance(val, float):
                        raise ValueError(
                            f"Element of vector is not correct: found {type(val)},"
                            f"expected float for '{var_name}' at row {row_index}, element {elt}.")

    class Header:
        """Class defining data header"""

        def __init__(self, name: str, value_type: str, value_unit: str) -> None:
            """Constructor.

            Parameters
            ----------
            name : str
                name of the variable
            value_type : str
                type among ``Data.Types``
            value_unit : str
                unit of the variable
            """
            self._name: str = name
            self._value_type: str = value_type
            self._value_unit: str = value_unit

        @property
        def name(self) -> str:
            """name of the variable"""
            return self._name

        @property
        def value_type(self) -> str:
            """type among ``Data.Types``"""
            return self._value_type

        @property
        def value_unit(self) -> str:
            """unit of the variable"""
            return self._value_unit

    def __init__(self, name: str, description: str, headers: List['Data.Header']):
        """Constructor.

        Parameters
        ----------
        name : str
            Name of the data
        description : str
            Description of the data
        headers : List[Data.Header]
            List of ``Data.Header`` to define the content
        """
        self._name: str = name
        self._description: str = description
        self._headers: List['Data.Header'] = headers
        self._values: List[List[float or str or List[float]]] = [
            [] for i in range(len(self._headers))]

    @property
    def name(self) -> str:
        """Name of the data"""
        return self._name

    @property
    def description(self) -> str:
        """Description of the data"""
        return self._description

    @property
    def headers(self) -> List['Data.Header']:
        """List of ``Data.Header`` defining the content"""
        return self._headers

    @property
    def names(self) -> List[str]:
        """List of header names"""
        return [header.name for header in self.headers]

    @property
    def types(self) -> List[str]:
        """List of header types"""
        return [header.value_type for header in self.headers]

    @property
    def units(self) -> List[str]:
        """List of header units"""
        return [header.value_unit for header in self.headers]

    @property
    def values(self) -> List[List[float or str or List[float]]]:
        """values per header"""
        return self._values

    @property
    def nb_rows(self):
        """Number of values per header"""
        return len(self.values[0])

    @property
    def nb_columns(self):
        """Number of header"""
        return len(self.headers)

    def add_values(self, values: List[float or str or List[float]]):
        """Add a row in the data.

        Parameters
        ----------
        values : List[float or str or List[float]]
            Value for each header

        Raises
        ------
        ValueError
            If type is not coherent with header
        """

        for index, value in enumerate(values):
            Data.Types.check_type(value=value,
                                  value_type=self.types[index],
                                  row_index=len(self._values[index]),
                                  var_name=self.names[index])
        for index, value in enumerate(values):
            self._values[index].append(value)

    def get_values(self, index) -> List[float or str or List[float]]:
        """Get a row in the data.

        Parameters
        ----------
        index : _type_
            Row index

        Returns
        -------
        List[float or str or List[float]]
            Value for each header
        """
        return [values[index] for values in self.values]


def data_to_csv(data: Data, filepath: Path):
    """Convert ``Data`` to csv.

    Parameters
    ----------
    data : Data
        data to dump
    filepath : Path
        Path to file
    """
    with filepath.open(mode='w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["NAME", data.name])
        csv_writer.writerow(["TITLE", data.description])
        csv_writer.writerow(["DATE", _get_date()])
        csv_writer.writerow(["COLUMN_NAMES"] + data.names)
        csv_writer.writerow(["COLUMN_TYPES"] + data.types)
        csv_writer.writerow(["COLUMN_TITLES"] + data.names)
        csv_writer.writerow(["COLUMN_UNITS"] + data.units)
        csv_writer.writerows([[index] + [str(values[index]) for values in data.values]
                              for index in range(data.nb_rows)])


def csv_to_data(filepath: Path) -> Data:
    """Convert csv to ``Data``.

    Parameters
    ----------
    filepath : Path
        Path to file

    Returns
    -------
    Data
        Loaded data
    """
    with filepath.open(mode='r', encoding='utf-8') as csv_file:

        matrix = []
        csv_reader = csv.reader(csv_file)
        for line_no, line in enumerate(csv_reader):
            if line_no == 0:
                name = line[1]
            elif line_no == 1:
                description = line[1]
            elif line_no == 2:
                pass  # date
            elif line_no == 3:
                names = line[1:]
            elif line_no == 4:
                types = line[1:]
            elif line_no == 5:
                pass  # titles
            elif line_no == 6:
                units = line[1:]
            else:
                matrix.append([Data.Types.convert(value, types[index])
                               for index, value in enumerate(line[1:])])

        data = Data(name=name,
                    description=description,
                    headers=[Data.Header(name=name,
                                         value_type=types[index],
                                         value_unit=units[index])
                             for index, name in enumerate(names)])
        for values in matrix:
            data.add_values(values)
        return data


def _get_date():
    return datetime.now().strftime("%a %b %d %H:%M:%S %Y")  # "Fri Oct 28 10:41:44 2016"


def data_to_json(data: Data, filepath: Path):
    """Convert ``Data`` to json.

    Parameters
    ----------
    data : Data
        data to dump
    filepath : Path
        Path to file
    """
    dico = {
        "_metadata":
        {
            "_comment": "",
            "date": _get_date(),
            "short_names": data.names,
            "table_description": data.description,
            "table_name": data.name,
            "types": data.types,
            "units": data.units
        },
        "items":
        [{name: values[index]
            for name, values in zip(data.names, data.values)}
            for index in range(data.nb_rows)]
    }
    filepath.write_text(json.dumps(dico), encoding='utf-8')


def json_to_data(filepath: Path) -> Data:
    """Convert json to ``Data``.

    Parameters
    ----------
    filepath : Path
        Path to file

    Returns
    -------
    Data
        Loaded data
    """
    dico = json.loads(filepath.read_text(encoding='utf-8'))
    data = Data(name=dico["_metadata"]["table_name"],
                description=dico["_metadata"]["table_description"],
                headers=[Data.Header(name=name,
                                     value_type=dico["_metadata"]["types"][index],
                                     value_unit=dico["_metadata"]["units"][index])
                         for index, name in enumerate(dico["_metadata"]["short_names"])])
    for item in dico["items"]:
        data.add_values([item[header.name] for header in data.headers])
    return data


def data_to_ascii(data: Data, filepath: Path):
    """Convert ``Data`` to 'Salome Table' as defined by Uranie.

    Parameters
    ----------
    data : Data
        data to dump
    filepath : Path
        Path to file
    """
    filepath.write_text(f"""
#NAME: {data.name}
#TITLE: {data.description}
#DATE: {_get_date()}
#COLUMN_NAMES: {'|'.join(data.names)}
#COLUMN_TYPES: {'|'.join(data.types)}
#COLUMN_TITLES: {'|'.join(data.names)}
#COLUMN_UNITS: {'|'.join(data.units)}

""" + "\n".join([" ".join([str(values[index]).replace(' ', '') for values in data.values])
                 for index in range(data.nb_rows)]) + "\n", encoding='utf-8')


def ascii_to_data(filepath: Path) -> Data:  # pylint: disable=too-many-branches  # noqa: C901
    """Convert 'Salome Table' as defined by Uranie to ``Data``.

    Parameters
    ----------
    filepath : Path
        Path to file

    Returns
    -------
    Data
        Loaded data
    """

    name = ""
    description = ""
    names = []
    types = []
    units = []
    matrix = []
    for line in filepath.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        if line.startswith("#NAME:"):
            name = line.replace('#NAME:', '').strip()
        elif line.startswith("#TITLE:"):
            description = line.replace('#TITLE:', '').strip()
        elif line.startswith("#DATE:"):
            pass
        elif line.startswith("#COLUMN_NAMES:"):
            names = [n.strip() for n in line.replace('#COLUMN_NAMES:', '').strip().split('|')]
        elif line.startswith("#COLUMN_TYPES:"):
            types = [n.strip() for n in line.replace('#COLUMN_TYPES:', '').strip().split('|')]
        elif line.startswith("#COLUMN_TITLES:"):
            pass
        elif line.startswith("#COLUMN_UNITS:"):
            units = [n.strip() for n in line.replace('#COLUMN_UNITS:', '').strip().split('|')]
        else:
            matrix.append([Data.Types.convert(value, types[index])
                           for index, value in enumerate(line.split())] if types else
                          [float(value) for value in line.split()])

    if not names:
        names = [str(index) for index, _ in enumerate(matrix[0])]
    if not types:
        types = ["D"] * len(names)
    if not units:
        units = [""] * len(names)

    data = Data(name=name,
                description=description,
                headers=[Data.Header(name=name,
                                     value_type=types[index],
                                     value_unit=units[index])
                         for index, name in enumerate(names)])
    for values in matrix:
        data.add_values(values)
    return data
