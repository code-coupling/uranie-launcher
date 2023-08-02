""" Script for launching a study with URANIE.
    It reads study parameters from input_data subclasses,
    and runs the script (or the command) commands_to_execute,
    which executes the individual calculation as many times as required.
"""

from pathlib import Path
from typing import Dict, List, Tuple
from uranie_launcher import _data_2_uranie as d2u
from uranie_launcher import input_data, execution as exe


def execute_uranie(commands_to_execute: Dict[str, List],
                   inputs: input_data.Inputs,
                   propagation: input_data.Propagation,
                   outputs: input_data.Outputs,
                   execution: exe.Execution,
                   output_directory: Path) -> Tuple[Path, int]:
    """ Use URANIE to genetrate the experiment plan based on inputs, then launch calculations.

    Parameters
    ----------
    commands_to_execute: Dict[str, List]
        Name of the script or the command which URANIE will execute with all its arguments.
    inputs: input_data.Inputs
        Object containing all the infos about the uncertain parameters.
    propagation: input_data.Propagation
        Object containing the name of the propagation method used.
    outputs: input_data.Outputs
        Object containing the name of the outputs and all the informations about them.
    execution: execution.Execution
        Object containing all the infos about how to execute the calculations.
    output_directory: Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation

    Returns
    -------
    Path
        Path to output file defined as ``output_directory/outputs.output_filename``.
    """

    t_data_server = d2u.create_data_server(outputs)

    d2u.set_inputs(inputs, t_data_server)

    d2u.generate_sample(propagation, outputs, t_data_server, output_directory)

    if execution.visualization:  # pragma: no cover
        d2u.visualisation(t_data_server)

    t_output_files = d2u.set_outputs(outputs)

    # Code instantiation
    t_launcher = d2u.create_launcher(commands_to_execute,
                                     t_data_server,
                                     output_directory,
                                     t_output_files)

    d2u.run_calculations(execution, t_launcher, output_directory)

    ascii_filepath, nb_failed = d2u.save_calculations(propagation,
                                                      execution,
                                                      outputs,
                                                      t_data_server,
                                                      output_directory)

    if execution.visualization:  # pragma: no cover
        d2u.visualisation(t_data_server)
        input('Type Enter to quit the program...')

    return ascii_filepath, nb_failed
