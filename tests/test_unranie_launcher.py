import pytest
from pathlib import Path
from typing import List
from uranie_launcher import execution as exe
from uranie_launcher import uncertainty_data
from uranie_launcher import utils
from uranie_launcher import _data_2_uranie
from uranie_launcher import _rootlogon


# def test_0(program_path, my_test_fun):
#
#     assert my_test_fun(a, b)


## uncertainty_data
def test_distribution_uniform():

    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound, upper_bound)

    assert (
        isinstance(distribution, uncertainty_data.Inputs.DistributionUniform) and
        distribution.lower_bound == lower_bound and
        distribution.upper_bound == upper_bound
        )


def test_distribution_truncated_normal():

    lower_bound = 0
    upper_bound = 1
    mean = 1
    standard_deviation = 0.05
    distribution = uncertainty_data.Inputs.DistributionTruncatedNormal(lower_bound,
                                                                       upper_bound,
                                                                       mean,
                                                                       standard_deviation)

    assert (
        isinstance(distribution, uncertainty_data.Inputs.DistributionTruncatedNormal) and
        distribution.lower_bound == lower_bound and
        distribution.upper_bound == upper_bound and
        distribution.mean == mean and
        distribution.standard_deviation == standard_deviation
        )


def test_one_input():

    inputs_list = uncertainty_data.Inputs()
    variable_name = "variable_1"
    type_distrib_1 = "DistributionUniform"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound,
                                                               upper_bound)
    inputs_list.add_input(uncertainty_data.Inputs.Input(variable_name,
                                                        distribution))

    assert (
        len(inputs_list.inputs) == 1 and
        inputs_list.inputs[0].variable_name == variable_name and
        inputs_list.inputs[0].distribution.__class__.__name__ == type_distrib_1 and
        inputs_list.inputs[0].distribution.lower_bound == lower_bound and
        inputs_list.inputs[0].distribution.upper_bound == upper_bound and
        inputs_list.inputs[0].flag == "@" + variable_name +"@"
        )


def test_two_input():

    inputs_list = uncertainty_data.Inputs()
    variable_name_1 = "variable_1"
    type_distrib_1 = "DistributionUniform"
    lower_bound_1 = 0
    upper_bound_1 = 1
    distribution_1 = uncertainty_data.Inputs.DistributionUniform(lower_bound_1,
                                                                 upper_bound_1)
    inputs_list.add_input(uncertainty_data.Inputs.Input(variable_name_1,
                                                        distribution_1))

    variable_name_2 = "variable_2"
    type_distrib_2 = "DistributionTruncatedNormal"
    lower_bound_2 = 0
    upper_bound_2 = 1
    mean = 1
    standard_deviation = 0.05
    distribution_2 = uncertainty_data.Inputs.DistributionTruncatedNormal(lower_bound_2,
                                                                         upper_bound_2,
                                                                         mean,
                                                                         standard_deviation)
    inputs_list.add_input(uncertainty_data.Inputs.Input(variable_name_2,
                                                        distribution_2))

    assert (
        len(inputs_list.inputs) == 2 and
        inputs_list.inputs[0].variable_name == variable_name_1 and
        inputs_list.inputs[0].distribution.__class__.__name__ == type_distrib_1 and
        inputs_list.inputs[0].distribution.lower_bound == lower_bound_1 and
        inputs_list.inputs[0].distribution.upper_bound == upper_bound_1 and
        inputs_list.inputs[0].flag == "@" + variable_name_1 +"@" and
        inputs_list.inputs[1].variable_name == variable_name_2 and
        inputs_list.inputs[1].distribution.__class__.__name__ == type_distrib_2 and
        inputs_list.inputs[1].distribution.lower_bound == lower_bound_2 and
        inputs_list.inputs[1].distribution.upper_bound == upper_bound_2 and
        inputs_list.inputs[1].distribution.mean == mean and
        inputs_list.inputs[1].distribution.standard_deviation == standard_deviation and
        inputs_list.inputs[1].flag == "@" + variable_name_2 +"@"
        )


def test_file_flag(scenario_flag_filename):

    inputs_list = uncertainty_data.Inputs()
    inputs_list.set_file_flag(scenario_flag_filename)

    assert (
        inputs_list.file_flag == scenario_flag_filename
        )


def test_propagation(sampling_method):

    sample_size = 2
    propagation = uncertainty_data.Propagation(sampling_method, sample_size)

    assert (
        isinstance(propagation, uncertainty_data.Propagation) and
        propagation.sampling_method == sampling_method and
        propagation.sample_size == sample_size
        )


def test_sample_size_zero_raises_value_error(sampling_method):

    sample_size = 0

    with pytest.raises(ValueError) as error:
        propagation = uncertainty_data.Propagation(sampling_method, sample_size)
    assert "sample_size must be greater than 0" in str(error.value)


def test_one_output(headers, quantity_of_interest):

    output = uncertainty_data.Outputs.Output(headers, quantity_of_interest)

    assert (
        isinstance(output, uncertainty_data.Outputs.Output) and
        output.headers == headers and
        output.quantity_of_interest == quantity_of_interest
        )


def test_outputs(headers, quantity_of_interest, tds_name):

    output = uncertainty_data.Outputs.Output(headers, quantity_of_interest)
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    assert (
        isinstance(outputs, uncertainty_data.Outputs) and
        isinstance(outputs.outputs, List) and
        isinstance(outputs.outputs[0], uncertainty_data.Outputs.Output) and
        outputs.outputs[0].headers == headers and
        outputs.outputs[0].quantity_of_interest == quantity_of_interest
        )


def test_two_output(headers, tds_name):

    headers_1 = headers
    headers_2 = headers[:-1]
    quantity_of_interest_1 = "Neutronic_Power"
    quantity_of_interest_2 = "Water_Density"
    output_1 = uncertainty_data.Outputs.Output(headers_1, quantity_of_interest_1)
    output_2 = uncertainty_data.Outputs.Output(headers_2, quantity_of_interest_2)

    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output_1)
    outputs.add_output(output_2)

    assert (
        isinstance(outputs, uncertainty_data.Outputs) and
        isinstance(outputs.outputs, List) and
        isinstance(outputs.outputs[0], uncertainty_data.Outputs.Output) and
        outputs.outputs[0].headers == headers_1 and
        outputs.outputs[1].headers == headers_2
    )


## execution
def test_execution_default():

    execution = exe.Execution()

    assert (
        execution.visualization is False
    )


def test_execution_enable_visualization():

    execution = exe.Execution()
    execution.enable_visualization()

    assert (
        execution.visualization is True
    )


def test_execution_local():

    nb_jobs = 2
    execution = exe.ExecutionLocal(nb_jobs)

    assert (
        execution.visualization is False and
        execution.nb_jobs == nb_jobs
    )


def test_execution_slurm_not_implemented():

    with pytest.raises(NotImplementedError) as error:
        execution = exe.ExecutionSlurm()
    assert "Execution on cluster is not implemented yet" in str(error.value)


## utils
def test_utils():

    assert (
        utils._log_level == 1
    )


def test_set_verbosity():

    new_log_level = 2
    utils.set_verbosity(new_log_level)

    assert (
        utils._log_level == new_log_level
    )


def test_set_verbosity_not_legit(): # FIXME : Est-ce normale de pouvoir faire ça ?

    new_log_level = 1
    utils._log_level = new_log_level

    assert (
        utils._log_level == new_log_level
    )


def test_set_verbosity_lower_that_min_bound():

    new_log_level = -1

    with pytest.raises(ValueError) as error:
        utils.set_verbosity(new_log_level)
    assert f"log_level must be in [{utils.NONE};{utils.DEBUG}]" in str(error.value)


def test_set_verbosity_greater_that_upper_bound():

    new_log_level = 3

    with pytest.raises(ValueError) as error:
        utils.set_verbosity(new_log_level)
    assert f"log_level must be in [{utils.NONE};{utils.DEBUG}]" in str(error.value)


def test_log(capsys):

    new_log_level = 1
    utils.set_verbosity(new_log_level)
    message_log = "un message de log"
    utils.log(utils.INFO, message_log)

    # Capture output
    captured_log = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_log.out == f"{message_log}\n"
    )


def test_no_info_output_when_log_level_below_info(capsys):
    new_log_level = utils.NONE
    utils.set_verbosity(new_log_level)

    message_info = "un message d'info"
    utils.info(message_info)

    # Capture output
    captured_info = capsys.readouterr()

    message_debug = "un message de debug"
    utils.debug(message_debug)

    # Capture output
    captured_debug = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_info.out == "" and
        captured_debug.out == ""
        )


def test_no_debug_output_when_log_level_below_debug(capsys):
    new_log_level = utils.INFO
    utils.set_verbosity(new_log_level)

    message_info = "un message d'info"
    utils.info(message_info)

    # Capture output
    captured_info = capsys.readouterr()

    message_debug = "un message de debug"
    utils.debug(message_debug)

    # Capture output
    captured_debug = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_info.out == f"{message_info}\n" and
        captured_debug.out == ""
        )


def test_all_output_when_log_level_set_to_debug(capsys):
    new_log_level = utils.DEBUG
    utils.set_verbosity(new_log_level)

    message_info = "un message d'info"
    utils.info(message_info)

    # Capture output
    captured_info = capsys.readouterr()

    message_debug = "un message de debug"
    utils.debug(message_debug)

    # Capture output
    captured_debug = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_info.out == f"{message_info}\n" and
        captured_debug.out == f"{message_debug}\n"
        )


## _data_2_uranie
def test_create_data_server(headers, quantity_of_interest, tds_name):

    output = uncertainty_data.Outputs.Output(headers, quantity_of_interest)
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    assert (
        isinstance(t_data_server, _rootlogon.DataServer.TDataServer)
    )


def test_set_inputs_distribution_uniform(t_data_server, tds_name, quantity_of_interest, capsys):

    variable_name = "Name_of_the_uncertain_variable"

    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound, upper_bound)

    _input = uncertainty_data.Inputs.Input(variable_name, distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    _data_2_uranie.set_inputs(inputs, t_data_server)

    print(t_data_server)
    captured_t_data_server = capsys.readouterr()

    assert (
        captured_t_data_server.out == f"Name: {tds_name} Title: Quantities: ['{quantity_of_interest}']\n" and
        False
    )


def test_set_inputs_distribution_truncated_normal(t_data_server, tds_name, quantity_of_interest, capsys):

    variable_name = "Name_of_the_uncertain_variable"

    lower_bound = 0
    upper_bound = 1
    mean = 1
    standard_deviation = 0.05
    distribution = uncertainty_data.Inputs.DistributionTruncatedNormal(lower_bound,
                                                                       upper_bound,
                                                                       mean,
                                                                       standard_deviation)

    _input = uncertainty_data.Inputs.Input(variable_name, distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    _data_2_uranie.set_inputs(inputs, t_data_server)

    print(t_data_server)

    captured_t_data_server = capsys.readouterr()

    assert (
        captured_t_data_server.out == f"Name: {tds_name} Title: Quantities: ['{quantity_of_interest}']\n" and
        False
    )


def test_set_inputs_raise_ValueError(t_data_server):

    variable_name = "Name_of_the_uncertain_variable"

    distribution = uncertainty_data.Inputs.Distribution()

    _input = uncertainty_data.Inputs.Input(variable_name, distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    with pytest.raises(ValueError) as error:
        _data_2_uranie.set_inputs(inputs, t_data_server)
    assert f"Invalid distribution type: {inputs.inputs[0].distribution.__class__.__name__}" in str(error.value)


def test_generate_sample_with_sobol(t_data_server):

    variable_name = "Name_of_the_uncertain_variable"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound, upper_bound)
    _input = uncertainty_data.Inputs.Input(variable_name, distribution)
    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)
    _data_2_uranie.set_inputs(inputs, t_data_server)

    sampling_method = "Sobol"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method, sample_size)
    output_dirname = "some/path/to/output_dirname"
    sampler = _data_2_uranie.generate_sample(propagation, t_data_server, Path(output_dirname))

    print(sampler)

    raise(
        False
    )


def test_generate_sample_with_srs(t_data_server):

    variable_name = "Name_of_the_uncertain_variable"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound, upper_bound)
    _input = uncertainty_data.Inputs.Input(variable_name, distribution)
    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)
    _data_2_uranie.set_inputs(inputs, t_data_server)

    sampling_method = "SRS"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method, sample_size)
    output_dirname = "some/path/to/output_dirname"
    sampler = _data_2_uranie.generate_sample(propagation, t_data_server, Path(output_dirname))

    print(sampler)

    raise(
        False
    )


def test_generate_sample_raise_ValueError(t_data_server):

    variable_name = "Name_of_the_uncertain_variable"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound, upper_bound)
    _input = uncertainty_data.Inputs.Input(variable_name, distribution)
    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)
    _data_2_uranie.set_inputs(inputs, t_data_server)

    sampling_method = "wrong_methode"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method, sample_size)
    output_dirname = "some/path/to/output_dirname"
    sampler = _data_2_uranie.generate_sample(propagation, t_data_server, Path(output_dirname))

    print(sampler)

    raise(
        False
    )


def test_visualisation(t_data_server):


    raise(
        False
    )


## _run_unitary


## launcher
