
from vlcp.server.module import Module, api
from vlcp.config import defaultconfig
from vlcp.event import Event, withIndices
from vlcp.event.runnable import RoutineContainer

@withIndices()
class ModuleTestEvent(Event):
    pass

@defaultconfig
class TestModule1(Module):
    class MyHandler(RoutineContainer):
        def method2(self, a, b):
            self.retvalue = a + b
            if False:
                yield
        def method3(self, a, b):
            for m in self.waitForSend(ModuleTestEvent(a = a, b = b)):
                yield m
            self.retvalue = None
    def __init__(self, server):
        Module.__init__(self, server)
        self.handlerRoutine = self.MyHandler(self.scheduler)
        self.createAPI(api(self.method1),
                api(self.handlerRoutine.method2,self.handlerRoutine),
                api(self.handlerRoutine.method3,self.handlerRoutine),
                api(self.method4)
                )
    def method1(self):
        return 'version3'
    def method4(self):
        raise ValueError('test')
