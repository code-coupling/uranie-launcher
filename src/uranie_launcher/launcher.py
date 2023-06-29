""" Script for launching a study with URANIE.
    It reads study parameters from uncertainty_data subclasses,
    and runs the script (or the command) commands_to_execute,
    which executes the individual calculation as many times as required.
"""

from pathlib import Path
from typing import Dict, List
from uranie_launcher import _data_2_uranie as d2u
from uranie_launcher import uncertainty_data, execution as exe

from uranie_launcher._data_2_uranie import (STUDY_EXP_DESIGN,   # pylint: disable=unused-import
                                            STUDY_WORKDIR_NAME,
                                            STUDY_OUTFILE_NAME,
                                            STUDY_OUTFILE_NAME_FAILED)


def execute_uranie(commands_to_execute: Dict[str, List],
                   inputs: uncertainty_data.Inputs,
                   propagation: uncertainty_data.Propagation,
                   outputs: uncertainty_data.Outputs,
                   execution: exe.Execution,
                   output_dirname: Path,
                   unitary_result_filename: str) -> int:
    """ Use URANIE to genetrate the experiment plan based on inputs, then launch calculations.

    Parameters
    ----------
    commands_to_execute: Dict[str, List]
        Name of the script or the command which URANIE will execute with all its arguments.
    inputs: uncertainty_data.Inputs
        Object containing all the infos about the uncertain parameters.
    propagation: uncertainty_data.Propagation
        Object containing the name of the propagation method used.
    outputs: uncertainty_data.Outputs
        Object containing the name of the outputs and all the informations about them.
    execution: execution.Execution
        Object containing all the infos about how to execute the calculations.
    output_dirname: Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation
    unitary_result_filename: str
        Name of the file containing the result of the
        aggregations functions for an unitary calculation

    Returns
    -------
    _rootlogon.DataServer.TDataServer
        return t_data_server if this function run through its end without crashing.
    """

    t_data_server = d2u.create_data_server(outputs)

    d2u.set_inputs(inputs, t_data_server)

    d2u.generate_sample(propagation, t_data_server, output_dirname)

    if execution.visualization:
        d2u.visualisation(t_data_server)

    t_output_file, headers = d2u.set_outputs(outputs, unitary_result_filename)

    # Code instantiation
    t_launcher, uranie_work_dir = d2u.create_launcher(commands_to_execute,
                                     t_data_server,
                                     output_dirname,
                                     t_output_file)

    d2u.run_calculations(execution, t_launcher)

    d2u.save_calculations(propagation,
                          t_data_server,
                          headers,
                          output_dirname,
                          unitary_result_filename,
                          uranie_work_dir)

    if execution.visualization:
        input('Type Enter to quit the program...')

    return t_data_server
