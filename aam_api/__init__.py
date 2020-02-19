import os

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("requests", "pandas", "xlrd")
missing_dependencies = []


for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

from aam_api.core.client import Client
from aam_api.core.derivedSignals import DerivedSignals
from aam_api.core.destinations import Destinations
from aam_api.core.segmentFolders import SegmentFolders
from aam_api.core.segments import Segments
from aam_api.core.traitFolders import TraitFolders
from aam_api.core.traits import Traits
from aam_api.core.users import Users
from aam_api.extras.search import search
from aam_api.helpers.apiError import APIError
from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.bytesToJson import bytesToJson
from aam_api.helpers.flattenJson import flattenJson
from aam_api.helpers.toDataFrame import toDataFrame
from aam_api.helpers.destinationSegments import segmentsMappedToDestination
from aam_api.helpers.segmentTraits import segmentTraits
from aam_api.helpers.traitSkeleton import traitSkeleton
from aam_api.helpers.inSegments import inSegments
from aam_api.helpers.inSegments import inSegmentsBool
