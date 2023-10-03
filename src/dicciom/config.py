import pathlib
from .util import logger

finalConfiguration = None

DEFAULT_CONFIGURATION = {
    "cd_repository": pathlib.Path(__file__).parent.parent / "resources/CDs",
    "log_level": 2
}

def addConfigurationArguments(argumentParser):
    argumentParser.add_argument("--cd-repository")
    argumentParser.add_argument("--log-level", type=int)


def loadConfiguration(parsedArgs=dict()):
    global finalConfiguration
    if finalConfiguration is None:
        
        finalConfiguration = {
            **DEFAULT_CONFIGURATION,
            **parsedArgs
        }

        for k in set(DEFAULT_CONFIGURATION.keys()) & set(parsedArgs.keys()):
            del parsedArgs[k]

        logger.level = finalConfiguration["log_level"]
    
    return finalConfiguration