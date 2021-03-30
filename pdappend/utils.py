def _or(this, that):
    if this is None:
        return that

    else:
        return this

    return that


def str_to_bool(string):
    if isinstance(string, bool):
        return string

    if string is None:
        return False

    if string.lower() in ("yes", "true", "t", "y", "1"):
        return True

    elif string.lower() in ("no", "false", "f", "n", "0"):
        return False

    return False
