#!/usr/bin/env python

from intmaniac import maniac_file
from intmaniac import tools
from intmaniac import output

import sys
from os import getcwd, unlink
from os.path import join, realpath, isfile
from argparse import ArgumentParser

logger = None


##############################################################################
#                                                                            #
# run test sets logic                                                        #
#                                                                            #
##############################################################################


def _run_tests(tests):
    re_raise_me = None
    try:
        retval = True
        for test in tests:
            output.output.block_open("Test " + test.name)
            test.run()
            retval = test.succeeded() and retval
            test.dump()
            output.output.block_done()
    except Exception as e:
        # this is just to make sure we really kill those darn temp files.
        re_raise_me = e
    finally:
        for test in tests:
            try:
                unlink(test.template)
            finally:
                pass
    if re_raise_me:
        raise re_raise_me
    return retval


##############################################################################
#                                                                            #
# startup initialization                                                     #
#                                                                            #
##############################################################################


def _parse_args(arguments):
    """
    Parses the arguments list given as parameter using argparse. Post-processes
    the configuration data (e.g. converting the string vars containing the
    KEY=VAL values for environment settings to a dict {k:v,...}).
    :param arguments: The argument list to parse
    :return: The config data object
    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config-file",
                        help="specify configuration file. "
                             "Default: ./intmaniac.yml",
                        default=realpath(join(getcwd(), "intmaniac.yaml")))
    parser.add_argument("-e", "--env",
                        help="dynamically add a value to the environment",
                        action="append",
                        default=[])
    parser.add_argument("-v", "--verbose",
                        help="increase verbosity level, use multiple times",
                        action="count",
                        default=0)
    parser.add_argument("-f", "--force",
                        help="Ignore warnings",
                        action="store_true",
                        default=False)
    config = parser.parse_args(arguments)
    # process arguments
    config.config_file = realpath(config.config_file)
    config.env = dict([e.split("=", 1) for e in config.env])
    # check arguments
    if not isfile(config.config_file):
        tools.fail("Could not find config file: {}".format(config.config_file))
    return config


def _init_logging(config):
    global logger
    tools.init_logging(config)
    logger = tools.get_logger(__name__)


def _internal_entrypoint(args):
    config = _parse_args(args)
    _init_logging(config)
    tests = maniac_file.parse(config)
    result = _run_tests(tests)
    if not result:
        sys.exit(1)


# this is for the console invocation by setuptools.
def console_entrypoint():
    _internal_entrypoint(sys.argv[1:])
