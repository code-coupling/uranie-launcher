"""Tests ``utils`` module."""

import pytest

from uranie_launcher import utils


def test_set_verbosity():

    new_log_level = 2
    utils.set_verbosity(new_log_level)

    assert (
        utils._log_level == new_log_level
    )


def test_set_verbosity_lower_that_min_bound():

    new_log_level = -1
    old_log_level = utils.get_log_level()

    with pytest.raises(ValueError) as error:
        utils.set_verbosity(new_log_level)
    assert (
        f"log_level must be in [{utils.NONE};{utils.DEBUG}]" in str(error.value)
    )

    assert old_log_level == utils.get_log_level()


def test_set_verbosity_greater_that_upper_bound():

    new_log_level = 3
    old_log_level = utils.get_log_level()

    with pytest.raises(ValueError) as error:
        utils.set_verbosity(new_log_level)
    assert (
        f"log_level must be in [{utils.NONE};{utils.DEBUG}]" in str(error.value)
    )

    assert old_log_level == utils.get_log_level()


def test_log(capsys):

    new_log_level = 1
    utils.set_verbosity(new_log_level)
    message_log = "un message de log"
    utils.log(utils.INFO, message_log)

    # Capture output
    captured_log = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_log.out == f"{message_log}\n"
    )


def test_no_info_output_when_log_level_below_info(capsys):

    new_log_level = utils.NONE
    utils.set_verbosity(new_log_level)

    message_info = "un message d'info"
    utils.info(message_info)

    # Capture output
    captured_info = capsys.readouterr()

    message_debug = "un message de debug"
    utils.debug(message_debug)

    # Capture output
    captured_debug = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_info.out == "" and
        captured_debug.out == ""
        )


def test_no_debug_output_when_log_level_below_debug(capsys):

    new_log_level = utils.INFO
    utils.set_verbosity(new_log_level)

    message_info = "un message d'info"
    utils.info(message_info)

    # Capture output
    captured_info = capsys.readouterr()

    message_debug = "un message de debug"
    utils.debug(message_debug)

    # Capture output
    captured_debug = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_info.out == f"{message_info}\n" and
        captured_debug.out == ""
        )


def test_all_output_when_log_level_set_to_debug(capsys):

    new_log_level = utils.DEBUG
    utils.set_verbosity(new_log_level)

    message_info = "un message d'info"
    utils.info(message_info)

    # Capture output
    captured_info = capsys.readouterr()

    message_debug = "un message de debug"
    utils.debug(message_debug)

    # Capture output
    captured_debug = capsys.readouterr()

    assert (
        utils._log_level == new_log_level and
        captured_info.out == f"{message_info}\n" and
        captured_debug.out == f"{message_debug}\n"
        )
