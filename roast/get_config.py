from roast import match_path

def get_config(cfg, type_, path):
    found = None
    for section in cfg.sections():
        try:
            (type, glob) = section.split(None, 1)
        except ValueError:
            continue
        if type != type_:
            continue
        if not match_path.match_path(
            path=path,
            glob=glob,
            ):
            continue
        if found is None:
            found = {}
        found.update(cfg.items(section))

    return found
