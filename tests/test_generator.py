
import pytest
from core.utils.generator import filename_generator

def test_filename_generator_basic():
    """
    Test basic functionality with simple inputs.
    """
    filenames = filename_generator(trials=1, locations=1, lump_status=["LUMP"])
    assert filenames == ["TRIAL_1_LOC_1_LUMP"]

def test_filename_generator_multiple():
    """
    Test with multiple trials, locations, and lump statuses.
    """
    filenames = filename_generator(trials=2, locations=2, lump_status=["LUMP", "NOLUMP"])
    expected = [
        "TRIAL_1_LOC_1_LUMP",
        "TRIAL_1_LOC_1_NOLUMP",
        "TRIAL_1_LOC_2_LUMP",
        "TRIAL_1_LOC_2_NOLUMP",
        "TRIAL_2_LOC_1_LUMP",
        "TRIAL_2_LOC_1_NOLUMP",
        "TRIAL_2_LOC_2_LUMP",
        "TRIAL_2_LOC_2_NOLUMP",
    ]
    assert filenames == expected

def test_filename_generator_empty_status():
    """
    Test with an empty lump_status list.
    """
    filenames = filename_generator(trials=1, locations=1, lump_status=[])
    assert filenames == []

def test_filename_generator_invalid_status():
    """
    Test with an invalid lump status value.
    """
    with pytest.raises(ValueError):
        filename_generator(trials=1, locations=1, lump_status=["INVALID"])
