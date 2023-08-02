"""Tests ``execution`` module."""

import pytest

from uranie_launcher import execution



## execution
def test_execution_default():
    """test exec default"""

    exe = execution.Execution(working_directory=".")

    assert (
        exe.working_directory == "." and
        exe.clean is True and
        exe.save == -1 and
        exe.visualization is False
    )


def test_execution_enable_visualization():
    """test exec enable visualization"""

    exe = execution.Execution(working_directory=".")
    exe.enable_visualization()
    exe.clean_outputs(False)
    exe.save_outputs(0)

    assert (
        exe.clean is False and
        exe.save == 0 and
        exe.visualization is True
    )


def test_execution_local():
    """test local exec"""

    with pytest.raises(ValueError) as error:
        execution.ExecutionLocal(working_directory=".", nb_jobs=0)
    assert "nb_jobs' (0) must be >=1." in str(error.value)

    nb_jobs = 2
    exe = execution.ExecutionLocal(working_directory="test_execution_local", nb_jobs=nb_jobs)

    assert (
        exe.visualization is False and
        exe.nb_jobs == nb_jobs
    )


def test_execution_slurm_raise():
    """test slurm exec"""

    with pytest.raises(NotImplementedError) as error:
        execution.ExecutionSlurm()
    assert "Execution on cluster is not implemented yet" in str(error.value)
