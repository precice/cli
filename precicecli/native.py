import argparse
import subprocess
import pathlib
import sys
import re
from importlib.metadata import version, requires

import preciceconfigcheck.cli


def removeToolsDeprecation(mess: str):
    if mess.startswith("WARNING: precice-tools is deprecated"):
        return "\n".join(mess.splitlines()[2:])

    return mess


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


def getLibraryVersion():
    try:
        ret = subprocess.run("precice-version", capture_output=True, text=True)
        return ret.stdout.strip()
    except:
        try:
            ret = subprocess.run(
                ["precice-tools", "version"], capture_output=True, text=True
            )
            return removeToolsDeprecation(ret.stdout.strip())
        except subprocess.CalledProcessError as e:
            return str(e)
        except FileNotFoundError:
            return "precice-version and precice-tools weren't found. Please install preCICE and add it to your PATH."


def runVersion(_):
    packages = ["precice-cli"] + [
        re.split(r"[\[<=>~]", p)[0].strip() for p in requires("precice-cli")
    ]

    len = max(map(str.__len__, packages))
    fmt = "{:" + str(len) + "}: {}"

    print(fmt.format("libprecice", getLibraryVersion()))
    for package in packages:
        print(fmt.format(package, version(package)))
    return 0


def runDoc(ns):
    try:
        ret = subprocess.run(["precice-config-doc", ns.format])
        return ret.returncode
    except subprocess.CalledProcessError as e:
        return 1
    except FileNotFoundError:
        try:
            ret = subprocess.run(
                ["precice-tools", ns.format], capture_output=True, text=True
            )
            filtered = removeToolsDeprecation(ret.stdout)
            try:
                print(filtered)
            except IOError:
                pass
        except subprocess.CalledProcessError as e:
            return 1
        except FileNotFoundError:
            print(
                "precice-config-doc and precice-tools weren't found. Please install preCICE and add it to your PATH.",
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
    args = [str(path)]
    if ns.participant:
        args.append(ns.participant)
        if ns.size:
            args.append(ns.size)

    try:
        subprocess.run(["precice-config-validate"] + args)
    except subprocess.CalledProcessError as e:
        return e.returncode
    except FileNotFoundError:
        try:
            subprocess.run(["precice-tools", "check"] + args)
        except subprocess.CalledProcessError as e:
            return e.returncode
        except FileNotFoundError:
            print(
                "precice-config-validate and precice-tools weren't found, hence the validation will be skipped. This may lead to crashes in the configuration checker.",
                file=sys.stderr,
            )
            print(
                "Please install preCICE and add it to your PATH for best results.",
                file=sys.stderr,
            )

    # Then check
    return preciceconfigcheck.cli.runCheck(path, ns.debug)
