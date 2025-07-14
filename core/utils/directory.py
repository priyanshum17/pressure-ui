import logging
from pathlib import Path

from core.config.setting import settings


def create_dir(base_dir: str, sub_dir: str) -> Path:
    """
    Ensure base_dir/sub_dir exists. If sub_dir exists, create an alternative.

    Args:
        base_dir (str): The root directory (e.g., "data").
        sub_dir (str): Subdirectory name (e.g., experiment name).

    Returns:
        Path: The created directory path (or an alternative one).
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        base_path.mkdir(parents=True)
        logging.info(f'Base directory "{base_path.resolve()}" created.')

    target_path = base_path / sub_dir
    if target_path.exists():
        alt_path = find_alternative_names(target_path)
        logging.warning(
            f'Directory "{target_path.resolve()}" exists. '
            f'Using alternative: "{alt_path.resolve()}".'
        )
        return alt_path

    target_path.mkdir()
    logging.info(f'Directory "{target_path.resolve()}" created successfully.')
    return target_path


def find_alternative_names(base_path: Path) -> Path:
    for suffix in range(settings.ALTERNATIVE_LIMIT):
        alt_path = base_path.with_name(f"{base_path.name}_{suffix}")
        if not alt_path.exists():
            alt_path.mkdir()
            return alt_path

    logging.error(
        f"Exceeded ALTERNATIVE_LIMIT while trying to create alt path for {base_path}"
    )
    return Path()
