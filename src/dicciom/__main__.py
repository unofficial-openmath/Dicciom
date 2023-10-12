import sys
from .util import logger
from .config import loadConfiguration, addConfigurationArguments
from .cmddecorator import setupSubparser, commandDataDictionary, commandObjectDictionary, importCommands
from argparse import ArgumentParser

argumentParser = ArgumentParser("dicciom")
addConfigurationArguments(argumentParser)

commandArgumentSubparser = argumentParser.add_subparsers( )
commandArgumentSubparser.dest = "command"
commandArgumentSubparser.metavar = "command"
commandArgumentSubparser.required = True

importCommands()
setupSubparser(commandArgumentSubparser)

argumentsParsed = {
    k:v
    for k,v
    in vars(argumentParser.parse_args()).items()
    if v
}
configuration = loadConfiguration(argumentsParsed)

commandObjectDictionary[argumentsParsed["command"]].run(**argumentsParsed)

