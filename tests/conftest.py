
import pytest
from pathlib import Path
from uranie_launcher import uncertainty_data
from uranie_launcher import _data_2_uranie
from uranie_launcher import _rootlogon


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


@pytest.fixture(name='headers', scope='session')
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


@pytest.fixture(name='quantity_of_interest', scope='session')
def quantity_of_interest_fixture():

    return "Temperature"


@pytest.fixture(name='tds_name', scope='session')
def tds_name_fixture():

    return "Name_of_t_data_server"


@pytest.fixture(name = 'outputs', scope='session')
def outputs_fixture(headers, quantity_of_interest, tds_name):

    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    return outputs


@pytest.fixture(name = 't_data_server', scope='session')
def t_data_server_fixture(outputs):

    data_server = _data_2_uranie.create_data_server(outputs)

    return data_server


@pytest.fixture(scope='session')
def t_output_file():

    unitary_result_filename = "unitary_aggregated_outputs.dat"
    output_file = _rootlogon.Launcher.TOutputFileRow(unitary_result_filename)

    headers = [
        'initial_value',
        'halftime_value',
        'final_value',
        'average_value',
        'cumulative_value',
        'minimum_value',
        'maximum_value'
        ]
    for header in headers:
        output_file.addAttribute(_rootlogon.DataServer.TAttribute(header))

    return output_file


@pytest.fixture(name='commands_to_execute', scope='session')
def commands_to_execute_fixture():

    commands_to_execute = {
        "test-run-unitary-calculation" : [
            "./input_for_tests",
            "./results",
            ],
        }

    return commands_to_execute

@pytest.fixture(name='program_tester', scope='session')
def program_tester_fixture():
    pass
