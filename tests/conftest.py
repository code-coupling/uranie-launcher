
import pytest
from pathlib import Path
from uranie_launcher import uncertainty_data, _data_2_uranie

# @pytest.fixture(scope='session')
# def program_path():

#     return Path(__file__).absolute().parent / "program_tester"


# @pytest.fixture(scope='session')
# def test_toto():

#     def my_test_fun(a, b):
#         return a == b
#     return my_test_fun


@pytest.fixture(scope='session')
def scenario_flag_filename():

    return "some/path/to/uranie_tag_input.xml"


@pytest.fixture(scope='session')
def sampling_method():

    return "name_of_sampling_method"


@pytest.fixture(name='tds_name', scope='session')
def headers_fixture():

    return [
        'initial_value',
        'halftime_value',
        'final_value',
        'average_value',
        'cumulative_value',
        'minimum_value',
        'maximum_value'
        ]


@pytest.fixture(name='tds_name', scope='session')
def quantity_of_interest_fixture():

    return "Neutronic_Power"


@pytest.fixture(name='tds_name', scope='session')
def tds_name_fixture():

    return "Name_of_t_data_server"


@pytest.fixture()
def t_data_server(headers, quantity_of_interest, tds_name):

    output = uncertainty_data.Outputs.Output(headers, quantity_of_interest)
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    data_server = _data_2_uranie.create_data_server(outputs)

    return data_server
