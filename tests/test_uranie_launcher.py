import json
import shutil
import pytest
from pathlib import Path
from typing import List

from URANIE import DataServer, Sampler

from . import program_tester

from uranie_launcher import execution as exe
from uranie_launcher import launcher
from uranie_launcher import input_data
from uranie_launcher import _data_2_uranie
from uranie_launcher import _run_unitary



## _run_unitary
def test_program_tester():

    output_dirname = Path(__file__).absolute().parent / "test_program_tester"
    output_dirname.mkdir(parents=False, exist_ok=True)
    data_filepath = output_dirname / "input_for_tests.json"

    data_filepath.write_text(json.dumps({"uncertain_variable": 250}), encoding="utf-8")
    program_tester.main_unitary_calculation([str(data_filepath), str(output_dirname)])
    assert (output_dirname / "result").is_file()


    data_filepath.write_text(json.dumps({"uncertain_variable": 249}), encoding="utf-8")
    with pytest.raises(ZeroDivisionError) as error:
        program_tester.main_unitary_calculation([str(data_filepath), str(output_dirname)])


def test_run_unitary():
    pass


## launcher
def test_launcher(commands_to_execute,
                  data_input_inputs_distribution_uniform,
                  data_input_outputs): #FIXME : Could be a better test...

    output_dirname = Path(__file__).absolute().parent / "test_launcher"
    if output_dirname.exists():
        shutil.rmtree(output_dirname)
    output_dirname.mkdir(parents=False, exist_ok=True)

    sample_size = 4
    propagation = input_data.Propagation(sampling_method=input_data.Propagation.SOBOL,
                                         sample_size=sample_size)

    execution = exe.ExecutionLocal(
        working_directory=output_dirname / "unitary", nb_jobs=sample_size)

    ascii_filepath, nb_failed = launcher.execute_uranie(
        commands_to_execute=commands_to_execute,
        inputs=data_input_inputs_distribution_uniform,
        propagation=propagation,
        outputs=data_input_outputs,
        execution=execution,
        output_directory=output_dirname)

    assert (
        nb_failed == 0 and
        ascii_filepath.exists()
    )
