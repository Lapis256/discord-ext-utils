from pathlib import Path


__all__ = ("get_extensions", )


def get_extensions(directory, recursive=True):
    path = Path(directory)
    exclude_parent = None
    exts = []
    
    for file in path.rglob("*"):
        _parent = file.parent
        if file.name != "__init__.py":
            if file.name.startswith("_"):
                if file.is_dir():
                    exclude_parent = file
                continue

            if exclude_parent and _parent.is_relative_to(exclude_parent):
                    continue
        
        if file.name == "__init__.py":
            exclude_parent = _parent
            exts.append(_parent)

        elif file.is_file() and file.suffix == ".py":
            exts.append(file)

    return [str(ext.with_suffix("")).replace("/", ".") for ext in exts]
