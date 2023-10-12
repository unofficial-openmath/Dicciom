import tabulate
from .base import BaseCommand
from ..config import loadConfiguration
from ..util import ANSI, logger
from ..resourceloader import loadCDsGroupedByCDBase
from ..cmddecorator import command

@command("list", help="List installed Content Dictionaries")
class ListCommand(BaseCommand):

    def prepareArgs(self, argparser):

        argparser.add_argument(
            "--group",
            help="",
            action="store_true",
            required=False
        )
        argparser.add_argument(
            "target",
            help="",
            nargs="*"
        )

    def innerRun(self, group=False, target=None):
        config = loadConfiguration()
        allowedStatus = ["official", "private"]
        if not config["skip_experimental"]: allowedStatus.append("experimental")
        if not config["skip_obsolete"]: allowedStatus.append("obsolete")
        
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

    statusColor = {
        "official": ANSI.GREEN + ANSI.BOLD,
        "private": ANSI.CYAN,
        "experimental": ANSI.MAGENTA,
        "obsolete": ANSI.RED,
    }
