import sys
import os

import pytest

import virtual_environments
from service_messages import ServiceMessage, assert_service_messages
from test_util import run_command, get_teamcity_messages_root


@pytest.fixture(scope='module', params=["django"])
def venv(request):
    if sys.version_info < (3, 5):
        pytest.skip("Django >2.0 requires Python 3.5+")
    return virtual_environments.prepare_virtualenv([request.param])


def test_smoke(venv):
    output = run(venv, os.path.join(get_teamcity_messages_root(), "tests", "guinea-pigs", "djangotest2"))

    test_name = "test_smoke.SmokeTestCase.test_xxx (XXX identity)"
    assert_service_messages(
        output,
        [
            ServiceMessage('testCount', {'count': "1"}),
            ServiceMessage('testStarted', {'name': test_name}),
            ServiceMessage('testFinished', {'name': test_name}),
        ])


def run(venv, project_root):
    command = os.path.join(os.getcwd(), venv.bin, 'python') + " manage.py test"
    return run_command(command, cwd=project_root)
