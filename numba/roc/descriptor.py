from numba.core.descriptors import TargetDescriptor
from numba.core.options import TargetOptions
from .target import HSATargetContext, HSATypingContext


class HSATargetOptions(TargetOptions):
    OPTIONS = {}

class HSATarget(TargetDescriptor):
    def __init__(self, name):
        self.options = HSATargetOptions
        self.typingctx = None
        self.targetctx = None
        super().__init__(name)

    @property
    def typing_context(self):
        if self.typingctx is None:
            self.typingctx = HSATypingContext()
        return self.typingctx

    @property
    def target_context(self):
        if self.targetctx is None:
            self.targetctx = HSATargetContext(self.typingctx)
        return self.targetctx

hsa_target = HSATarget('hsa')
