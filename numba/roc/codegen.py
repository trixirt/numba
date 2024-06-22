from llvmlite import binding as ll
from llvmlite import ir
from numba.core import utils
from numba.core.codegen import Codegen, CodeLibrary
from .hlc import DATALAYOUT, TRIPLE, hlc


class HSACodeLibrary(CodeLibrary):
    def __init__(self, codegen, name):
        super().__init__(codegen, name)
        # The llvmlite module for this library.
        self._module = None

    def _optimize_functions(self, ll_module):
        pass

    def _optimize_final_module(self):
        pass

    def _finalize_specific(self):
        pass

    def add_ir_module(self, mod):
        self._module = mod
        pass

    def add_linking_library(self, library):
        pass

    def finalize(self):
        pass

    def get_asm_str(self):
        """
        Get the human-readable assembly.
        """
        m = hlc.Module()
        m.load_llvm(str(self._final_module))
        out = m.finalize()
        return str(out.hsail)

    def get_function(self, name):
        for fn in self._module.functions:
            if fn.name == name:
                return fn

    def get_llvm_str(self):
        return "\nTBD\n"


class JITHSACodegen(Codegen):
    _library_class = HSACodeLibrary

    def _init(self):
        self._data_layout = DATALAYOUT[utils.MACHINE_BITS]
        self._target_data = ll.create_target_data(self._data_layout)

    def _create_empty_module(self, name):
        ir_module = ir.Module(name)
        ir_module.triple = TRIPLE
        return ir_module

    def _module_pass_manager(self):
        raise NotImplementedError

    def _function_pass_manager(self, llvm_module):
        raise NotImplementedError

    def _add_module(self, module):
        pass
