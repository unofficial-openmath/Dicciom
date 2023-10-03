import tabulate
from .base import BaseCommand
from ..util import ANSI, logger
from ..resourceloader import loadCDsGroupedByCDBase

class ListCommand(BaseCommand):

    statusColor = {
        "official": ANSI.GREEN + ANSI.BOLD,
        "private": ANSI.CYAN,
        "experimental": ANSI.MAGENTA,
        "obsolete": ANSI.RED,
    }

    def prettyPrintCDs(self, base, cdGroupedByBase):
        outputTable = [
            [
                self.statusColor[status]+name+ANSI.RESET,
                status,
                version
            ]
            for (name, status, version)
            in cdGroupedByBase
        ]
        print(ANSI.BOLD,base ,ANSI.NOT_BOLD, sep="")
        print(tabulate.tabulate(
            outputTable, 
            headers=["name", "status", "version"],
            tablefmt="simple",
            colalign=("right","left","center")
        ))

    def innerRun(self, skip_obsolete=False, skip_experimental=False):
        allowedStatus = ["official", "private"]
        if not skip_experimental: allowedStatus.append("experimental")
        if not skip_obsolete: allowedStatus.append("obsolete")
        
        groupedCDs = loadCDsGroupedByCDBase()
        groupedCDsListData = {
            base: [
                (cd.name, cd.status, cd.version)
                for cd
                in cds
            ]
            for base, cds
            in groupedCDs.items()
        }
        for i, base in enumerate(groupedCDsListData):
            cdsToBeListed = [cd for cd in groupedCDsListData[base] if cd[1] in allowedStatus]
            sortedCDs = sorted(cdsToBeListed, key = lambda x: allowedStatus.index(x[1]))
            self.prettyPrintCDs(base, sortedCDs)
            if i < len(groupedCDsListData): print("")

    def help(self):
        return "List installed Content Dictionaries"

    def prepareArgs(self, argparser):
        argparser.add_argument("-s", "--skip-obsolete", action="store_true")
        argparser.add_argument("-x", "--skip-experimental", action="store_true")