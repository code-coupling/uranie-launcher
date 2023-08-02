"""Pytest configuration script."""
# pylint: disable=redefined-outer-name

from pathlib import Path
import sys

import pytest

from uranie_launcher import data, execution, input_data, utils, _data_2_uranie


# Fixtures for testing data module
@pytest.fixture
def simple_data():
    """Test data fixture"""
    my_data = data.Data(name="test_data",
                        description="test",
                        headers=[data.Data.Header("x", data.Data.Types.DOUBLE, "u_x"),
                                 data.Data.Header("y", data.Data.Types.STRING, "u_y"),
                                 data.Data.Header("z", data.Data.Types.VECTOR, "u_z")])
    values=[1.0, "toto", [1.0, 2.0]]
    my_data.add_values(values=values)
    return my_data


# Fixtures for running the dummy code
@pytest.fixture(scope='session')
def simulation_variable():
    """Name of variable"""
    return 'nb_simu'


@pytest.fixture(scope='session')
def quantity_of_interest():
    """Name of quantity computed"""
    return 'pi'


@pytest.fixture(scope='session')
def result_filename():
    """result filename"""
    return "result"


@pytest.fixture(scope='session')
def tag_filename():
    """tag filename"""
    return "tag_input_for_tests.json"


@pytest.fixture(scope='session')
def data_server_name():
    """data server name"""
    return "my_data_server"


@pytest.fixture(scope='session')
def headers(quantity_of_interest):
    """list of headers to provide to the tests"""
    return [quantity_of_interest]


@pytest.fixture(scope='session')
def commands_to_execute(tag_filename):
    """command to run"""

    return {
        sys.executable : [
             str(Path(__file__).parent / "program_tester.py"),
            tag_filename,
            ".",
            ],
        }

# Fixtures to test input data model
@pytest.fixture(scope='session')
def data_input_inputs_distribution_uniform(simulation_variable, tag_filename):
    """creates an inputs object"""
    inputs = input_data.Inputs()
    inputs.add_input(input_data.Inputs.Input(
        variable_name=simulation_variable,
        distribution=input_data.Inputs.DistributionUniform(lower_bound=100, upper_bound=1000)))
    inputs.set_file_flag(Path(__file__).absolute().parent / tag_filename)
    return inputs


@pytest.fixture(scope='session')
def data_input_inputs_distribution_truncated_normal(simulation_variable, tag_filename):
    """creates an inputs object"""
    inputs = input_data.Inputs()
    inputs.add_input(input_data.Inputs.Input(
        variable_name=simulation_variable,
        distribution=input_data.Inputs.DistributionTruncatedNormal(
            lower_bound=100, upper_bound=1000, mean=600, standard_deviation=100)))
    inputs.set_file_flag(Path(__file__).absolute().parent / tag_filename)
    return inputs


@pytest.fixture(scope='session')
def data_input_outputs(headers, result_filename, data_server_name, quantity_of_interest):
    """creates an outputs object"""
    output = input_data.Outputs.Output(headers=headers,
                                       quantity_of_interest=quantity_of_interest,
                                       filename=result_filename)

    outputs = input_data.Outputs(data_server_name)
    outputs.add_output(output)

    return outputs


@pytest.fixture
def t_data_server(data_input_outputs):
    """creates an t_data_server object"""
    return _data_2_uranie.create_data_server(data_input_outputs)


@pytest.fixture
def generate_sample(data_input_outputs,
                    data_input_inputs_distribution_uniform):
    """creates function to generate a sample"""

    def _generate(output_dirname, t_data_server, sampling_method, sample_size):
        _data_2_uranie.set_inputs(data_input_inputs_distribution_uniform, t_data_server)

        propagation = input_data.Propagation(sampling_method=sampling_method,
                                            sample_size=sample_size)

        return _data_2_uranie.generate_sample(propagation=propagation,
                                            outputs=data_input_outputs,
                                            t_data_server=t_data_server,
                                            output_directory=output_dirname)
    return _generate


@pytest.fixture
def t_output_files(data_input_outputs):
    """creates a list of t_output_file"""
    return _data_2_uranie.set_outputs(data_input_outputs)


@pytest.fixture
def generate_t_launcher(commands_to_execute, t_data_server, t_output_files, generate_sample):
    """creates function to generate a t_launcher"""
    def _generate(output_dirname):
        generate_sample(output_dirname,
                        t_data_server,
                        input_data.Propagation.SOBOL,
                        4)

        utils.set_verbosity(utils.DEBUG)

        return _data_2_uranie.create_launcher(commands_to_execute,
                                              t_data_server,
                                              output_dirname,
                                              t_output_files)
    return _generate


@pytest.fixture
def generate_final_results(
        commands_to_execute, data_input_outputs, t_data_server, t_output_files, generate_sample):
    """creates function to get calculation results"""
    def _generate(output_dirname, sample_size):

        generate_sample(output_dirname,
                        t_data_server,
                        input_data.Propagation.SOBOL,
                        sample_size)

        t_launcher = _data_2_uranie.create_launcher(commands_to_execute,
                                                    t_data_server,
                                                    output_dirname,
                                                    t_output_files)

        exe = execution.ExecutionLocal(working_directory=output_dirname / "unitary",
                                       nb_jobs=sample_size)

        _data_2_uranie.run_calculations(execution=exe,
                                        t_launcher=t_launcher,
                                        output_directory=output_dirname)

        propagation = input_data.Propagation(sampling_method=input_data.Propagation.SOBOL,
                                            sample_size=sample_size)

        utils.set_verbosity(utils.DEBUG)

        return _data_2_uranie.save_calculations(propagation=propagation,
                                                             execution=exe,
                                                             outputs=data_input_outputs,
                                                             t_data_server=t_data_server,
                                                             output_directory=output_dirname)
    return _generate
