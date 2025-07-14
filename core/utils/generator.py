from typing import List

def filename_generator(
    trials: int = 1,
    locations: int = 1,
    lump_status: List[str] = list()
) -> List[str]:
    """
    Generate filenames based on trial count, location count, and lump status.

    Args:
        trials (int): Number of trials (e.g., 3).
        locations (int): Number of locations (e.g., 2).
        lump_status (List[str]): List of conditions ['LUMP', 'NOLUMP'].

    Returns:
        List[str]: List of filenames in format TRIAL_<trial>_LOC_<location>_<status>
    """
    if lump_status is None:
        lump_status = []

    valid_statuses = {"LUMP", "NOLUMP"}
    invalid = [s for s in lump_status if s not in valid_statuses]
    if invalid:
        raise ValueError(f"Invalid lump status values: {invalid}. Allowed: {valid_statuses}")

    filenames = []
    for trial in range(1, trials + 1):
        for location in range(1, locations + 1):
            for status in lump_status:
                filenames.append(f"TRIAL_{trial}_LOC_{location}_{status}")
    return filenames