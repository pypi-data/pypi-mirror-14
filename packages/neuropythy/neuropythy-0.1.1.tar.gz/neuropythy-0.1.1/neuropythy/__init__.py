# __init__.py

'''Tools for analyzing and registering cortical meshes.'''

from cortex import cortex_to_mrvolume
from freesurfer import freesurfer_subject
from registration import mesh_register, register_retinotopy

# Version information...
_version_major = 0
_version_minor = 1
_version_micro = 0
__version__ = "%s.%s.%s" % (_version_major, _version_minor, _version_micro)

description = 'Integrate Python environment with FreeSurfer and perform mesh registration'
    
