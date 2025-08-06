import argparse
import sys

from preciceconfigvisualizer.cli import makeVisualizeParser, runVisualize
from preciceconfigformat.cli import makeFormatParser, runFormat

from preciceprofiling.analyze import runAnalyze, makeAnalyzeParser
from preciceprofiling.export import runExport, makeExportParser
from preciceprofiling.histogram import runHistogram, makeHistogramParser
from preciceprofiling.trace import runTrace, makeTraceParser
from preciceprofiling.merge import runMerge, makeMergeParser

from precicecli.native import (
    runCheck,
    runDoc,
    runVersion,
    makeDocParser,
    makeCheckParser,
)

from precicecasegenerate.cli import runGenerate, makeGenerateParser


def add_subparser(subparser, name, parserFactory):
    parser = parserFactory(False)
    subparser.add_parser(
        name,
        help=parser.description,
        description=parser.description,
        parents=[parser],
    )


def runProfiling(ns):
    return {
        "analyze": runAnalyze,
        "trace": runTrace,
        "export": runExport,
        "histogram": runHistogram,
        "merge": runMerge,
    }[ns.subcmd](ns)


def runConfig(ns):
    return {
        "visualize": runVisualize,
        "format": runFormat,
        "doc": runDoc,
        "check": runCheck,
    }[ns.subcmd](ns)


def makeParser():
    parser = argparse.ArgumentParser(description="Unified preCICE commandline tools")
    subparsers = parser.add_subparsers(
        title="commands",
        dest="cmd",
    )

    version_help = "Show version of preCICE"
    subparsers.add_parser("version", help=version_help, description=version_help)

    add_subparser(subparsers, "init", makeGenerateParser)

    profiling_help = "Tools for processing preCICE profiling files"
    profiling_root = subparsers.add_parser(
        "profiling", help=profiling_help, description=profiling_help
    )
    profiling = profiling_root.add_subparsers(
        title="profiling commands",
        dest="subcmd",
    )

    add_subparser(profiling, "analyze", makeAnalyzeParser)
    add_subparser(profiling, "trace", makeTraceParser)
    add_subparser(profiling, "export", makeExportParser)
    add_subparser(profiling, "histogram", makeHistogramParser)
    add_subparser(profiling, "merge", makeMergeParser)

    config_help = "Tools for processing preCICE configuration files"
    config_root = subparsers.add_parser(
        "config", help=config_help, description=config_help
    )
    config = config_root.add_subparsers(
        title="configuration commands",
        dest="subcmd",
    )

    add_subparser(config, "format", makeFormatParser)
    add_subparser(config, "visualize", makeVisualizeParser)
    add_subparser(config, "check", makeCheckParser)
    add_subparser(config, "doc", makeDocParser)

    def checker(args):
        def printParserHelp(p):
            p.print_help()
            return 1

        if args.cmd is None:
            return printParserHelp(parser)
        if args.cmd == "profiling" and args.subcmd is None:
            return printParserHelp(profiling_root)
        if args.cmd == "config" and args.subcmd is None:
            return printParserHelp(config_root)
        return 0

    return parser, checker


def run(ns):
    return {
        "version": runVersion,
        "profiling": runProfiling,
        "config": runConfig,
        "init": runGenerate,
    }[ns.cmd](ns)


def main():
    parser, checker = makeParser()
    ns = parser.parse_args()
    if rc := checker(ns):
        return rc
    return run(ns)
