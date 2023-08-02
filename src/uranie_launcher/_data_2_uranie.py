"""Contains the implementation of the functions used in launcher.py
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from URANIE import DataServer, Launcher, Sampler
import ROOT

from . import utils, input_data, execution as exe

URANIE_TCODE_LAUNCHER = "uranie-launcher-unitary"
URANIE_TCODE_JSON = ".uranie-launcher-commands.json"

URANIE_FAILED_VALUE = "1.234567890e+00"
"""This is the default value used by Uranie when calculation failed."""


def create_data_server(outputs: input_data.Outputs) -> DataServer.TDataServer:
    """Create the data server for Uranie

    Parameters
    ----------
    outputs : input_data.Outputs
        Object containing the name of the outputs and all the informations about them.

    Returns
    -------
    DataServer.TDataServer
        TDataServer object.
    """

    title = f"Quantities = {[output.quantity_of_interest for output in outputs.outputs]}"
    return DataServer.TDataServer(outputs.name, title)


def set_inputs(inputs: input_data.Inputs, t_data_server: DataServer.TDataServer):
    """Defines the parameters of the distribution law for each uncertains values,
    and associate the variable_name to the flag used in file_flag.

    Parameters
    ----------
    inputs : input_data.Inputs
        Object containing all the infos about the uncertain parameters.
    t_data_server : DataServer.TDataServer
        A TDataServer object

    Raises
    ------
    ValueError
        Invalid distribution type if the variable distribution isn't 'Uniform' or 'TruncatedNormal'.
    """
    for _input in inputs.inputs:
        variable_name = _input.variable_name
        if isinstance(_input.distribution, input_data.Inputs.DistributionUniform):
            t_data_server.addAttribute(DataServer.TUniformDistribution(
                variable_name, _input.distribution.lower_bound, _input.distribution.upper_bound))

        elif isinstance(_input.distribution, input_data.Inputs.DistributionTruncatedNormal):
            mean = _input.distribution.mean
            std_dev = _input.distribution.standard_deviation
            t_data_server.addAttribute(DataServer.TNormalDistribution(
                variable_name, mean, std_dev))
            t_data_server.getAttribute(variable_name).setBounds(
                _input.distribution.lower_bound, _input.distribution.upper_bound)

        else:
            raise ValueError("Invalid distribution type: "
                             f"{_input.distribution.__class__.__name__}")

        t_data_server.getAttribute(variable_name).setFileFlag(str(inputs.file_flag), _input.flag)


def generate_sample(propagation: input_data.Propagation,
                    outputs: input_data.Outputs,
                    t_data_server: DataServer.TDataServer,
                    output_directory: Path
                    ) -> Sampler.TQMC or Sampler.TSampling:
    """Definition of the experimental plan

    Parameters
    ----------
    propagation : input_data.Propagation
        Object containing the name of the propagation method used and the sample size.
    outputs : input_data.Outputs
        Object containing the name of the experimental design file name.
    t_data_server : DataServer.TDataServer
        A TDataServer object
    output_directory: Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation
    Returns
    -------
    Sampler.TQMC or Sampler.TSampling
        t_sampler object containing the experimental plan.

    Raises
    ------
    ValueError
        Invalid sampling method if the sampling method is not 'SRS' or 'Sobol'.
    """
    if propagation.sampling_method == propagation.SOBOL:
        # here I considered that canvas was deterministic
        t_sampler = Sampler.TQMC(
            t_data_server, propagation.sampling_method, propagation.sample_size)
    elif propagation.sampling_method == propagation.SRS:
        t_sampler = Sampler.TSampling(
            t_data_server, propagation.sampling_method, propagation.sample_size)
    else:
        raise ValueError(f"Unknown sampling method: {propagation.sampling_method}")

    t_sampler.generateSample()

    t_data_server.exportData(str(output_directory / outputs.experimental_design_filename))

    return t_sampler


def visualisation(t_data_server: DataServer.TDataServer):  # pragma: no cover
    """Plot a graph if the visualization variable is equal to True

    Parameters
    ----------
    t_data_server : DataServer.TDataServer
        A TDataServer object
    """
    ROOT.gROOT.SetBatch(False)  # pylint: disable=no-member
    canvas = ROOT.TCanvas()  # pylint: disable=no-member
    canvas.Clear()
    t_data_server.drawPairs()
    canvas.Draw()


def set_outputs(outputs: input_data.Outputs) -> List[Launcher.TOutputFileRow]:
    """Prepares the unitary aggregated outputs file.

    Parameters
    ----------
    outputs : input_data.Outputs
        Object containing the name of the outputs and all the informations about them.

    Returns
    -------
    List[Launcher.TOutputFileRow]
        List of file that will contain the unitary aggregated outputs
    """
    # The output files of the code
    t_output_files = []

    # The attribute in the output file
    for output in outputs.outputs:
        t_output_file = Launcher.TOutputFileRow(output.filename)
        for header in output.headers:
            t_output_file.addAttribute(DataServer.TAttribute(header))
        t_output_files.append(t_output_file)
    return t_output_files


def create_launcher(commands_to_execute: Dict[str, List],
                    t_data_server: DataServer.TDataServer,
                    output_directory: Path,
                    t_output_files: List[Launcher.TOutputFileRow]
                    ) -> Launcher.TLauncher:
    """Create the launcher for Uranie

    Parameters
    ----------
    commands_to_execute : Dict[str, List]
        Name of the script or the command which URANIE will execute with all its arguments.
    t_data_server : DataServer.TDataServer
        A TDataServer object
    output_directory : Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation
    t_output_files : List[Launcher.TOutputFileRow]
        List of files that will contain the unitary aggregated outputs

    Returns
    -------
    Launcher.TLauncher
        t_launcher object.
    """
    commands_json_file = output_directory / URANIE_TCODE_JSON
    with open(commands_json_file, 'w', encoding='utf-8') as tcode_file:
        json.dump(commands_to_execute, tcode_file, indent=4)

    command = [URANIE_TCODE_LAUNCHER, str(commands_json_file), "> log.out 2> log.err"]
    if utils.get_log_level() >= utils.DEBUG:
        command.insert(1, "--debug")
    t_code = Launcher.TCode(t_data_server, " ".join(command))

    # we add the output file of the code
    for t_output_file in t_output_files:
        t_code.addOutputFile(t_output_file)

    return Launcher.TLauncher(t_data_server, t_code)


def run_calculations(execution: exe.Execution,
                     t_launcher: Launcher.TLauncher,
                     output_directory: Path) -> Path:
    """Launch the calculation according to the appropriate mode (on your desktop or on a cluster).

    Parameters
    ----------
    execution: execution.Execution
        Object containing all the infos about how to execute the calculations.
    t_launcher : Launcher.TLauncher
        t_launcher object.
    output_directory : Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation

    Raises
    ------
    ValueError
        Invalid execution mode if it's different from 'desktop' or 'cluster'.
    ValueError
        execution.clean and output_directory == execution.working_directory is not possible.
    """

    # To back up all directories
    t_launcher.setSave(execution.save)
    t_launcher.setClean(execution.clean)

    # Uranie working directory
    t_launcher.setWorkingDirectory(str(execution.working_directory))

    if output_directory == execution.working_directory and execution.clean:
        raise ValueError(
            "execution.clean is True and output_directory == "
            "execution.working_directory is not possible.")

    if isinstance(execution, exe.ExecutionLocal):
        if execution.nb_jobs == 1:  # Launching code on a single processor
            # For display during runing
            if execution.visualization:  # pragma: no cover
                t_launcher.setVarDraw("max:initial_power", "", "")  # FIXME lie a integration_bench
            t_launcher.run()
        else:
            t_launcher.run(f"localhost={execution.nb_jobs}")

    # elif isinstance(execution, exe.ExecutionSlurm):
    #     pass
    #     #sbatch -n <nb de tâches> -c <nb de cœurs par tâche> -p <partition> --qos=<qos>
    #     # -A <account> -t <walltime HH:MM:SS> -J <jobname> -o <fichier de sortie>
    #     # -e <fichier d’erreur> --mail-user=<email> --mail-type=<BEGIN|END|FAIL|ALL>
    #     # -w <liste des nœuds> myscript.sh
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
    int
        Number of failed calculations.
    """
    list_directories = os.listdir(uranie_work_dir)
    list_directories.remove('UranieResults')
    nb_fail = 0
    for directory in list_directories:
        uranie_results_file = uranie_work_dir / directory / unitary_result_filename
        utils.debug(f"Check output {uranie_results_file}: {uranie_results_file.is_file()}")
        if not uranie_results_file.is_file():
            nb_fail += 1

    return nb_fail


def save_calculations(propagation: input_data.Propagation,
                      execution: exe.Execution,
                      outputs: input_data.Outputs,
                      t_data_server: DataServer.TDataServer,
                      output_directory: Path) -> Tuple[Path, int]:
    """Save calculation results in one file for valid calculations,
    and in another for failed calculations (if there is some).

    Parameters
    ----------
    propagation : input_data.Propagation
        Object containing the name of the propagation method used.
    execution: execution.Execution
        Object containing all the infos about how to execute the calculations.
    outputs : input_data.Outputs
        Object containing the outputs of the study to recover output filename.
    t_data_server : DataServer.TDataServer
        A TDataServer object.
    output_directory: Path
        Name of the directory where are stored the results
        of the uncertainty quantification calculation

    Returns
    -------
    Tuple[Path, int]
        Path to output file defined as ``output_directory/outputs.output_filename``
        and nb of failed.
    """

    output0 = outputs.outputs[0]
    nb_fail = _count_of_failed_calculations(execution.working_directory, output0.filename)

    ascii_filepath = output_directory / outputs.output_filename

    # Some succeded
    if nb_fail < propagation.sample_size:
        t_data_server.exportData(
            str(ascii_filepath), "*", f"{output0.headers[0]}!={URANIE_FAILED_VALUE}")

    if utils.get_log_level() >= utils.INFO:
        t_data_server.scan()

    # Some failed
    if nb_fail > 0:
        utils.info(f"\033[1;31m{nb_fail} over {propagation.sample_size} calculation(s) "
                   "failed !\033[0m")
        utils.debug(f"export failed simulations to {output_directory/outputs.failed_filename}.")
        utils.debug(f" -> condition: {output0.headers[0]}=={URANIE_FAILED_VALUE}")
        t_data_server.exportData(str(output_directory/outputs.failed_filename), "*",
                                 f"{output0.headers[0]}=={URANIE_FAILED_VALUE}")
    else:
        utils.info(f"\033[1;32mAll the {propagation.sample_size} calculation(s) "
                   "have succeeded !\033[0m")

    return ascii_filepath, nb_fail
