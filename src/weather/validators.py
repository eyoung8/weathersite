from .utils import is_zip, format_address


def validate_location(location):
    if (is_zip(location)):
        pass
    else:
        location = format_address(location)
    return location