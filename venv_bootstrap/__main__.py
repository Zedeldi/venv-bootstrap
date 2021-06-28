import logging
from argparse import ArgumentParser

from venv_bootstrap import create_venv, parse_requirements, archive


def main():
    parser = ArgumentParser(
        prog="venv-bootstrap",
        description="venv-bootstrap - Copyright (C) 2020 Zack Didcott",
    )
    parser.add_argument(
        "directory", type=str, help="path for the virtual environment"
    )
    parser.add_argument(
        "-p",
        "--packages",
        type=str,
        default="",
        help="space-separated string of packages",
    )
    parser.add_argument(
        "-r",
        "--requirements",
        type=str,
        default="",
        help="space-separated string of requirements files",
    )
    parser.add_argument(
        "-o",
        "--pipopts",
        type=str,
        default="",
        help="additional arguments to pass to pip",
    )
    parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        default=False,
        help="create zip archive of venv",
    )
    parser.add_argument(
        "-l", "--log", type=str, default=None, help="output log into a file"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        const=-1,
        default=0,
        dest="verbosity",
        help="only display warnings",
    )
    group.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=1,
        default=0,
        dest="verbosity",
        help="display debugging information",
    )

    args = parser.parse_args()

    loglevel = 20 - (args.verbosity * 10)
    logging.basicConfig(
        level=loglevel,
        filename=args.log,
        format="%(asctime)s | [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
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
    if args.zip:
        archive(DIRECTORY)
    if err:
        padding = "\n{0:>13}".format(" ")
        logging.warning(
            "The following packages failed to install:{0}{1}".format(
                padding, padding.join(err)
            )
        )
    logging.info("Done! :)")


if __name__ == "__main__":
    main()
