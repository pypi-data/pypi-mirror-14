
from vlcp.server.module import Module, api, depend
from vlcp.config import defaultconfig
from vlcp.event import Event, withIndices
from vlcp.event.runnable import RoutineContainer
from . import testmodule1

@withIndices()
class ModuleTestEvent2(Event):
    pass

@defaultconfig
@depend(testmodule1.TestModule1)
class TestModule2(Module):
    class MyHandler(RoutineContainer):
        def main(self):
            matcher = testmodule1.ModuleTestEvent.createMatcher()
            while True:
                yield (matcher,)
                self.subroutine(self.waitForSend(ModuleTestEvent2(result=self.event.a + self.event.b, version = 'version3')), False)
    def __init__(self, server):
        Module.__init__(self, server)
        self.routines.append(self.MyHandler(self.scheduler))
