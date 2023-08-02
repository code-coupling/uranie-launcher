import pytest
from pathlib import Path

from URANIE import DataServer, Sampler

from uranie_launcher import execution, input_data, _data_2_uranie

## create_data_server
def test_create_data_server(t_data_server, data_server_name, quantity_of_interest):

    assert (
        isinstance(t_data_server, DataServer.TDataServer) and
        str(t_data_server) == (f"Name: {data_server_name} "
                               f"Title: Quantities = ['{quantity_of_interest}']") and
        t_data_server.GetName() == data_server_name and
        t_data_server.GetTitle() == f"Quantities = ['{quantity_of_interest}']"
    )


## set_inputs
def test_set_inputs_distribution_unknown(t_data_server, simulation_variable, tag_filename): #FIXME : Could be a better test...

    inputs = input_data.Inputs()
    inputs.add_input(input_data.Inputs.Input(variable_name=simulation_variable, distribution=None))
    inputs.set_file_flag(Path(__file__).absolute().parent / tag_filename)

    with pytest.raises(ValueError) as error:
        _data_2_uranie.set_inputs(inputs, t_data_server)
    assert (
        f"Invalid distribution type: NoneType" in str(error.value)
    )


def test_set_inputs_distribution_uniform(
        t_data_server, data_input_inputs_distribution_uniform, simulation_variable): #FIXME : Could be a better test...


    _data_2_uranie.set_inputs(data_input_inputs_distribution_uniform, t_data_server)

    assert (
        isinstance(t_data_server.getAttribute(simulation_variable),
                   DataServer.TUniformDistribution) and
        str(t_data_server.getAttribute(simulation_variable)) == (
            f"Name: {simulation_variable} Title: {simulation_variable}") and
        t_data_server.getAttribute(simulation_variable).GetName() == simulation_variable and
        t_data_server.getAttribute(simulation_variable).GetTitle() == simulation_variable and
        t_data_server.getAttribute(simulation_variable).getLowerBound() == 100 and
        t_data_server.getAttribute(simulation_variable).getUpperBound() == 1000
        # test the filFlag value...
    )


def test_set_inputs_distribution_truncated_normal(t_data_server,
                                                  data_input_inputs_distribution_truncated_normal,
                                                  simulation_variable): #FIXME : Could be a better test...

    _data_2_uranie.set_inputs(data_input_inputs_distribution_truncated_normal, t_data_server)

    assert (
        isinstance(t_data_server.getAttribute(simulation_variable),
                   DataServer.TNormalDistribution) and
        str(t_data_server.getAttribute(simulation_variable)) == (
            f"Name: {simulation_variable} Title: {simulation_variable}") and
        t_data_server.getAttribute(simulation_variable).GetName() == simulation_variable and
        t_data_server.getAttribute(simulation_variable).GetTitle() == simulation_variable and
        t_data_server.getAttribute(simulation_variable).getLowerBound() == 100 and
        t_data_server.getAttribute(simulation_variable).getUpperBound() == 1000 and
        t_data_server.getAttribute(simulation_variable).getParameterMu() == 600 and
        t_data_server.getAttribute(simulation_variable).getParameterSigma() == 100
        # test the filFlag value...
    )

## generate_sample
def test_generate_sobol_sample(generate_sample, t_data_server): #FIXME : Could be a better test...

    sampler = generate_sample(Path("some/path/to/output_dirname"),
                              t_data_server,
                              input_data.Propagation.SOBOL,
                              4)

    assert (
        isinstance(sampler, Sampler.TQMC) and
        sampler.getMethodName() == "qMC_sobol" and
        sampler.GetName() == f"Sampling_qMC_sobol_4" and
        sampler.GetTitle() == f"Uranie 4 sample with qMC method sobol"
    )


def test_generate_srs_sample(generate_sample, t_data_server): #FIXME : Could be a better test...

    sampler = generate_sample(Path("some/path/to/output_dirname"),
                              t_data_server,
                              input_data.Propagation.SRS,
                              4)

    assert (
        isinstance(sampler, Sampler.TSampling) and
        sampler.getMethodName() == "SRS" and
        sampler.GetName() == f"Sampling_srs_4" and
        sampler.GetTitle() == f"Uranie 4 sample with method srs"
    )


def test_generate_unknown_sample(generate_sample, t_data_server):


    with pytest.raises(ValueError) as error:
        generate_sample(Path("some/path/to/output_dirname"),
                        t_data_server,
                        "unknown_method",
                        4)
    assert f"Unknown sampling method: unknown_method" in str(error.value)

@pytest.mark.skip(reason="Not implemented yet")
def test_visualisation(t_data_server, mocker):

    import ROOT

    # Mock les méthodes et les objets nécessaires
    mocker.patch.object(ROOT.gROOT, 'SetBatch')
    mocker.patch.object(ROOT, 'TCanvas')
    mocker.patch.object(t_data_server, 'drawPairs')

    # Appeler la fonction à tester
    _data_2_uranie.visualisation(t_data_server)

    # Vérifier l'appel des méthodes et des objets
    ROOT.gROOT.SetBatch.assert_called_once_with(False)
    ROOT.TCanvas.assert_called_once_with()
    t_data_server.drawPairs.assert_called_once_with()


def test_set_outputs(t_output_files, result_filename): #FIXME : Could be a better test...

    assert (str(t_output_files[0]) ==
            f"Name: {result_filename} Title: TCodeFile with name[{result_filename}]")


def test_create_launcher(generate_t_launcher):

    output_dirname = Path(__file__).absolute().parent / "test_create_launcher"
    output_dirname.mkdir(parents=True, exist_ok=True)

    t_launcher = generate_t_launcher(output_dirname)


def test_run_calculation_local_parallel(generate_t_launcher): #FIXME : Could be a better test...

    output_dirname = Path(__file__).absolute().parent / "test_run_calculation_local_parallel"
    output_dirname.mkdir(parents=True, exist_ok=True)

    t_launcher = generate_t_launcher(output_dirname)

    exec = execution.ExecutionLocal(working_directory=output_dirname / "unitary", nb_jobs=2)

    _data_2_uranie.run_calculations(execution=exec,
                                    t_launcher=t_launcher,
                                    output_directory=output_dirname)

    assert (
        t_launcher.getWorkingDirectory() == str(output_dirname / "unitary") and
        t_launcher.getSave() == True and
        t_launcher.getClean() == True
    )


def test_run_calculation_local_sequentiel(generate_t_launcher): #FIXME : Could be a better test...

    output_dirname = Path(__file__).absolute().parent / "test_run_calculation_local_sequentiel"
    output_dirname.mkdir(parents=True, exist_ok=True)

    t_launcher = generate_t_launcher(output_dirname)

    exec = execution.ExecutionLocal(working_directory=output_dirname / "unitary", nb_jobs=1)

    _data_2_uranie.run_calculations(execution=exec,
                                    t_launcher=t_launcher,
                                    output_directory=output_dirname)

    assert (
        t_launcher.getWorkingDirectory() == str(output_dirname / "unitary") and
        t_launcher.getSave() == True and
        t_launcher.getClean() == True
    )


def test_run_calculation_raise(generate_t_launcher): #FIXME : Could be a better test...

    output_dirname = Path(__file__).absolute().parent / "test_run_calculation_raise"
    output_dirname.mkdir(parents=True, exist_ok=True)

    t_launcher = generate_t_launcher(output_dirname)

    with pytest.raises(ValueError) as error:
        exec = execution.ExecutionLocal(working_directory=output_dirname, nb_jobs=1)
        _data_2_uranie.run_calculations(execution=exec,
                                        t_launcher=t_launcher,
                                        output_directory=output_dirname)

    assert ("execution.clean is True and output_directory =="
            " execution.working_directory is not possible.") in str(error.value)

    with pytest.raises(ValueError) as error:
        exec = execution.Execution(working_directory=output_dirname / "unitary")
        _data_2_uranie.run_calculations(execution=exec,
                                        t_launcher=t_launcher,
                                        output_directory=output_dirname)

    assert ("Invalid execution mode: Execution") in str(error.value)


def test_save_calculations(generate_final_results): #FIXME : Could be a better test...

    output_dirname = Path(__file__).absolute().parent / "test_save_calculations"
    output_dirname.mkdir(parents=True, exist_ok=True)

    output_file, nb_fails = generate_final_results(output_dirname=output_dirname, sample_size=4)

    assert output_file.is_file()
    assert nb_fails == 0


def test_save_calculations_1_fail(generate_final_results): #FIXME : Could be a better test...

    output_dirname = Path(__file__).absolute().parent / "test_save_calculations_1_fail"
    output_dirname.mkdir(parents=True, exist_ok=True)
    output_file, nb_fails = generate_final_results(output_dirname=output_dirname, sample_size=10)

    assert output_file.is_file()
    assert nb_fails == 1
