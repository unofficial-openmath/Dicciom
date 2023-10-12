import json
import pathlib
from .util import logger

finalConfiguration = None

DEFAULT_CONFIGURATION = {
    "cd_repository": pathlib.Path(__file__).parent.parent / "resources/CDs",
    "config": pathlib.Path.home() / ".local/share/openmath/dicciom.config.json",
    "log_level": 2,
    "skip_obsolete": True,
    "skip_experimental": False,
}

def addConfigurationArguments(argumentParser):
    argumentParser.add_argument(
        "-c",
        "--config"
    )
    argumentParser.add_argument(
        "-r",
        "--cd-repository",
        type=pathlib.Path
    )
    argumentParser.add_argument(
        "--log-level",
        type=int,
        choices=[0,1,2,3]
    )
    argumentParser.add_argument(
        "-s", 
        "--skip-obsolete", 
        help="",
        action="store_true"
    )
    argumentParser.add_argument(
        "-x",
        "--skip-experimental",
        help="",
        action="store_true"
    )


def loadConfiguration(parsedArgs=dict()):
    global finalConfiguration
    if finalConfiguration is None:
        
        configFileConfiguration = _parseConfigFile(parsedArgs)
        
        finalConfiguration = {
            **DEFAULT_CONFIGURATION,
            **configFileConfiguration,
            **parsedArgs
        }

        for k in set(DEFAULT_CONFIGURATION.keys()) & set(parsedArgs.keys()):
            del parsedArgs[k]

        logger.level = finalConfiguration["log_level"]
    
    return finalConfiguration


def _parseConfigFile(parsedArgs):
    configFilePath = parsedArgs.get("config", DEFAULT_CONFIGURATION.get("config"))
    
    if pathlib.Path(configFilePath).exists():
        with open(configFilePath) as fh:
            return json.load(fh)

    if configFilePath is DEFAULT_CONFIGURATION.get("config"):
    
        configFilePath.parent.mkdir(parents=True, exist_ok=True)
        with open(configFilePath, "w") as fh:
            json.dump(DEFAULT_CONFIGURATION, fh, default=str, indent=2)
        return DEFAULT_CONFIGURATION
    
    logger.error("Configuration file not found: "+configFilePath)
    raise FileNotFoundError(configFilePath)
    

