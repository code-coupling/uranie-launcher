"""Contains the implementation of the functions used in launcher.py
"""
import json
import os
from pathlib import Path
from typing import Dict, List
from . import _rootlogon, utils, uncertainty_data, execution as exe

URANIE_TCODE_LAUNCHER = "uranie-launcher-unitary"
URANIE_TCODE_JSON = ".uranie-unitary-commands.json"

STUDY_EXP_DESIGN = "experimental_design.dat"
STUDY_WORKDIR_NAME = "uranie_unitaries"
STUDY_OUTFILE_NAME = "aggregated_outputs.dat"
STUDY_OUTFILE_NAME_FAILED = "aggregated_outputs_failed.dat"


def create_data_server(outputs: uncertainty_data.Outputs):
    """Create the data server for Uranie

    Parameters
    ----------
    outputs : uncertainty_data.Outputs
        Object containing the name of the outputs and all the informations about them.

    Returns
    -------
    _rootlogon.DataServer.TDataServer
        TDataServer object.
    """

    title = f"Quantities: {[output.quantity_of_interest for output in outputs.outputs]}"
    return _rootlogon.DataServer.TDataServer(outputs.name, title)


def set_inputs(inputs: uncertainty_data.Inputs, t_data_server: _rootlogon.DataServer.TDataServer):
    """Defines the parameters of the distribution law for each uncertains values,
    and associate the variable_name to the flag used in file_flag.

    Parameters
    ----------
    inputs : uncertainty_data.Inputs
        Object containing all the infos about the uncertain parameters.
    t_data_server : _rootlogon.DataServer.TDataServer
        A TDataServer object

    Raises
    ------
    ValueError
        Invalid distribution type if the variable distribution isn't 'Uniform' or 'TruncatedNormal'.
    """
    for _input in inputs.inputs:
        variable_name = _input.variable_name
        if isinstance(_input.distribution, uncertainty_data.Inputs.DistributionUniform):
            t_data_server.addAttribute(_rootlogon.DataServer.TUniformDistribution(
                variable_name, _input.distribution.lower_bound, _input.distribution.upper_bound))

        elif isinstance(_input.distribution, uncertainty_data.Inputs.DistributionTruncatedNormal):
            mean = _input.distribution.mean
            std_dev = _input.distribution.standard_deviation
            t_data_server.addAttribute(_rootlogon.DataServer.TNormalDistribution(variable_name,
                                                                                 mean,
                                                                                 std_dev))
            t_data_server.getAttribute(variable_name).setBounds(_input.distribution.lower_bound,
                                                                _input.distribution.upper_bound)

        else:
            raise ValueError("Invalid distribution type: "
                             f"{_input.distribution.__class__.__name__}")

        t_data_server.getAttribute(variable_name).setFileFlag(inputs.file_flag, _input.flag)


def generate_sample(propagation: uncertainty_data.Propagation,
                    t_data_server: _rootlogon.DataServer.TDataServer,
                    output_dirname: Path):
    """Definition of the experimental plan

    Parameters
    ----------
    propagation : uncertainty_data.Propagation
        Object containing the name of the propagation method used and the sample size.
    t_data_server : _rootlogon.DataServer.TDataServer
        A TDataServer object
    output_dirname: Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation
    Returns
    -------
    _rootlogon.Sampler.TQMC or _rootlogon.Sampler.TSampling
        t_sampler object containing the experimental plan.

    Raises
    ------
    ValueError
        Invalid sampling method if the sampling method is not 'SRS' or 'Sobol'.
    """
    if propagation.sampling_method == propagation.SOBOL:
        # here I considered that canvas was deterministic
        t_sampler = _rootlogon.Sampler.TQMC(
            t_data_server, propagation.sampling_method, propagation.sample_size)
    elif propagation.sampling_method == propagation.SRS:
        t_sampler = _rootlogon.Sampler.TSampling(
            t_data_server, propagation.sampling_method, propagation.sample_size)
    else:
        raise ValueError(f"Unknown sampling method: {propagation.sampling_method}")

    t_sampler.generateSample()

    t_data_server.exportData(str(output_dirname / STUDY_EXP_DESIGN))

    return t_sampler


def visualisation(t_data_server: _rootlogon.DataServer.TDataServer):
    """Plot a graph if the visualization variable is equal to True

    Parameters
    ----------
    t_data_server : _rootlogon.DataServer.TDataServer
        A TDataServer object
    """
    _rootlogon.ROOT.gROOT.SetBatch(False)  # pylint: disable=no-member
    canvas = _rootlogon.ROOT.TCanvas()  # pylint: disable=no-member
    canvas.Clear()
    t_data_server.drawPairs()
    canvas.Draw()


def set_outputs(outputs: uncertainty_data.Outputs, unitary_result_filename: str):
    """Prepares the unitary aggregated outputs file.

    Parameters
    ----------
    outputs : uncertainty_data.Outputs
        Object containing the name of the outputs and all the informations about them.
    unitary_result_filename : str
        Name of the file containing the result of the
        aggregations functions for an unitary calculation

    Returns
    -------
    _rootlogon.Launcher.TOutputFileRow
        File that will contain the unitary aggregated outputs
    List
        Names of the different aggregations functions
    """
    # The output file of the code
    t_output_file = _rootlogon.Launcher.TOutputFileRow(unitary_result_filename)

    # The attribute in the output file
    # FIXME : here, headers is a list containing ALL the headers of all outputs.
    # May not be a good idea to do so...
    headers = []
    for output in outputs.outputs:
        for header in output.headers:
            headers.append(header)
            t_output_file.addAttribute(_rootlogon.DataServer.TAttribute(header))


    return t_output_file, headers


def create_launcher(commands_to_execute: Dict[str, List],
                    t_data_server: _rootlogon.DataServer.TDataServer,
                    output_dirname: Path,
                    t_output_file: _rootlogon.Launcher.TOutputFileRow):
    """Create the launcher for Uranie

    Parameters
    ----------
    commands_to_execute : Dict[str, List]
        Name of the script or the command which URANIE will execute with all its arguments.
    t_data_server : _rootlogon.DataServer.TDataServer
        A TDataServer object
    output_dirname : Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation
    t_output_file : _rootlogon.Launcher.TOutputFileRow
        File that will contain the unitary aggregated outputs

    Returns
    -------
    _rootlogon.Launcher.TLauncher
        t_launcher object.
    Path
        Directory where all unitary calculations are stored.
    """
    commands_json_file = output_dirname / URANIE_TCODE_JSON
    with open(commands_json_file, 'w', encoding = 'utf-8') as tcode_file:
        json.dump(commands_to_execute, tcode_file, indent=4)

    command = f'{URANIE_TCODE_LAUNCHER} {commands_json_file} > log.out 2> log.err'
    t_code = _rootlogon.Launcher.TCode(t_data_server, command)

    # we add the output file of the code
    t_code.addOutputFile(t_output_file)

    uranie_work_dir = output_dirname / STUDY_WORKDIR_NAME

    print(t_data_server)
    print(t_code)
    t_launcher = _rootlogon.Launcher.TLauncher(t_data_server, t_code)
    # To back up all directories
    t_launcher.setSave()
    t_launcher.setClean()
    t_launcher.setWorkingDirectory(str(uranie_work_dir))

    return t_launcher, uranie_work_dir


def run_calculations(execution: exe.Execution,
                     t_launcher: _rootlogon.Launcher.TLauncher):
    """Launch the calculation according to the appropriate mode (on your desktop or on a cluster).

    Parameters
    ----------
    execution: execution.Execution
        Object containing all the infos about how to execute the calculations.
    t_launcher : _rootlogon.Launcher.TLauncher
        t_launcher object.

    Raises
    ------
    ValueError
        Invalid execution mode if it's different from 'desktop' or 'cluster'.
    """
    if isinstance(execution, exe.ExecutionLocal):
        if execution.nb_jobs == 1:  # Launching code on a single processor
            # For display during runing
            if execution.visualization:
                t_launcher.setVarDraw("max:initial_power","","") # FIXME lie a integration_bench
        t_launcher.run(f"localhost={execution.nb_jobs}")

    elif isinstance(execution, exe.ExecutionSlurm):
        pass
        #sbatch -n <nb de tâches> -c <nb de cœurs par tâche> -p <partition> --qos=<qos>
        # -A <account> -t <walltime HH:MM:SS> -J <jobname> -o <fichier de sortie>
        # -e <fichier d’erreur> --mail-user=<email> --mail-type=<BEGIN|END|FAIL|ALL>
        # -w <liste des nœuds> myscript.sh
    else:
        raise ValueError(f"Invalid execution mode: {execution.__class__.__name__}")


def _count_of_failed_calculations(uranie_work_dir: Path, unitary_result_filename: str):
    """ Counts the number of failed calculations.

    Parameters
    ----------
    uranie_work_dir : Path
        Absoulut path to the URANIE output directory.
    unitary_result_filename : str
        Name of the file containing the result of the
        aggregations functions for an unitary calculation

    Returns
    -------
    nb_fail : int
        Number of failed calculations.
    """
    list_directories = os.listdir(uranie_work_dir)
    list_directories.remove('UranieResults')
    nb_fail = 0
    for directory in list_directories:
        uranie_results_file = uranie_work_dir / directory / unitary_result_filename
        if not uranie_results_file.is_file():
            nb_fail += 1

    return nb_fail


def save_calculations(propagation: uncertainty_data.Propagation,
                      t_data_server: _rootlogon.DataServer.TDataServer,
                      headers: List,
                      output_dirname: Path,
                      unitary_result_filename: str,
                      uranie_work_dir: Path):
    """Save calculation results in one file for valid calculations,
    and in another for failed calculations (if there is some).

    Parameters
    ----------
    propagation : uncertainty_data.Propagation
        Object containing the name of the propagation method used.
    t_data_server : _rootlogon.DataServer.TDataServer
        A TDataServer object.
    headers : List
        Names of the different aggregations functions
    output_dirname: Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation
    unitary_result_filename : str
        Name of the file containing the result of the
        aggregations functions for an unitary calculation
    uranie_work_dir
        Directory where all unitary calculations are stored.
    """
    # "1.234567890e+00" is the default value used by Uranie when calculation failed.
    nb_fail = _count_of_failed_calculations(uranie_work_dir, unitary_result_filename)

    if nb_fail < propagation.sample_size:
        t_data_server.exportData(str(output_dirname/STUDY_OUTFILE_NAME), "*",
                                 f"{headers[0]}!=1.234567890e+00")

    if nb_fail > 0:
        t_data_server.exportData(str(output_dirname/STUDY_OUTFILE_NAME_FAILED), "*",
                                 f"{headers[0]}==1.234567890e+00")
        utils.info(f"\033[1;31m{nb_fail} over {propagation.sample_size} calculation(s) "
                   "failed !\033[0m")
    elif nb_fail == 0:
        utils.info(f"\033[1;32mAll the {propagation.sample_size} calculation(s) "
                   "have succeeded !\033[0m")
