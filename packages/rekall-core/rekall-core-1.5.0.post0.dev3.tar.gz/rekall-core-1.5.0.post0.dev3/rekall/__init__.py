import rekall.compatibility
from pkg_resources import resource_filename

def get_resource(name):
    """Use the pkg_resources API to extract resources.

    This will extract into a temporary file in case the egg is compressed.
    """
    return resource_filename("rekall.resources", name)

from ._version import get_versions
__version__ = get_versions()['version']
