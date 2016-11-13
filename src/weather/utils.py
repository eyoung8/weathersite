
def validate_location(location):
    if (is_zip(location)):
        pass
    else:
        location = format_address(location)
    return location

def is_zip(location):
    is_zip = True
    if (len(location) == 5):
        try:
            int(location)
            is_zip = not '-' in location
        except ValueError:
            is_zip = False
    else:
        is_zip = False     
    return is_zip

def format_address(location):
    location = location.lower()
    split_location = location.split(',')
    location = []
    for part in split_location:
        part = remove_whitespace(part)
        location.append(part)
    return ' '.join(location)

def remove_whitespace(str):
    return "".join(str.split())