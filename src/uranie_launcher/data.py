"""Module to load, parse and write data based on uranie file format (ascii or json).
"""
import csv
from datetime import datetime
import json
from pathlib import Path
from typing import List


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

        def convert(value: str, value_type: str):
            """_summary_

            Parameters
            ----------
            value : str
                _description_
            value_type : str
                _description_

            Returns
            -------
            _type_
                _description_
            """
            return {
                Data.Types.STRING: lambda value: str(value),
                Data.Types.DOUBLE: lambda value: float(value),
                Data.Types.VECTOR: [float(val) for val in value.strip('][').split(',')],
            }[value_type](value)


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

        types = {
            Data.Types.STRING: str,
            Data.Types.DOUBLE: (float, int),
            Data.Types.VECTOR: list,
        }

        for index, value in enumerate(values):
            if not isinstance(value, types[self.types[index]]):
                raise ValueError(f"Type is not correct for index {index}: found {type(value)},"
                                 f"expected {types[self.types[index]]} for '{self.names[index]}'.")
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
        csv_writer.writerow(["DATE", datetime.now().strftime("%a %b %d %H:%M:%S %Y")]) # "Fri Oct 28 10:41:44 2016"
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
    with filepath.open(mode='w', encoding='utf-8') as csv_file:

        matrix = []
        csv_reader = csv.reader(csv_file)
        for line_no, line in enumerate(csv_reader):
            if line_no == 0:
                name = line[1]
            elif line_no == 1:
                description = line[1]
            elif line_no == 2:
                pass # date
            elif line_no == 3:
                names = line[1:]
            elif line_no == 4:
                types = line[1:]
            elif line_no == 5:
                pass # titles
            elif line_no == 6:
                units = line[1:]
            else:
                matrix.append([Data.Types.convert(value, types[index])
                            for index, value in enumerate(line)])

        data = Data(name=name,
                    description=description,
                    headers=[Data.Header(name=name,
                                        value_type=types[index],
                                        value_unit=units[index])
                            for index, name in enumerate(names)])
        for values in matrix:
            data.add_values(values[1:])
        return data


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
        "_metadata" :
        {
            "_comment" : "",
            "date" : datetime.now().strftime("%a %b %d %H:%M:%S %Y"), # "Fri Oct 28 10:41:44 2016"
            "short_names" : data.names,
            "table_description" : data.description,
            "table_name" : data.name,
            "types" : data.types,
            "units" : data.units
        },
        "items" :
        [{name: values[index]
            for name, values in zip(data.names, data.values) }
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
#DATE: {datetime.now().strftime("%a %b %d %H:%M:%S %Y")}
#COLUMN_NAMES: {'|'.join(data.names)}
#COLUMN_TYPES: {'|'.join(data.types)}
#COLUMN_TITLES: {'|'.join(data.names)}
#COLUMN_UNITS: {'|'.join(data.units)}

""" + "\n".join([" ".join([str(values[index]) for values in data.values])
                     for index in range(data.nb_rows)]), encoding='utf-8')

def ascii_to_data(filepath: Path) -> Data:
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
        elif line.startswith("#NAME:"):
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
            if types:
                matrix.append([Data.Types.convert(value, types[index])
                               for index, value in enumerate(line.split())])
            else:
                matrix.append([float(value) for value in line.split()])

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
