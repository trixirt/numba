from numba.core.descriptors import TargetDescriptor
from numba.core.options import TargetOptions
from .target import HSATargetContext, HSATypingContext


class HSATargetOptions(TargetOptions):
    OPTIONS = {}

class HSATarget(TargetDescriptor):
    options = HSATargetOptions
    typingctx = HSATypingContext()
    targetctx = HSATargetContext(typingctx)
    super().__init__('hsa')


