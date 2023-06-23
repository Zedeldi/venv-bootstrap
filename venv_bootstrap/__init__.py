"""Bootstrap a virtual environment with specified packages."""

import logging
import os
import venv
from shutil import make_archive
from subprocess import PIPE, STDOUT, run


def create_venv(
    path: str, packages: list[str] = [], pip_opts: list[str] = []
) -> list[str]:
    """
    Create venv and install specified packages.

    See https://docs.python.org/3/library/venv.html for more information
    """
    logging.info("Creating virtual environment...")
    venv.create(path, clear=True, symlinks=False, with_pip=True)

    if os.name == "nt":
        python = os.path.join(path, "Scripts", "python.exe")
    else:
        python = os.path.join(path, "bin", "python")

    n = 1
    err = []
    for pkg in packages:
        logging.info(
            "Installing {0}...{1:>{2}}[{3}/{4}]".format(
                pkg, " ", abs(25 - len(pkg)), n, len(packages)
            )
        )
        pip = run(
            [python, "-m", "pip", "install", *pip_opts, pkg],
            stdout=PIPE,
            stderr=STDOUT,
            universal_newlines=True,
        )
        if pip.returncode != 0:
            logging.warning("{0} install failed.".format(pkg))
            logging.debug("Error message:\n===\n{0}===".format(pip.stdout))
            err.append(pkg)
        n += 1
    return err


def parse_requirements(requirements: list[str]) -> list[str]:
    """Read requirement files and return list of packages."""
    packages = []
    for req in requirements:
        try:
            for line in open(req, "r").readlines():
                pkg = line.strip()
                if pkg and not pkg.startswith("#"):
                    packages.append(pkg)
            # Alternatively, let pip handle requirements
            # open(req, 'r').close()
            # PACKAGES.append("-r" + req)
        except OSError:
            logging.warning("{0} not found.".format(req))
    return packages


def archive(path: str) -> str:
    """Create zip archive of path."""
    logging.info("Compressing...")
    archive = make_archive(path, "zip", path)
    return archive
