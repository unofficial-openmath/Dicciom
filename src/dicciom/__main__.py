import sys
from . import *
from .util import logger
from .config import loadConfiguration, addConfigurationArguments
from argparse import ArgumentParser


commandDictionary = {
    "list": ListCommand(),
    "info": InfoCommand(),
}

argumentParser = ArgumentParser("dicciom")
addConfigurationArguments(argumentParser)

commandArgumentSubparser = argumentParser.add_subparsers( )
commandArgumentSubparser.dest = "command"
commandArgumentSubparser.metavar = "command"
commandArgumentSubparser.required = True

for commandName, commandObject in commandDictionary.items():
    commandObject.prepareArgs(
        commandArgumentSubparser.add_parser(
            commandName,
            help=commandObject.help()
        )
    )

argumentsParsed = {
    k:v
    for k,v
    in vars(argumentParser.parse_args()).items()
    if v is not None
}
configuration = loadConfiguration(argumentsParsed)

commandDictionary[argumentsParsed["command"]].run(**argumentsParsed)

