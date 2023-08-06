# -*- coding: utf-8 -*-
"""
    fsnviz.tests.test_general
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Main command tests.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from click.testing import CliRunner

from fsnviz.main import cli


def test_help():
    runner = CliRunner()
    cmd = runner.invoke(cli, ["--help"])
    assert cmd.exit_code == 0
