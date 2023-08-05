import sys
import inspect

from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec
from os import path
from types import ModuleType

from cffi import FFI


def get_declaration(func):
    name = func.__name__
    sig = inspect.signature(func)
    params = [p.annotation for p in sig.parameters.values()]
    return '{} {}({});'.format(sig.return_annotation, name, ', '.join(params))


class DllModule(ModuleType):
    def __init__(self, name, ffi, lib):
        super(DllModule, self).__init__(name)
        self._lib = lib
        self._ffi = ffi

    def declare(self, signature):
        self._ffi.cdef(signature)

    def extern(self, decl):
        self.declare(get_declaration(decl))
        return getattr(self, decl.__name__)

    def __getattr__(self, attr):
        return getattr(self._lib, attr)


class DllFinder(MetaPathFinder):
    def find_spec(self, name, m_path, target=None):
        if not name.startswith('_'): return
        if m_path is not None:
            name = path.join(m_path[0], name)
        source = name[1:] + '.dll'
        if path.exists(source):
            return ModuleSpec(name, DllLoader(source))

    def register(self):
        sys.meta_path.append(self)

    def revoke(self):
        sys.meta_path = [finder for finder in sys.meta_path if finder is not self]

    def __enter__(self):
        self.register()

    def __exit__(self, *_):
        self.revoke()


class DllLoader(Loader):
    def __init__(self, file_path):
        ffi = FFI()
        self.ffi = ffi
        self.lib = ffi.dlopen(file_path)
    
    def create_module(self, spec):
        return DllModule(spec.name, self.ffi, self.lib)

    def exec_module(self, module):
        return module


ABI = DllFinder()