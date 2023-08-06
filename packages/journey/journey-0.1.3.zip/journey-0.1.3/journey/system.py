import inspect
from .annotations import (consumer, provider)


def sort_by_providers(procs):
    sigs = {proc: inspect.signature(proc) for proc in procs}
    sorted_procs = [p for (p, sig) in sigs.items() if consumer not in [prm.annotation for prm in sig.parameters.values()]]
    provided_data = {prm.name for proc in sorted_procs for prm in sigs[proc].parameters.values()}
    procs = procs.difference(sorted_procs)
    while procs:
        any_added = False
        for proc in list(procs):
            proc_provided = {prm.name for prm in sigs[proc].parameters.values() if prm.annotation == consumer}
            if not proc_provided.difference(provided_data):
                procs.remove(proc)
                provided_data.update({prm.name for prm in sigs[proc].parameters.values() if prm.annotation == provider})
                sorted_procs.append(proc)
                any_added = True
        if not any_added:
            raise KeyError('Some required data types are not provided in time')
    return sorted_procs


def provide(proc, data_types):
    return proc(**{
        param.name: data_types[param.name] 
        for param in inspect.signature(proc).parameters.values()
    })


class System:
    DATA_TYPES = {}
    PLUGINS = set()

    def __init__(self, source):
        self.source = source
        self.data = self.__class__.DATA_TYPES.copy()

    @classmethod
    def register(cls, dt):
        cls.DATA_TYPES[dt.__name__] = dt

    def iter_source(self):
        for item in self.source:
            yield item

    def run(self):
        procs = self.PLUGINS
        consumers = [provide(proc, self.data) for proc in sort_by_providers({f for f in procs if inspect.isgeneratorfunction(f)})]
        oracles = sort_by_providers(procs.difference(consumers))
        for cons in consumers: cons.send(None)
        for item in self.iter_source():
            for cons in list(consumers):
                try: cons.send(item)
                except StopIteration: consumers.remove(cons)
        for cons in consumers: cons.close()
        for oracle in oracles:
            provide(oracle, self.data)
        return self.data