"""
Testing elements of a Learning instance
"""
import pytest
import json

from typing import Callable

from application.lib.instance_generation.instance_generation_main import new_instance

from application.lib.config_generation.config_file_structure import (
    generate_test_input_config_as_json,
    generate_full_run_test_input_config_as_json,
)
from application.lib.config_generation.generate_config_data import (
    generate_instance_configuration_data,
)


@pytest.mark.django_db
@pytest.fixture(name="test_learning_instance")
def setup_instance():
    """
    Set up a new learning instance for testing
    """
    config = generate_full_run_test_input_config_as_json(
        test_instance_id="test_instance"
    )
    test_learning_instance = new_instance(input_config=config)

    return test_learning_instance


@pytest.mark.django_db
def test_instance_generators(test_learning_instance: object):
    """
    Test the learning instance has been correctly configured
    """

    assert isinstance(test_learning_instance.agent_generater_partial, Callable)
    assert isinstance(test_learning_instance.alt_agent_generator, Callable)


@pytest.mark.django_db
def test_alt_run_generation(test_learning_instance: object):
    """
    Testing the alt approach of run generation
    """
