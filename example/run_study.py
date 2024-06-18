"""Tests ``launcher`` module."""

import json
from pathlib import Path
import shutil
import sys


from uranie_launcher import execution, input_data, launcher, data


def main():
    """Test execute_uranie"""

    template_input_filename = "input_file.json"
    result_filename = "result"

    commands_to_execute = [
        (sys.executable, [
            str(Path(__file__).parent.absolute() / "compute_pi_monte_carlo"),
            template_input_filename,
            ".",
            ]),
        (sys.executable, [
            str(Path(__file__).parent.absolute() / "post_compute"),
            ".",
            result_filename,
            ]),
        ]

    """creates an inputs object"""
    simulation_variable = 'nb_simu'
    data_input_inputs_distribution_uniform = input_data.Inputs()
    data_input_inputs_distribution_uniform.add_input(input_data.Inputs.Input(
        variable_name=simulation_variable,
        distribution=input_data.Inputs.DistributionUniform(lower_bound=100, upper_bound=100000)))
    data_input_inputs_distribution_uniform.set_file_flag(Path(__file__).absolute().parent / template_input_filename)


    """creates an outputs object"""
    quantity_of_interest = 'Pi'
    headers = ['pi', 'pi2']
    output = input_data.Outputs.Output(headers=headers,
                                       quantity_of_interest=quantity_of_interest,
                                       filename=result_filename)
    data_server_name = "my_data_server"
    data_input_outputs = input_data.Outputs(data_server_name)
    data_input_outputs.add_output(output)

    output_dirname = Path(__file__).absolute().parent / "results"
    if output_dirname.exists():
        shutil.rmtree(output_dirname)
    output_dirname.mkdir(parents=False, exist_ok=True)

    sample_size = 6
    propagation = input_data.Propagation(sampling_method=input_data.Propagation.SOBOL,
                                         sample_size=sample_size)

    exe = execution.ExecutionLocal(
        working_directory=output_dirname / "unitary", nb_jobs=sample_size)

    ascii_filepath, nb_failed = launcher.execute_uranie(
        commands_to_execute=commands_to_execute,
        inputs=data_input_inputs_distribution_uniform,
        propagation=propagation,
        outputs=data_input_outputs,
        execution=exe,
        output_directory=output_dirname)

    print(ascii_filepath)
    outp_data = data.ascii_to_data(ascii_filepath)
    data.data_to_csv(outp_data, ascii_filepath.with_suffix(".csv"))
    data.data_to_json(outp_data, ascii_filepath.with_suffix(".json"))

    assert (
        nb_failed == 0 and
        ascii_filepath.exists()
    )


if __name__ == "__main__":

    main()
