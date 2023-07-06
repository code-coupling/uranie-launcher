import json
import pytest
import subprocess
from pathlib import Path
from typing import List
from uranie_launcher import execution as exe
from uranie_launcher import launcher
from uranie_launcher import uncertainty_data
from uranie_launcher import utils
from uranie_launcher import _data_2_uranie
from uranie_launcher import _rootlogon
from uranie_launcher import _run_unitary
from . import program_tester


# def test_0(program_path, my_test_fun):
#
#     assert my_test_fun(a, b)


## uncertainty_data
def test_distribution_uniform():

    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound,
                                                               upper_bound)

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
    input_1 = uncertainty_data.Inputs.Input(variable_name,
                                            distribution)
    inputs_list.add_input(input_1)

    assert (
        isinstance(inputs_list, uncertainty_data.Inputs) and
        isinstance(inputs_list.inputs, List) and
        len(inputs_list.inputs) == 1 and
        isinstance(inputs_list.inputs[0], uncertainty_data.Inputs.Input) and
        inputs_list.inputs[0] == input_1 and
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

    input_1 = uncertainty_data.Inputs.Input(variable_name_1,
                                            distribution_1)

    input_2 = uncertainty_data.Inputs.Input(variable_name_2,
                                            distribution_2)

    inputs_list.add_input(input_1)
    inputs_list.add_input(input_2)

    assert (
        isinstance(inputs_list.inputs, List) and
        len(inputs_list.inputs) == 2 and
        isinstance(inputs_list.inputs[0], uncertainty_data.Inputs.Input) and
        inputs_list.inputs[0] == input_1 and
        inputs_list.inputs[0].variable_name == variable_name_1 and
        inputs_list.inputs[0].distribution.__class__.__name__ == type_distrib_1 and
        inputs_list.inputs[0].distribution.lower_bound == lower_bound_1 and
        inputs_list.inputs[0].distribution.upper_bound == upper_bound_1 and
        inputs_list.inputs[0].flag == "@" + variable_name_1 +"@" and
        isinstance(inputs_list.inputs[1], uncertainty_data.Inputs.Input) and
        inputs_list.inputs[1] == input_2 and
        inputs_list.inputs[1].variable_name == variable_name_2 and
        inputs_list.inputs[1].distribution.__class__.__name__ == type_distrib_2 and
        inputs_list.inputs[1].distribution.lower_bound == lower_bound_2 and
        inputs_list.inputs[1].distribution.upper_bound == upper_bound_2 and
        inputs_list.inputs[1].distribution.mean == mean and
        inputs_list.inputs[1].distribution.standard_deviation == standard_deviation and
        inputs_list.inputs[1].flag == "@" + variable_name_2 +"@"
        )


def test_file_flag():

    inputs_list = uncertainty_data.Inputs()

    scenario_flag_filename = "some/path/to/uranie_tag_input.xml"
    inputs_list.set_file_flag(scenario_flag_filename)

    assert (
        inputs_list.file_flag == scenario_flag_filename
        )


def test_propagation():

    sampling_method = "name_of_sampling_method"
    sample_size = 2
    propagation = uncertainty_data.Propagation(sampling_method,
                                               sample_size)

    assert (
        isinstance(propagation, uncertainty_data.Propagation) and
        propagation.sampling_method == sampling_method and
        propagation.sample_size == sample_size
        )


def test_sample_size_zero_raises_value_error():

    sampling_method = "name_of_sampling_method"
    sample_size = 0

    with pytest.raises(ValueError) as error:
        propagation = uncertainty_data.Propagation(sampling_method,
                                                   sample_size)
    assert (
        "sample_size must be greater than 0" in str(error.value)
    )


def test_one_output(headers):

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    assert (
        isinstance(output, uncertainty_data.Outputs.Output) and
        output.headers == headers and
        output.quantity_of_interest == quantity_of_interest
        )


def test_outputs(headers):

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    assert (
        isinstance(outputs, uncertainty_data.Outputs) and
        outputs.name == tds_name and
        isinstance(outputs.outputs, List) and
        isinstance(outputs.outputs[0], uncertainty_data.Outputs.Output) and
        outputs.outputs[0].headers == headers and
        outputs.outputs[0].quantity_of_interest == quantity_of_interest
        )


def test_two_output(headers):

    headers_1 = headers
    headers_2 = headers[:-1]
    quantity_of_interest_1 = "Temperature"
    quantity_of_interest_2 = "Density"
    output_1 = uncertainty_data.Outputs.Output(headers_1,
                                               quantity_of_interest_1)
    output_2 = uncertainty_data.Outputs.Output(headers_2,
                                               quantity_of_interest_2)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output_1)
    outputs.add_output(output_2)

    assert (
        isinstance(outputs, uncertainty_data.Outputs) and
        outputs.name == tds_name and
        isinstance(outputs.outputs, List) and
        isinstance(outputs.outputs[0], uncertainty_data.Outputs.Output) and
        outputs.outputs[0].headers == headers_1 and
        outputs.outputs[0].quantity_of_interest == quantity_of_interest_1 and
        isinstance(outputs.outputs[1], uncertainty_data.Outputs.Output) and
        outputs.outputs[1].headers == headers_2 and
        outputs.outputs[1].quantity_of_interest == quantity_of_interest_2
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
    assert (
        "Execution on cluster is not implemented yet" in str(error.value)
    )


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
    assert (
        f"log_level must be in [{utils.NONE};{utils.DEBUG}]" in str(error.value)
    )


def test_set_verbosity_greater_that_upper_bound():

    new_log_level = 3

    with pytest.raises(ValueError) as error:
        utils.set_verbosity(new_log_level)
    assert (
        f"log_level must be in [{utils.NONE};{utils.DEBUG}]" in str(error.value)
    )


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
def test_create_data_server(headers):

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    assert (
        isinstance(t_data_server, _rootlogon.DataServer.TDataServer) and
        str(t_data_server) == f"Name: {tds_name} Title: Quantities: ['{quantity_of_interest}']" and
        t_data_server.GetName() == tds_name
        #and t_data_server.GetTitle() == title
    )


def test_set_inputs_distribution_uniform(headers):

    variable_name = "variable_1"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound,
                                                               upper_bound)

    _input = uncertainty_data.Inputs.Input(variable_name,
                                           distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    _data_2_uranie.set_inputs(inputs, t_data_server)

    assert (
        isinstance(t_data_server.getAttribute(variable_name), _rootlogon.DataServer.TUniformDistribution) and
        str(t_data_server.getAttribute(variable_name)) == f"Name: {variable_name} Title: {variable_name}" and
        t_data_server.getAttribute(variable_name).getLowerBound() == lower_bound and
        t_data_server.getAttribute(variable_name).getUpperBound() == upper_bound
    )


def test_set_inputs_distribution_truncated_normal(headers):

    variable_name = "variable_1"
    lower_bound = 0
    upper_bound = 1
    mean = 1
    standard_deviation = 0.05
    distribution = uncertainty_data.Inputs.DistributionTruncatedNormal(lower_bound,
                                                                       upper_bound,
                                                                       mean,
                                                                       standard_deviation)

    _input = uncertainty_data.Inputs.Input(variable_name,
                                           distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    _data_2_uranie.set_inputs(inputs, t_data_server)

    assert (
        isinstance(t_data_server.getAttribute(variable_name), _rootlogon.DataServer.TNormalDistribution) and
        str(t_data_server.getAttribute(variable_name)) == f"Name: {variable_name} Title: {variable_name}" and
        t_data_server.getAttribute(variable_name).getLowerBound() == lower_bound and
        t_data_server.getAttribute(variable_name).getUpperBound() == upper_bound and
        t_data_server.getAttribute(variable_name).getParameterMu() == mean and
        t_data_server.getAttribute(variable_name).getParameterSigma() == standard_deviation
    )


def test_set_inputs_raise_ValueError(headers):

    variable_name = "variable_1"

    distribution = uncertainty_data.Inputs.Distribution()

    _input = uncertainty_data.Inputs.Input(variable_name,
                                           distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    with pytest.raises(ValueError) as error:
        _data_2_uranie.set_inputs(inputs, t_data_server)
    assert (
        f"Invalid distribution type: {inputs.inputs[0].distribution.__class__.__name__}" in str(error.value)
    )


def test_generate_sample_with_sobol(headers):

    variable_name = "variable_1"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound,
                                                               upper_bound)

    _input = uncertainty_data.Inputs.Input(variable_name,
                                           distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    _data_2_uranie.set_inputs(inputs, t_data_server)



    sampling_method = "Sobol"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method,
                                               sample_size)

    output_dirname = "some/path/to/output_dirname"
    sampler = _data_2_uranie.generate_sample(propagation,
                                             t_data_server,
                                             Path(output_dirname))

    # print("sampler.printLog() :", sampler.printLog())

    assert (
        isinstance(sampler, _rootlogon.Sampler.TQMC) and
        sampler.getTDS() == t_data_server and
        sampler.getMethodName() == "qMC_sobol" and
        sampler.GetName() == f"Sampling_qMC_{sampling_method.lower()}_{sample_size}" and
        sampler.GetTitle() == f"Uranie {sample_size} sample with qMC method {sampling_method.lower()}"
        #FIXME : Could be a better test...
    )


def test_generate_sample_with_srs(headers):

    variable_name = "variable_1"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound,
                                                               upper_bound)

    _input = uncertainty_data.Inputs.Input(variable_name,
                                           distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    _data_2_uranie.set_inputs(inputs, t_data_server)



    sampling_method = "SRS"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method,
                                               sample_size)

    output_dirname = "some/path/to/output_dirname"
    sampler = _data_2_uranie.generate_sample(propagation,
                                             t_data_server,
                                             Path(output_dirname))

    # print("sampler.printLog() :", sampler.printLog())

    assert (
        isinstance(sampler, _rootlogon.Sampler.TSampling) and
        sampler.getTDS() == t_data_server and
        sampler.getMethodName() == sampling_method and
        sampler.GetName() == f"Sampling_{sampling_method.lower()}_{sample_size}" and
        sampler.GetTitle() == f"Uranie {sample_size} sample with method {sampling_method.lower()}"
        #FIXME : Could be a better test...
    )


def test_generate_sample_raise_ValueError(headers):

    variable_name = "variable_1"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound,
                                                               upper_bound)

    _input = uncertainty_data.Inputs.Input(variable_name,
                                           distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    t_data_server = _data_2_uranie.create_data_server(outputs)

    _data_2_uranie.set_inputs(inputs, t_data_server)



    sampling_method = "wrong_methode"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method,
                                               sample_size)

    output_dirname = "some/path/to/output_dirname"

    with pytest.raises(ValueError) as error:
        sampler = _data_2_uranie.generate_sample(propagation,
                                                 t_data_server,
                                                 Path(output_dirname))
    assert (
        f"Unknown sampling method: {propagation.sampling_method}" in str(error.value)
    )


# def test_visualisation(t_data_server, mocker):

#     # Mock les méthodes et les objets nécessaires
#     mocker.patch.object(_rootlogon.ROOT.gROOT, 'SetBatch')
#     mocker.patch.object(_rootlogon.ROOT, 'TCanvas')
#     mocker.patch.object(t_data_server, 'drawPairs')

#     # Appeler la fonction à tester
#     _data_2_uranie.visualisation(t_data_server)

#     # Vérifier l'appel des méthodes et des objets
#     _rootlogon.ROOT.gROOT.SetBatch.assert_called_once_with(False)
#     _rootlogon.ROOT.TCanvas.assert_called_once_with()
#     t_data_server.drawPairs.assert_called_once_with()


def test_set_outputs(headers):

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    unitary_result_filename = "unitary_aggregated_outputs.dat"

    t_output_file, headers = _data_2_uranie.set_outputs(outputs,
                                                        unitary_result_filename)

    print(t_output_file)

    assert (
        headers == [
        'initial_value',
        'halftime_value',
        'final_value',
        'average_value',
        'cumulative_value',
        'minimum_value',
        'maximum_value'
        ] and
        str(t_output_file) == f"Name: {unitary_result_filename} Title: TCodeFile with name[{unitary_result_filename}]"
    )


def test_create_launcher(headers, commands_to_execute):

    ## preparation des donnees
    # inputs
    inputs = uncertainty_data.Inputs()
    variable_name = "variable_1"
    lower_bound = 0
    upper_bound = 1
    distribution = inputs.DistributionUniform(lower_bound,
                                              upper_bound)
    inputs.add_input(inputs.Input(variable_name,
                                  distribution))
    scenario_flag_filename = Path(__file__).absolute().parent / "tag_input_for_tests.json"
    inputs.set_file_flag(str(scenario_flag_filename))

    # propagation
    sampling_method = "Sobol"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method,
                                               sample_size)

    # outputs
    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    quantity_of_interest = "Temperature"
    outputs.add_output(outputs.Output(headers,
                                      quantity_of_interest))

    # execution
    execution = exe.ExecutionLocal(1)
    ## fin preparation des donnees

    output_dirname = Path(__file__).absolute().parent / "results"
    unitary_result_filename = "unitary_aggregated_outputs.dat"


    t_data_server = _data_2_uranie.create_data_server(outputs)

    _data_2_uranie.set_inputs(inputs, t_data_server)

    sampler = _data_2_uranie.generate_sample(propagation,
                                             t_data_server,
                                             output_dirname)

    t_output_file, _headers = _data_2_uranie.set_outputs(outputs,
                                                         unitary_result_filename)

    t_launcher, uranie_work_dir = _data_2_uranie.create_launcher(commands_to_execute,
                                                                 t_data_server,
                                                                 output_dirname,
                                                                 t_output_file)

    assert (
        # uranie_work_dir == Path(__file__).absolute().parent / "uranie_unitaries" and
        # t_launcher.getWorkingDirectory() == uranie_work_dir and
        # t_launcher.getSave() == True and
        # t_launcher.getClean() == True
        True
    )


## _run_unitary
def test_program_tester():

    data_filename = "./input_for_tests"
    output_dirname = "./results"

    program_tester.main_unitary_calculation([data_filename, output_dirname])

    output_dir = Path(__file__).absolute().parent / output_dirname

    assert (
        output_dir.is_dir()
        #FIXME : Could be a better test...
    )


# def test_run_unitary():
#     pass

## launcher
def test_launcher(headers,
                  commands_to_execute):

    variable_name = "variable_1"
    lower_bound = 0
    upper_bound = 1
    distribution = uncertainty_data.Inputs.DistributionUniform(lower_bound,
                                                               upper_bound)

    _input = uncertainty_data.Inputs.Input(variable_name,
                                           distribution)

    inputs = uncertainty_data.Inputs()
    inputs.add_input(_input)
    scenario_flag_filename = Path(__file__).absolute().parent / "tag_input_for_tests.json"
    inputs.set_file_flag(str(scenario_flag_filename))

    quantity_of_interest = "Temperature"
    output = uncertainty_data.Outputs.Output(headers,
                                             quantity_of_interest)

    tds_name = "Name_of_t_data_server"
    outputs = uncertainty_data.Outputs(tds_name)
    outputs.add_output(output)

    sampling_method = "Sobol"
    sample_size = 42
    propagation = uncertainty_data.Propagation(sampling_method,
                                               sample_size)

    output_dirname = Path(__file__).absolute().parent

    unitary_result_filename = "unitary_aggregated_outputs.dat"

    nb_jobs = 2
    execution = exe.ExecutionLocal(nb_jobs)


    t_data_server = launcher.execute_uranie(commands_to_execute,
                                            inputs,
                                            propagation,
                                            outputs,
                                            execution,
                                            output_dirname,
                                            unitary_result_filename)
    assert (
        False
    )

