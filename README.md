# venv-bootstrap

[![GitHub license](https://img.shields.io/github/license/Zedeldi/venv-bootstrap?style=flat-square)](https://github.com/Zedeldi/venv-bootstrap/blob/master/LICENSE) [![GitHub last commit](https://img.shields.io/github/last-commit/Zedeldi/venv-bootstrap?style=flat-square)](https://github.com/Zedeldi/venv-bootstrap/commits) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

Small Python script to bootstrap a virtual environment, with specified packages.

## Description

venv-bootstrap creates a [virtual environment](https://docs.python.org/3/library/venv.html), and installs the specified packages using [pip](https://pypi.org/project/pip/). Only the [standard library](https://docs.python.org/3/library/index.html) is required; this project was designed to be portable and implemented by other projects to help automate their setup process.

It accepts a space-delimited list of packages and/or requirement files. The [`venv.EnvBuilder.post_setup()`](https://docs.python.org/3/library/venv.html#venv.EnvBuilder.post_setup) method can also be overridden to perform other post-creation steps.

## Installation

1. Clone this repo: `git clone https://github.com/Zedeldi/venv-bootstrap.git`
2. Install build: `pip3 install build`
3. Build: `python3 -m build`
4. Install wheel: `pip3 install dist/venv_bootstrap-*-py3-none-any.whl`
5. Run: `venv-bootstrap -r requirements.txt -p "foo bar baz" .venv`

### Usage

Specify additional options to pip:

`--pipopts "--proxy [user:passwd@]proxy.server:port"`

To create a venv from a different project, use the following:

```python
from venv_bootstrap import create_venv, parse_requirements

create_venv(".venv", parse_requirements(["requirements.txt"]))
```

## Todo

- Cross-platform support

## License

venv-bootstrap is licensed under the GPL v3 for everyone to use, modify and share freely.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

[![GPL v3 Logo](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl-3.0-standalone.html)

## Donate

If you found this project useful, please consider donating. Any amount is greatly appreciated! Thank you :smiley:

My bitcoin address is: [bc1q5aygkqypxuw7cjg062tnh56sd0mxt0zd5md536](bitcoin://bc1q5aygkqypxuw7cjg062tnh56sd0mxt0zd5md536)
