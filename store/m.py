def strip_suffix(filename):
    """
    Removes the suffix from a filename
    """
    return filename[:filename.rfind('.')]

def test_strip_suffix()