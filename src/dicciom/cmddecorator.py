from .util import logger
import pathlib
import importlib

thisDirectory = pathlib.Path(__file__).parent
commandDirectory = thisDirectory / "cmd"
commandDataDictionary = {}
commandObjectDictionary = {}

def command(name, *args, **kargs):
    def commandDecorator(clazz):
        commandDataDictionary[name] = (
            clazz,
            args,
            kargs,
        )
        return lambda x: x
    return commandDecorator
        
def importCommands():
    commandModules = [
        str(filename).removeprefix(str(thisDirectory)).removesuffix(".py").replace("/", ".")
        for filename
        in commandDirectory.iterdir()
        if filename.suffix == ".py" and not filename.name.startswith("_")
    ]
    for modulePath in commandModules:
        importlib.import_module(modulePath, "dicciom")

def setupSubparser(subparser):
    
    for commandName, commandData in commandDataDictionary.items():
        (commandClass, args, kargs) = commandData
        commandObjectDictionary[commandName] = commandClass()
        subparser.add_parser(
            commandName,
            *args,
            **kargs
        )