import argparse
import subprocess

def makeCheckParser(_):
    parser = argparse.ArgumentParser(add_help=False, description="Validates configuration files using the preCICE tooling API.")
    parser.add_argument("infile")
    parser.add_argument("participant", nargs="?")
    parser.add_argument("size", nargs="?")
    return parser


def makeDocParser(_):
    parser = argparse.ArgumentParser(add_help=False, description="Generates configuration documentation.")
    parser.add_argument("format", choices=("xml", "dtd", "md"))
    return parser


def runVersion(_):
    try:
        ret = subprocess.run("precice-version")
        return ret.returncode
    except subprocess.CalledProcessError as e:
        return 1
    except FileNotFoundError:
        print("precice-version wasn't found. Please install preCICE and add it to your PATH.", file=sys.stderr, flush=True)
        return 1

def runDoc(ns):
    try:
        ret = subprocess.run(["precice-config-doc", ns.format])
        return ret.returncode
    except subprocess.CalledProcessError as e:
        return 1
    except FileNotFoundError:
        print("precice-config-doc wasn't found. Please install preCICE and add it to your PATH.", file=sys.stderr, flush=True)
        return 1
    return 0


def runCheck(ns):
    # Frist validate
    args = ["precice-config-validate", ns.infile]
    if ns.participant:
        args.append(ns.participant)
        if ns.size:
            args.append(ns.size)

    try:
        ret = subprocess.run(args)
        return 1
    except subprocess.CalledProcessError as e:
        return e.returncode
    except FileNotFoundError:
        print("precice-config-doc wasn't found. Please install preCICE and add it to your PATH.", file=sys.stderr, flush=True)
        return 1

    # Then check
    # TODO
    return 0
