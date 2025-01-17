from pathlib import Path
from unittest.mock import MagicMock, ANY

import pytest

from secureli.abstractions.pre_commit import LanguageNotSupportedError
from secureli.actions.action import ActionDependencies
from secureli.actions.initializer import InitializerAction
from secureli.services.logging import LogAction

test_folder_path = Path("does-not-matter")


@pytest.fixture()
def mock_scanner() -> MagicMock:
    mock_scanner = MagicMock()
    return mock_scanner


@pytest.fixture()
def mock_updater() -> MagicMock:
    mock_updater = MagicMock()
    return mock_updater


@pytest.fixture()
def action_deps(
    mock_echo: MagicMock,
    mock_language_analyzer: MagicMock,
    mock_language_support: MagicMock,
    mock_scanner: MagicMock,
    mock_secureli_config: MagicMock,
    mock_updater: MagicMock,
    mock_pre_commit: MagicMock,
) -> ActionDependencies:
    return ActionDependencies(
        mock_echo,
        mock_language_analyzer,
        mock_language_support,
        mock_scanner,
        mock_secureli_config,
        mock_updater,
        mock_pre_commit,
    )


@pytest.fixture()
def initializer_action(
    action_deps: ActionDependencies,
    mock_logging_service: MagicMock,
) -> InitializerAction:
    return InitializerAction(
        action_deps=action_deps,
        logging=mock_logging_service,
    )


def test_that_initialize_repo_does_not_load_config_when_resetting(
    initializer_action: InitializerAction,
    mock_secureli_config: MagicMock,
    mock_echo: MagicMock,
    mock_logging_service: MagicMock,
):
    initializer_action.initialize_repo(test_folder_path, True, True)

    mock_secureli_config.load.assert_not_called()

    mock_logging_service.success.assert_called_once_with(LogAction.init)


def test_that_initialize_repo_logs_failure_when_failing_to_verify(
    initializer_action: InitializerAction,
    mock_secureli_config: MagicMock,
    mock_language_analyzer: MagicMock,
    mock_logging_service: MagicMock,
):
    mock_language_analyzer.analyze.side_effect = LanguageNotSupportedError

    initializer_action.initialize_repo(test_folder_path, True, True)

    mock_logging_service.failure.assert_called_once_with(LogAction.init, ANY)
