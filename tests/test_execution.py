"""Tests ``execution`` module."""

import pytest

from uranie_launcher import execution



## execution
def test_execution_default():

    exec = execution.Execution(working_directory=".")

    assert (
        exec.working_directory == "." and
        exec.clean == True and
        exec.save == -1 and
        exec.visualization is False
    )


def test_execution_enable_visualization():

    exec = execution.Execution(working_directory=".")
    exec.enable_visualization()
    exec.clean_outputs(False)
    exec.save_outputs(0)

    assert (
        exec.clean == False and
        exec.save == 0 and
        exec.visualization is True
    )


def test_execution_local():


    with pytest.raises(ValueError) as error:
        exec = exec = execution.ExecutionLocal(working_directory=".", nb_jobs=0)
    assert "nb_jobs' (0) must be >=1." in str(error.value)

    nb_jobs = 2
    exec = execution.ExecutionLocal(working_directory="test_execution_local", nb_jobs=nb_jobs)

    assert (
        exec.visualization is False and
        exec.nb_jobs == nb_jobs
    )


def test_execution_slurm_raise_NotImplementedError():

    with pytest.raises(NotImplementedError) as error:
        exec = execution.ExecutionSlurm()
    assert "Execution on cluster is not implemented yet" in str(error.value)
