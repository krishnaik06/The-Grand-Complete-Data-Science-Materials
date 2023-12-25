"""Client-side implementations of the Jupyter protocol"""
from ._version import __version__  # noqa
from ._version import protocol_version  # noqa
from ._version import protocol_version_info  # noqa
from ._version import version_info  # noqa

try:
    from .asynchronous import AsyncKernelClient  # noqa
    from .blocking import BlockingKernelClient
    from .client import KernelClient
    from .connect import *  # noqa
    from .launcher import *  # noqa
    from .manager import AsyncKernelManager
    from .manager import KernelManager
    from .manager import run_kernel
    from .multikernelmanager import AsyncMultiKernelManager
    from .multikernelmanager import MultiKernelManager
    from .provisioning import KernelProvisionerBase
    from .provisioning import LocalProvisioner
except ModuleNotFoundError:
    import warnings

    warnings.warn("Could not import submodules")
