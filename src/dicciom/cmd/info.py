from .base import BaseCommand
from ..util import ANSI
from ..resourceloader import loadCDs

class InfoCommand(BaseCommand):

    statusColor = {
        "official": ANSI.GREEN + ANSI.BOLD,
        "private": ANSI.CYAN,
        "experimental": ANSI.MAGENTA,
        "obsolete": ANSI.RED,
    }

    def prettyPrintCDs(self, base, cdGroupedByBase):
        outputTable = [
            f"\n{self.statusColor[status]}{name}{ANSI.RESET} ({status})\n   {desc}"
            for (name, status, desc)
            in cdGroupedByBase
        ]
        print(ANSI.BOLD,base ,ANSI.NOT_BOLD, sep="")
        print("\n".join(outputTable))

    def help(self):
        return "Show detailed information about a Content Dictionary or a symbol"

    def innerRun(self, name):
        cds = loadCDs()
        groupedCDs = {}
        for cd in cds:
            if cd.base not in groupedCDs:
                groupedCDs[cd.base] = []
            groupedCDs[cd.base].append((
                cd.name, cd.status, cd.description
            ))
        
        for base in groupedCDs:
            self.prettyPrintCDs(base, sorted(groupedCDs[base]))


    def prepareArgs(self, argparser):
        pass