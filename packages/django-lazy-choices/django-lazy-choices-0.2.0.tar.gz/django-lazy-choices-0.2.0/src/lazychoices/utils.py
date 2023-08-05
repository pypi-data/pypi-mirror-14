def flatten_choices(choices):
    flat = []
    for choice, value in choices:
        if isinstance(value, (list, tuple)):
            flat.extend(value)
        else:
            flat.append((choice, value))
    return flat
