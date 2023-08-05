# -*- coding: utf-8 -*-
import pytest

@pytest.mark.tryfirst
def pytest_runtest_logreport(report):
    """Overwrite report by removing any captured stderr."""
    # print("PLUGIN SAYS -> report -> {0}".format(report))
    # print("PLUGIN SAYS -> report.sections -> {0}".format(report.sections))
    # print("PLUGIN SAYS -> dir(report) -> {0}".format(dir(report)))
    # print("PLUGIN SAYS -> type(report) -> {0}".format(type(report)))
    sections = [item for item in report.sections if item[0] not in ("Captured stdout call", "Captured stderr call", "Captured stdout setup", "Captured stderr setup", "Captured stdout teardown", "Captured stderr teardown")]
    # print("PLUGIN SAYS -> sections -> {0}".format(sections))
    report.sections = sections
