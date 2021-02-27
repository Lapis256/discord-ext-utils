from pathlib import Path


__all_ = ("get_extensions")


def get_extensions(directory, recursive=True):
    path = Path(directory)
    parent = None
    exts = []

    for module in path.glob("**/*.py"):
        _parent = module.parent
        if parent and _parent.is_relative_to(parent):
            continue

        if module.name == "__init__.py" and (recursive or _parent.parent == path):
            parent = _parent
            exts.append(_parent)
        elif (recursive or _parent == path):
            exts.append(module.with_suffix(""))

    return [str(ext).replace("/", ".") for ext in exts]
