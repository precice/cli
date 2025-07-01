import argparse
import subprocess
import pathlib
import sys

import preciceconfigcheck.cli


def makeCheckParser(_):
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Validates configuration files using the preCICE tooling API.",
    )
    parser.add_argument("infile", type=pathlib.Path)
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug output in the configuration checker.",
    )
    parser.add_argument("participant", nargs="?")
    parser.add_argument("size", nargs="?")
    return parser


def makeDocParser(_):
    parser = argparse.ArgumentParser(
        add_help=False, description="Generates configuration documentation."
    )
    parser.add_argument("format", choices=("xml", "dtd", "md"))
    return parser


def runVersion(_):
    try:
        ret = subprocess.run("precice-version")
        return ret.returncode
    except subprocess.CalledProcessError as e:
        return 1
    except FileNotFoundError:
        print(
            "precice-version wasn't found. Please install preCICE and add it to your PATH.",
            file=sys.stderr,
            flush=True,
        )
        return 1


def runDoc(ns):
    try:
        ret = subprocess.run(["precice-config-doc", ns.format])
        return ret.returncode
    except subprocess.CalledProcessError as e:
        return 1
    except FileNotFoundError:
        print(
            "precice-config-doc wasn't found. Please install preCICE and add it to your PATH.",
            file=sys.stderr,
            flush=True,
        )
        return 1
    return 0


def runCheck(ns):
    path = ns.infile
    if not path.is_file():
        print(f"The given file {path} doesn't exist.", file=sys.stderr, flush=True)
        return 1

    # First validate
    args = ["precice-config-validate", str(path)]
    if ns.participant:
        args.append(ns.participant)
        if ns.size:
            args.append(ns.size)

    try:
        subprocess.run(args)
    except subprocess.CalledProcessError as e:
        return e.returncode
    except FileNotFoundError:
        print(
            "precice-config-validate wasn't found, hence the validation will be skipped. This may lead to crashes in the configuration checker.",
            file=sys.stderr,
        )
        print(
            "Please install preCICE and add it to your PATH for best results.",
            file=sys.stderr,
        )

    # Then check
    return preciceconfigcheck.cli.runCheck(path, ns.debug)
