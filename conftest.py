# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""
Configuration file for Pytest
"""

import os
import os.path as osp
import shutil

# To activate/deactivate certain things for pytest's only
# NOTE: Please leave this before any other import here!!
os.environ['SPYDER_PYTEST'] = 'True'

import pytest

# Local imports
from spyder.tests.fixtures.file_fixtures import create_folders_files
from spyder.tests.fixtures.bookmark_fixtures import (code_editor_bot,
                                                     setup_editor)
from spyder.plugins.editor.lsp.tests.fixtures import lsp_manager, qtbot_module
from spyder.plugins.editor.widgets.tests.fixtures import lsp_codeeditor

# Remove temp conf_dir before starting the tests
from spyder.config.base import get_conf_path
conf_dir = get_conf_path()
if osp.isdir(conf_dir):
    shutil.rmtree(conf_dir)


def pytest_addoption(parser):
    """Add option to run slow tests."""
    parser.addoption("--run-slow", action="store_true",
                     default=False, help="Run slow tests")


def pytest_collection_modifyitems(config, items):
    """Skip tests with the slow marker"""
    if config.getoption("--run-slow"):
        # --run-slow given in cli: do not skip slow tests
        return

    skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
