import os

def ensure_subdirectory(base_dir, sub_dir_name):
    """
    Creates a subdirectory inside the given base directory only if it doesn't already exist.
    
    Parameters:
        base_dir (str): The path to the base directory.
        sub_dir_name (str): The name of the subdirectory to create.
        
    Returns:
        str: Full path to the created subdirectory.
        
    Raises:
        FileNotFoundError: If the base directory does not exist.
        FileExistsError: If the subdirectory already exists.
    """
    if not os.path.isdir(base_dir):
        raise FileNotFoundError(f"Base directory does not exist: {base_dir}")

    sub_dir_path = os.path.join(base_dir, sub_dir_name)

    if os.path.exists(sub_dir_path):
        raise FileExistsError(f"Subdirectory already exists: {sub_dir_path}")

    os.makedirs(sub_dir_path)
    print(f"Created subdirectory: {sub_dir_path}")
    return sub_dir_path
