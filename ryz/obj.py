def get_fqname(obj: object):
    # ref: https://stackoverflow.com/a/2020083/14748231
    klass = obj.__class__
    module = klass.__module__
    if (
            module is None
            # avoid outputs like "builtins.str"
            or module == "builtins"):
        return klass.__qualname__
    return module + "." + klass.__qualname__
