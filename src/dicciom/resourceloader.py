from .util import logger
from .config import loadConfiguration
from openmath.cd import parser
import pathlib

def loadCDs():
    config = loadConfiguration()
    cdRepositoryPath = config["cd_repository"]
    
    allowedStatus = ["official", "private"]
    if not config["skip_experimental"]: allowedStatus.append("experimental")
    if not config["skip_obsolete"]: allowedStatus.append("obsolete")
        
    ocdFiles = pathlib.Path(cdRepositoryPath).rglob("*.ocd")
    cds = []
    for filename in ocdFiles:
        with open(filename) as fh:
            text = fh.read()
            cd = parser.parseXML(text)
            if cd.status in allowedStatus:
                cds.append(cd)
    return sorted(cds, key = lambda cd: (allowedStatus.index(cd.status), cd.name))

def loadCDsGroupedByCDBase():
    allCDs = loadCDs()
    dictByCDBase = {}
    cdsWithoutCDBase = []
    for cd in allCDs:
        if cd.base is None:
            cdsWithoutCDBase.append(cd)
            continue
        if cd.base not in dictByCDBase:
            dictByCDBase[cd.base] = []
        dictByCDBase[cd.base].append(cd)
    
    if len(cdsWithoutCDBase) > 0:
        expermientalWithoutBase = len([cd for cd in cdsWithoutCDBase if cd.status == "experimental"])
        obsoleteWithoutBase = len([cd for cd in cdsWithoutCDBase if cd.status == "obsolete"])
        officialWithoutBase = len([cd for cd in cdsWithoutCDBase if cd.status == "official"])
        privateWithoutBase = len([cd for cd in cdsWithoutCDBase if cd.status == "private"])
        logger.warning(f"CDs without cdbase: {len(cdsWithoutCDBase)}")
        logger.warning(f"  expermiental: {expermientalWithoutBase}")
        logger.warning(f"  obsolete: {obsoleteWithoutBase}")
        logger.warning(f"  official: {officialWithoutBase}")
        logger.warning(f"  private: {privateWithoutBase}")
    
    return dictByCDBase