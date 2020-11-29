#!/usr/bin/env python3

# venv_bootstrap.py
# Copyright (C) 2020  Zack Didcott

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Bootstrap a venv with required packages

TODO
----
Cross-platform support
"""

import logging, os, venv
from argparse import ArgumentParser
from shutil import make_archive
from subprocess import run, PIPE, STDOUT

def create_venv(path, packages=[], pip_opts=[]):
	"""
	Create venv and install specified packages
	
	See https://docs.python.org/3/library/venv.html for more information
	"""
	logging.info("Creating virtual environment...")
	venv.create(path, clear=True, symlinks=False, with_pip=True)
	
	if os.name == 'nt': python = os.path.join(path, "Scripts", "python.exe")
	else: python = os.path.join(path, "bin", "python")
	
	n = 1; err = []
	for pkg in packages:
		logging.info("Installing {0}...{1:>{2}}[{3}/{4}]".format(pkg, ' ', abs(25-len(pkg)), n, len(packages)))
		pip = run([python, "-m", "pip", "install", *pip_opts, pkg], stdout=PIPE, stderr=STDOUT, universal_newlines=True)
		if pip.returncode != 0:
			logging.warning("{0} install failed.".format(pkg))
			logging.debug("Error message:\n===\n{0}===".format(pip.stdout))
			err.append(pkg)
		n += 1
	return err

def parse_requirements(requirements):
	"""Read requirement files and return list of packages"""
	packages = []
	for req in requirements:
		try:
			for line in open(req, 'r').readlines():
				pkg = line.strip()
				if not pkg.startswith("#"):
					packages.append(pkg)
			# Alternatively, let pip handle requirements
			#open(req, 'r').close()
			#PACKAGES.append("-r" + req)
		except OSError:
			logging.warning("{0} not found.".format(req))
	return packages

def archive(path):
	"""Create zip archive of path"""
	logging.info("Compressing...")
	archive = make_archive(path, "zip", path)
	return archive

if __name__ == "__main__":
	parser = ArgumentParser(description="venv_bootstrap - Copyright (C) 2020 Zack Didcott")
	parser.add_argument("directory", type=str, help="path for the virtual environment")
	parser.add_argument("-p", "--packages", type=str, default="", help="space-separated string of packages")
	parser.add_argument("-r", "--requirements", type=str, default="", help="space-separated string of requirements files")
	parser.add_argument("-o", "--pipopts", type=str, default="", help="additional arguments to pass to pip")
	parser.add_argument("-z", "--zip", action="store_true", default=False, help="create zip archive of venv")
	parser.add_argument("-l", "--log", type=str, default=None, help="output log into a file")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-q", "--quiet", action="store_const", const=-1, default=0, dest="verbosity", help="only display warnings")
	group.add_argument("-v", "--verbose", action="store_const", const=1, default=0, dest="verbosity", help="display debugging information")

	args = parser.parse_args()
	
	loglevel = 20 - (args.verbosity * 10)
	logging.basicConfig(
		level=loglevel,
		filename=args.log,
		format="%(asctime)s | [%(levelname)s] %(message)s",
		datefmt="%H:%M:%S"
	)
	
	logging.info(parser.description)
	logging.debug("== Configuration ==")
	for arg, value in sorted(vars(args).items()):
		logging.debug("{0}: {1}".format(arg.title(), value))
	logging.debug("===================")

	DIRECTORY = args.directory
	PACKAGES = args.packages.split()
	REQUIREMENTS = args.requirements.split()
	PIP_OPTS = args.pipopts.split()
	PACKAGES.extend(parse_requirements(REQUIREMENTS))
	
	err = create_venv(DIRECTORY, PACKAGES, PIP_OPTS)
	if args.zip: archive(DIRECTORY)
	if err:
		padding = "\n{0:>13}".format(' ')
		logging.warning("The following packages failed to install:{0}{1}".format(
			padding,
			padding.join(err)
		))
	logging.info("Done! :)")
