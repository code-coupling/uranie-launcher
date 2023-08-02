"""Tests ``input_data`` module."""

from typing import List

import pytest

from uranie_launcher import input_data


## input_data
def test_distribution_uniform():
    """Test distribution"""

    lower_bound = 0
    upper_bound = 1
    distribution = input_data.Inputs.DistributionUniform(lower_bound, upper_bound)

    assert (
        isinstance(distribution, input_data.Inputs.DistributionUniform) and
        distribution.lower_bound == lower_bound and
        distribution.upper_bound == upper_bound
        )


def test_distribution_uniform_raise():
    """Test distribution"""

    lower_bound = 2
    upper_bound = 1

    with pytest.raises(ValueError) as error:
        input_data.Inputs.DistributionUniform(lower_bound, upper_bound)
    assert "The upper bound have to be greater than the lower one !" in str(error.value)


def test_distribution_truncated_normal():
    """Test distribution"""

    lower_bound = 0
    upper_bound = 1
    mean = 1
    standard_deviation = 0.05
    distribution = input_data.Inputs.DistributionTruncatedNormal(lower_bound,
                                                                 upper_bound,
                                                                 mean,
                                                                 standard_deviation)

    assert (
        isinstance(distribution, input_data.Inputs.DistributionTruncatedNormal) and
        distribution.lower_bound == lower_bound and
        distribution.upper_bound == upper_bound and
        distribution.mean == mean and
        distribution.standard_deviation == standard_deviation
        )


def test_distribution_truncated_normal_raise():
    """Test inputs"""

    lower_bound = 2
    upper_bound = 1
    mean = 1
    standard_deviation = 0.05

    with pytest.raises(ValueError) as error:
        input_data.Inputs.DistributionTruncatedNormal(lower_bound,
                                                      upper_bound,
                                                      mean,
                                                      standard_deviation)
    assert "The upper bound have to be greater than the lower one !" in str(error.value)


def test_one_input(simulation_variable):
    """Test inputs"""

    lower_bound = 0
    upper_bound = 1
    distribution = input_data.Inputs.DistributionUniform(lower_bound=lower_bound,
                                                         upper_bound=upper_bound)

    input_1 = input_data.Inputs.Input(simulation_variable, distribution)

    inputs = input_data.Inputs()
    inputs.add_input(input_1)

    assert (
        isinstance(inputs, input_data.Inputs) and
        isinstance(inputs.inputs, List) and
        len(inputs.inputs) == 1 and
        isinstance(inputs.inputs[0], input_data.Inputs.Input) and
        inputs.inputs[0] == input_1 and
        isinstance(inputs.inputs[0].distribution, input_data.Inputs.DistributionUniform) and
        inputs.inputs[0].variable_name == simulation_variable and
        inputs.inputs[0].distribution.lower_bound == lower_bound and
        inputs.inputs[0].distribution.upper_bound == upper_bound and
        inputs.inputs[0].flag == "@" + simulation_variable +"@"
        )


def test_two_input():
    """Test inputs"""

    variable_name_1 = "variable_1"
    lower_bound_1 = 0
    upper_bound_1 = 1
    distribution_1 = input_data.Inputs.DistributionUniform(lower_bound_1, upper_bound_1)

    variable_name_2 = "variable_2"
    lower_bound_2 = 0
    upper_bound_2 = 1
    mean = 1
    standard_deviation = 0.05
    distribution_2 = input_data.Inputs.DistributionTruncatedNormal(lower_bound_2,
                                                                   upper_bound_2,
                                                                   mean,
                                                                   standard_deviation)

    input_1 = input_data.Inputs.Input(variable_name_1, distribution_1)
    input_2 = input_data.Inputs.Input(variable_name_2, distribution_2)

    inputs = input_data.Inputs()
    inputs.add_input(input_1)
    inputs.add_input(input_2)

    assert (
        isinstance(inputs.inputs, List) and
        len(inputs.inputs) == 2 and
        isinstance(inputs.inputs[0], input_data.Inputs.Input) and
        inputs.inputs[0] == input_1 and
        isinstance(inputs.inputs[0].distribution, input_data.Inputs.DistributionUniform) and
        inputs.inputs[0].variable_name == variable_name_1 and
        inputs.inputs[0].distribution.lower_bound == lower_bound_1 and
        inputs.inputs[0].distribution.upper_bound == upper_bound_1 and
        inputs.inputs[0].flag == "@" + variable_name_1 +"@" and
        isinstance(inputs.inputs[1], input_data.Inputs.Input) and
        inputs.inputs[1] == input_2 and
        isinstance(inputs.inputs[1].distribution, input_data.Inputs.DistributionTruncatedNormal) and
        inputs.inputs[1].variable_name == variable_name_2 and
        inputs.inputs[1].distribution.lower_bound == lower_bound_2 and
        inputs.inputs[1].distribution.upper_bound == upper_bound_2 and
        inputs.inputs[1].distribution.mean == mean and
        inputs.inputs[1].distribution.standard_deviation == standard_deviation and
        inputs.inputs[1].flag == "@" + variable_name_2 +"@"
        )


def test_file_flag():
    """Test file flag"""

    inputs = input_data.Inputs()
    scenario_flag_filename = "some/path/to/uranie_tag_input.xml"
    inputs.set_file_flag(scenario_flag_filename)

    assert inputs.file_flag == scenario_flag_filename


def test_propagation():
    """Test propagation"""

    sampling_method = "name_of_sampling_method"
    sample_size = 4
    propagation = input_data.Propagation(sampling_method, sample_size)

    assert (
        isinstance(propagation, input_data.Propagation) and
        propagation.sampling_method == sampling_method and
        propagation.sample_size == sample_size
        )


def test_sample_size_zero_raises_value_error():
    """Test sample"""

    with pytest.raises(ValueError) as error:
        input_data.Propagation(sampling_method="name_of_sampling_method", sample_size=0)
    assert (
        "sample_size must be greater than 0" in str(error.value)
    )


def test_one_output(headers, quantity_of_interest):
    """Test outputs"""

    filename = "filename"
    output = input_data.Outputs.Output(filename=filename,
                                       headers=headers,
                                       quantity_of_interest=quantity_of_interest)

    assert (
        isinstance(output, input_data.Outputs.Output) and
        output.filename == filename and
        output.headers == headers and
        output.quantity_of_interest == quantity_of_interest
        )


def test_outputs(headers, quantity_of_interest, data_server_name):
    """Test outputs"""

    outputs = input_data.Outputs(data_server_name)
    outputs.add_output(input_data.Outputs.Output(headers, quantity_of_interest, "output_file"))

    assert (
        isinstance(outputs, input_data.Outputs) and
        outputs.name == data_server_name and
        isinstance(outputs.outputs, List) and
        isinstance(outputs.outputs[0], input_data.Outputs.Output) and
        outputs.outputs[0].headers == headers and
        outputs.outputs[0].quantity_of_interest == quantity_of_interest
        )


def test_two_output():
    """Test outputs"""

    headers = ['toto', 'tata']

    headers_1 = headers
    quantity_of_interest_1 = "Temperature"
    output_1 = input_data.Outputs.Output(headers_1, quantity_of_interest_1, "Temperature_output")

    headers_2 = headers[:-1]
    quantity_of_interest_2 = "Density"
    output_2 = input_data.Outputs.Output(headers_2, quantity_of_interest_2, "Density_output")

    name = "Name_of_the_study"
    outputs = input_data.Outputs(name)
    outputs.add_output(output_1)
    outputs.add_output(output_2)

    assert isinstance(outputs, input_data.Outputs)
    assert outputs.name == name
    assert isinstance(outputs.outputs, List)
    assert isinstance(outputs.outputs[0], input_data.Outputs.Output)
    assert outputs.outputs[0].headers == headers_1
    assert outputs.outputs[0].quantity_of_interest == quantity_of_interest_1
    assert isinstance(outputs.outputs[1], input_data.Outputs.Output)
    assert outputs.outputs[1].headers == headers_2
    assert outputs.outputs[1].quantity_of_interest == quantity_of_interest_2

    assert outputs.experimental_design_filename == f"{name}_exp_design.dat"
    assert outputs.output_filename == f"{name}_output.dat"
    assert outputs.failed_filename == f"{name}_failed.dat"
