from contextlib import contextmanager
import json
import os
from pathlib import Path
import site
import sys

mypath = "/Users/{name}/Documents/python3_venv"

PYTHON_VERSION = f"python{sys.version_info.major}.{sys.version_info.minor}"
LIB_PATH = {
    "nt": "Lib/site-packages",
    "posix": f"lib/{PYTHON_VERSION}/site-packages",
}
BIN_PATH = {
    "nt": "Scripts",
    "posix": "bin",
}
PYTHON_EXECUTABLE_PATH = {
    "nt": "Scripts/python.exe",
    "posix": "bin/python",
}

def _activate_venv(venv_path: Path) -> None:
    base_path = str(venv_path.resolve())
    venv_dict = {
        "VIRTUAL_ENV": base_path,
        "_OLD_VIRTUAL_PATH": os.environ.pop("PATH", ""),
        "_OLD_SYS_PATH": sys.path,
        "_OLD_PREFIX": sys.prefix,
    }

    try:
        bin_dir = f"{base_path}/{BIN_PATH[os.name]}"
    except KeyError:
        # java/jython
        raise RuntimeError("Jython not supported (yet?)") from None

    # add venv to list
    venvs = json.loads(os.environ.get("IDAVenvs", "[]"))
    venvs.append(venv_dict)
    os.environ["IDAVenvs"] = json.dumps(venvs)

    # save old path
    os.environ["_OLD_VIRTUAL_PATH"] = venv_dict["_OLD_VIRTUAL_PATH"]

    # prepend bin to PATH (this file is inside the bin directory)
    os.environ["PATH"] = os.pathsep.join(
        [bin_dir] + os.environ.get("PATH", "").split(os.pathsep)
    )
    os.environ["VIRTUAL_ENV"] = venv_dict["VIRTUAL_ENV"]

    # add the virtual environments libraries to the host python import mechanism
    prev_length = len(sys.path)

    lib = f"{base_path}/{LIB_PATH[os.name]}"
    path = os.path.realpath(os.path.join(bin_dir, lib))
    site.addsitedir(path)

    sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]
    sys.prefix = sys.exec_prefix = base_path

def activate_venv(venv_path: Path) -> None:
    python_path = venv_path / PYTHON_EXECUTABLE_PATH[os.name]
    if not python_path.is_file():
        raise("Coundn't find python venv file")
    print(f"[IDAVenv] activate_venv {python_path}")
    _activate_venv(venv_path)

def deactivate_venv() -> None:
    print("[IDAVenv] deactivate_venv")
    venv_dicts = json.loads(os.environ.get("IDAVenvs", "[]"))
    if not venv_dicts:
        return

    venv_dict = venv_dicts.pop()
    if not venv_dict:
        return

    # restore old path
    os.environ["PATH"] = os.environ.pop("_OLD_VIRTUAL_PATH", "")
    sys.path = venv_dict["_OLD_SYS_PATH"]
    # restore prefix
    sys.prefix = sys.exec_prefix = venv_dict["_OLD_PREFIX"]
    os.environ["IDAVenvs"] = json.dumps(venv_dicts)

    # TODO! improve this
    to_remove = []
    for name, module in sys.modules.items():
        if not module:
            continue
        try:
            if module.__file__.startswith(venv_dict["VIRTUAL_ENV"]):
                to_remove.append(name)
        except AttributeError:
            pass

    for name in to_remove:
        del sys.modules[name]

@contextmanager
def change_executable(executable: str):
    _executable = sys.executable

    sys.executable = executable
    sys._base_executable = sys.executable
    yield
    sys._base_executable = sys.executable = _executable


def get_context():
    if os.name == "nt":
        executable = Path(sys.base_prefix, "python.exe")
    elif os.name == "posix":
        # On Linux we use system python
        executable = Path(sys.base_prefix, "bin", "python3")
    else:
        # java/jython
        raise RuntimeError("Jython not supported (yet?)")
    return change_executable(str(executable))

@contextmanager
def venv_context(venv_path: Path, dependencies: list[str] | None = None):
    activate_venv(venv_path=venv_path, dependencies=dependencies)
    yield
    deactivate_venv()

activate_venv(Path(mypath))
