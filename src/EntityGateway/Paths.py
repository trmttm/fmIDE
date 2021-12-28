def get_path(directory, file_name: str):
    try:
        path = directory / file_name
    except TypeError:
        path = f'{directory}{file_name}'
    return path
