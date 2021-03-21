from pathlib import Path


__all__ = ("get_extensions", )


def _is_exclude(exclude_parents, path):
    for parent in exclude_parents:
        if path.is_relative_to(parent):
            return True
    return False


def get_extensions(directory, recursive=True):
    path = Path(directory)
    exclude_parents = []
    extensions = []

    for file in (path.rglob if recursive else path.glob)("*"):
        _parent = file.parent

        if file.name.startswith("_"):
            if file.is_dir():
                exclude_parents.append(file)
            continue

        if _is_exclude(exclude_parents, _parent):
            continue

        if file.is_dir() and list(file.glob("__init__.py")):
            exclude_parents.append(file)
            extensions.append(file)

        elif file.is_file() and file.suffix == ".py":
            extensions.append(file)

    return [str(ext.with_suffix("")).replace("/", ".") for ext in extensions]
