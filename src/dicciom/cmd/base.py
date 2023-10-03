from ..util import logger

class BaseCommand():
    def run(self, **kargs):
        try:
            del kargs["command"]
            self.innerRun(**kargs)
        except Exception as e:
            logger.error(e)
            raise e

    def innerRun(self, **kargs):
        raise NotImplementedError(__class__)

    def desc(self):
        raise NotImplementedError(__class__)

    def help(self):
        raise NotImplementedError(__class__)

    def prepareArgs(self, _):
        raise NotImplementedError(__class__)