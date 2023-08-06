####################################################################################################
# registration.py
# Tools for registering the cortical surface to a particular potential function
# By Noah C. Benson

import numpy as np
import scipy as sp
import os, sys
from math import pi
from numbers import Number
from neuropythy.cortex import CorticalMesh
from neuropythy.freesurfer import freesurfer_subject
from neuropythy.topology import Registration
from pysistence import make_dict
from array import array

from py4j.java_gateway import (launch_gateway, JavaGateway, GatewayParameters)

# Java start:
_java_port = None
_java = None
def init_registration():
    global _java, _java_port
    if _java is not None: return
    _java_port = launch_gateway(
        classpath=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
            'lib', 'nben', 'target', 'nben-standalone.jar'),
        javaopts=['-Xmx2g'],
        die_on_exit=True)
    _java = JavaGateway(gateway_parameters=GatewayParameters(port=_java_port))

# These are dictionaries of all the details we have about each of the possible arguments to the
# mesh_register's field argument:
_parse_field_data_types = {
    'mesh': ['newStandardMeshPotential', ['edge_scale', 1.0], ['angle_scale', 1.0], 'F', 'X'],
    'edge': {
        'harmonic':      ['newHarmonicEdgePotential',   ['scale', 1.0], ['order', 2.0], 'F', 'X'],
        'lennard-jones': ['newLJEdgePotential',         ['scale', 1.0], ['order', 2.0], 'F', 'X']},
    'angle': {
        'harmonic':      ['newHarmonicAnglePotential',  ['scale', 1.0], ['order', 2.0], 'F', 'X'],
        'lennard-hones': ['newLJAnglePotential',        ['scale', 1.0], ['order', 2.0], 'F', 'X'],
        'infinite-well': ['newWellAnglePotential',      ['scale', 1.0], ['order', 2.0], 
                                                        ['min',   0.0], ['max',   pi],  'F', 'X']},
    'anchor': {
        'harmonic':      ['newHarmonicAnchorPotential', ['scale', 1.0], ['shape', 2.0], 0, 1, 'X'],
        'gaussian':      ['newGaussianAnchorPotential', ['scale', 1.0], ['shape', 2.0], 
                                                        ['sigma', 1.0], 0, 1, 'X']},
    'perimeter': {
        'harmonic':   ['newHarmonicPerimeterPotential', ['scale', 1.0], ['shape', 2.0], 'F', 'X']}};

def serialize_numpy(m, t):
    '''
    serialize_numpy(m, type) converts the numpy array m into a byte stream that can be read by the
    nben.util.Py4j Java class. The function assumes that the type of the array needn't be encoded
    in the bytearray itself. The bytearray will begin with an integer, the number of dimensions,
    followed by that number of integers (the dimension sizes themselves) then the bytes of the
    array, flattened.
    The argument type gives the type of the array to be transferred and must be 'i' for integer or
    'd' for double (or any other string accepted by array.array()).
    '''
    # Start with the header: <number of dimensions> <dim1-size> <dim2-size> ...
    header = array('i', [len(m.shape)] + list(m.shape))
    # Now, we can do the array itself, just flattened
    body = array(t, m.flatten().tolist())
    # Wrap bytes if necessary...
    if sys.byteorder != 'big':
        header.byteswap()
        body.byteswap()
    # And return the result:
    return bytearray(header.tostring() + body.tostring())

def to_java_doubles(m):
    '''
    to_java_doubles(m) yields a java array object for the vector or matrix m.
    '''
    global _java
    if _java is None: init_registration()
    m = np.asarray(m)
    dims = len(m.shape)
    if dims > 2: raise ValueError('1D and 2D arrays supported only')
    bindat = serialize_numpy(m, 'd')
    return (_java.jvm.nben.util.Numpy.double2FromBytes(bindat) if dims == 2
            else _java.jvm.nben.util.Numpy.double1FromBytes(bindat))
def to_java_ints(m):
    '''
    to_java_ints(m) yields a java array object for the vector or matrix m.
    '''
    global _java
    if _java is None: init_registration()
    m = np.asarray(m)
    dims = len(m.shape)
    if dims > 2: raise ValueError('1D and 2D arrays supported only')
    bindat = serialize_numpy(m, 'i')
    return (_java.jvm.nben.util.Numpy.int2FromBytes(bindat) if dims == 2
            else _java.jvm.nben.util.Numpy.int1FromBytes(bindat))
def to_java_array(m):
    '''
    to_java_array(m) yields to_java_ints(m) if m is an array of integers and to_java_doubles(m) if
    m is anything else. The numpy array m is tested via numpy.issubdtype(m.dtype, numpy.int64).
    '''
    m = np.asarray(m)
    return to_java_ints(m) if np.issubdtype(m.dtype, np.int64) else to_java_doubles(m)
        
def _parse_field_function_argument(argdat, args, faces, coords):
    # first, see if this is an easy one...
    if argdat == 'F':
        return faces
    elif argdat == 'X':
        return coords
    elif isinstance(argdat, (int, long)):
        return to_java_array(args[argdat])
    # okay, none of those; must be a list with a default arg
    argname = argdat[0]
    argdflt = argdat[1]
    # see if we can find such an arg...
    for i in range(len(args)):
        if isinstance(args[i], basestring) and args[i].lower() == argname.lower():
            return args[i+1] if isinstance(args[i+1], Number) else to_java_array(args[i+1])
    # did not find the arg; use the default:
    return argdflt

def _parse_field_argument(instruct, faces, coords):
    global _java
    if _java is None: init_registration()
    if isinstance(instruct, basestring):
        insttype = instruct
        instargs = []
    elif type(instruct) in [list, tuple]:
        insttype = instruct[0]
        instargs = instruct[1:]
    else:
        raise RuntimeError('potential field instruction must be list/tuple or string')
    # look this type up in the types data:
    insttype = insttype.lower()
    if insttype not in _parse_field_data_types:
        raise RuntimeError('Unrecognized field data type: ' + insttype)
    instdata = _parse_field_data_types[insttype]
    # if the data is a dictionary, we must parse on the next arg
    if isinstance(instdata, dict):
        shape_name = instargs[0].lower()
        instargs = instargs[1:]
        if shape_name not in instdata:
            raise RuntimeError('Shape ' + shape_name + ' not supported for type ' + insttype)
        instdata = instdata[shape_name]
    # okay, we have a list of instructions... find the java method we are going to call...
    java_method = getattr(_java.jvm.nben.mesh.registration.Fields, instdata[0])
    # and parse the arguments into a list...
    java_args = [_parse_field_function_argument(a, instargs, faces, coords) for a in instdata[1:]]
    # and call the function...
    return java_method(*java_args)

# parse a field potential argument and return a java object that represents it
def _parse_field_arguments(arg, faces, coords):
    '''See mesh_register.'''
    if not isinstance(arg, list):
        raise RuntimeError('field argument must be a list of instructions')
    pot = [_parse_field_argument(instruct, faces, coords) for instruct in arg]
    # make a new Potential sum unless the length is 1
    if len(pot) <= 1:
        return pot[0]
    else:
        sp = _java.jvm.nben.mesh.registration.Fields.newSum()
        for field in pot: sp.addField(field)
        return sp

# The mesh_register function
def mesh_register(mesh, field, max_steps=25000, max_step_size=0.1, max_pe_change=1):
    '''
    mesh_register(mesh, field) yields the mesh that results from registering the given mesh by
    minimizing the given potential field description over the position of the vertices in the
    mesh. The mesh argument must be a CorticalMesh (see neuropythy.cortex) such as can be read
    from FreeSurfer using the neuropythy.freesurfer.Subject class. The field argument must be
    a list of field names and arguments; with the exception of 'mesh' (or 'standard'), the 
    arguments must be a list, the first element of which is the field type name, the second
    element of which is the field shape name, and the final element of which is a dictionary of
    arguments accepted by the field shape.

    The following are valid field type names:
      * 'mesh' : the standard mesh potential, which includes an edge potential, an angle
        potential, and a perimeter potential. Accepts no arguments, and must be passed as a
        single string instead of a list.
      * 'edge': an edge potential field in which the potential is a function of the change in the
        edge length, summed over each edge in the mesh.
      * 'angle': an angle potential field in which the potential is a function of the change in
        the angle measure, summed over all angles in the mesh.
      * 'perimeter': a potential that depends on the vertices on the perimeter of a 2D mesh
        remaining in place; the potential changes as a function of the distance of each perimeter
        vertex from its reference position.
      * 'anchor': a potential that depends on the distance of a set of vertices from fixed points
        in space. After the shape name second argument, an anchor must be followed by a list of
        vertex ids then a list of fixed points to which the vertex ids are anchored:
        ['anchor', shape_name, vertex_ids, fixed_points, args...].

    The following are valid shape names:
      * 'harmonic': a harmonic function with the form (c/q) * abs(x - x0)^q.
        Parameters: 
          * 'scale', the scale parameter c; default: 1.
          * 'order', the order parameter q; default: 2.
      * 'Lennard-Jones': a Lennard-Jones function with the form c (1 + (r0/r)^q - 2(r0/r)^(q/2));
        Parameters:
          * 'scale': the scale parameter c; default: 1. 
          * 'order': the order parameter q; default: 2.
      * 'Gaussian': A Gaussian function with the form c (1 - exp(-0.5 abs((x - x0)/s)^q))
        Parameters:
          * 'scale': the scale parameter c; default: 1.
          * 'order': the order parameter q; default: 2.
          * 'sigma': the standard deviation parameter s; default: 1.
      * 'infinite-well': an infinite well function with the form 
        c ( (((x0 - m)/(x - m))^q - 1)^2 + (((M - x0)/(M - x))^q - 1)^2 )
        Parameters:
          * 'scale': the scale parameter c; default: 1.
          * 'order': the order parameter q; default: 0.5.
          * 'min': the minimum value m; default: 0.
          * 'max': the maximum value M; default: pi.

    Options: The following optional arguments are accepted.
      * max_steps (default: 25000) the maximum number of steps to minimize for.
      * max_step_size (default: 0.1) the maximum distance to allow a vertex to move in a single
        minimization step.
      * max_pe_change: the maximum fraction of the initial potential value that the minimizer
        should minimize away before returning; i.e., 0 indicates that no minimization should be
        allowed while 0.9 would indicate that the minimizer should minimize until the potential
        is 10% or less of the initial potential.

    Examples:
      registered_mesh = mesh_register(
         mesh,
         [['edge', 'harmonic', 'scale', 0.5], # slightly weak edge potential
          ['angle', 'infinite-well'], # default arguments for an infinite-well angle potential
          ['anchor', 'Gaussian', [1, 10, 50], [[0.0, 0.0], [1.1, 1.1], [2.2, 2.2]]]],
         max_step_size=0.05,
         max_steps=10000)
    '''
    global _java
    if _java is None: init_registration()
    # Sanity checking.
    # First, make sure that the arguments are all okay:
    if not isinstance(mesh, CorticalMesh):
        raise RuntimeError('mesh argument must be an instance of neuropythy.cortex.CorticalMesh')
    if not isinstance(max_steps, (int, long)) or max_steps < 1:
        raise RuntimeError('max_steps argument must be a positive integer')
    if not isinstance(max_steps, (float, int, long)) or max_step_size <= 0:
        raise RuntimeError('max_step_size must be a positive number')
    if not isinstance(max_pe_change, (float, int, long)) or max_pe_change <= 0 or max_pe_change > 1:
        raise RuntimeError('max_pe_change must be a number x such that 0 < x <= 1')
    # Parse the field argument.
    faces  = to_java_ints([mesh.index[frow] for frow in mesh.faces])
    coords = to_java_doubles(mesh.coordinates)
    potential = _parse_field_arguments(field, faces, coords)
    # Okay, that's basically all we need to do the minimization...
    minimizer = _java.jvm.nben.mesh.registration.Minimizer(potential, coords)
    minimizer.step(float(max_pe_change), int(max_steps), float(max_step_size))
    return np.array(minimizer.getX())

# How we construct a Schira Model:
class SchiraModel:
    '''
    The SchiraModel class is a Python wrapper around the Java nben.neuroscience.SchiraModel class;
    it handles conversion from visual field angle to cortical surface coordinates and vice versa for
    the Banded Double-Sech model proposed in the following paper:
    Schira MM, Tyler CW, Spehar B, Breakspear M (2010) Modeling Magnification and Anisotropy in the
    Primate Foveal Confluence. PLOS Comput Biol 6(1):e1000651. doi:10.1371/journal.pcbi.1000651.
    '''

    # These are the accepted arguments to the model:
    default_parameters = {
        'A': 0.5,
        'B': 135.0,
        'lambda': 1.0,
        'psi': 0.15,
        'scale': [7.0, 8.0],
        'shear': [[1.0, -0.2], [0.0, 1.0]],
        'center': [-7.0, -2.0],
        'v1size': 1.2,
        'v2size': 0.6,
        'v3size': 0.4,
        'hv4size': 0.9,
        'v3asize': 0.9}
    # This function checks the given arguments to see if they are okay:
    def __check_parameters(self, parameters):
        # we don't care if there are extra parameters; we just make sure the given parameters make
        # sense, then return the full set of parameters
        opts = {
            k: parameters[k] if k in parameters else v
            for (k,v) in SchiraModel.default_parameters.iteritems()}
        return opts

    # This class is immutable: don't change the params to change the model; 
    # don't change the java object!
    def __setattr__(self, name, val):
        raise ValueError('The SchiraModel class is immutable; its objects cannot be edited')

    def __init__(self, **opts):
        global _java
        if _java is None:
            init_registration()
        # start by getting the proper parameters
        params = self.__check_parameters(opts)
        # Now, do the translations that we need...
        if isinstance(params['scale'], Number):
            params['scale'] = [params['scale'], params['scale']]
        if isinstance(params['shear'], Number) and params['shear'] == 0:
            params['shear'] = [[1, 0], [0, 1]]
        elif params['shear'][0][0] != 1 or params['shear'][1][1] != 1:
            raise RuntimeError('shear matrix [0,0] elements and [1,1] elements must be 1!')
        if isinstance(params['center'], Number) and params['center'] == 0:
            params['center'] = [0.0, 0.0]
        self.__dict__['parameters'] = make_dict(params)
        # Okay, let's construct the object...
        self.__dict__['_java_object'] = _java.jvm.nben.neuroscience.SchiraModel(
            params['A'],
            params['B'],
            params['lambda'],
            params['psi'],
            params['v1size'],
            params['v2size'],
            params['v3size'],
            params['hv4size'],
            params['v3asize'],
            params['center'][0],
            params['center'][1],
            params['scale'][0],
            params['scale'][1],
            params['shear'][0][1],
            params['shear'][1][0])
    
    def angle_to_cortex(self, theta, rho):
        global _java
        if _java is None: init_registration()
        iterTheta = hasattr(theta, '__iter__')
        iterRho = hasattr(rho, '__iter__')
        if iterTheta and iterRho:
            if len(theta) != len(rho):
                raise RuntimeError('Arguments theta and rho must be the same length!')
            return self._java_object.angleToCortex(to_java_doubles(theta), to_java_doubles(rho))
        elif iterTheta:
            return self._java_object.angleToCortex(to_java_doubles(theta),
                                                   to_java_doubles([rho for t in theta]))
        elif iterRho:
            return self._java_object.angleToCortex(to_java_doubles([theta for r in rho]),
                                                   to_java_doubles(rho))
        else:
            return self._java_object.angleToCortex(theta, rho)
    def cortex_to_angle(self, x, y):
        global _java
        iterX = hasattr(x, '__iter__')
        iterY = hasattr(y, '__iter__')
        if iterX and iterY:
            if len(x) != len(y):
                raise RuntimeError('Arguments x and y must be the same length!')
            return self._java_object.cortexToAngle(to_java_doubles(x), to_java_doubles(y))
        elif iterX:
            return self._java_object.cortexToAngle(to_java_doubles(x),
                                                   to_java_doubles([y for i in x]))
        elif iterY:
            return self._java_object.cortexToAngle(to_java_doubles([x for i in y]),
                                                   to_java_doubles(y))
        else:
            return self._java_object.cortexToAngle(x, y)

def schira_anchors(mesh, mdl,
                   polar_angle=None, eccentricity=None,
                   weight=None, weight_cutoff=None,
                   shape='Gaussian', suffix=None):
    '''
    schira_anchors(mesh, model) is intended for use with the mesh_register function and the 
    SchiraModel class; it yields a description of the anchor points that tie relevant vertices of
    the given mesh to points predicted by the given SchiraModel object, model.

    Options:
      * polar_angle (default None) specifies that the given data should be used in place of the
        'polar_angle' or 'PRF_polar_angle'  property values. The given argument must be numeric and
        the same length as the the number of vertices in the mesh. If None is given, then the
        property value of the mesh is used; if a list is given and any element is None, then the
        weight for that vertex is treated as a zero. If the option is a string, then the property
        value with the same name isused as the polar_angle data.
      * eccentricity (default None) specifies that the given data should be used in places of the
        'eccentricity' or 'PRF_eccentricity' property values. The eccentricity option is handled 
        virtually identically to the polar_angle option.
      * weight (default None) specifies that the weight or scale of the data; this is handled
        generally like the polar_angle and eccentricity options, but may also be 1, indicating that
        all vertices with polar_angle and eccentricity values defined will be given a weight of 1.
        If weight is left as None, then the function will check for 'weight',
        'variance_explained', 'PRF_variance_explained', and 'retinotopy_weight' values and will use
        the first found (in that order). If none of these is found, then a value of 1 is assumed.
      * weight_cutoff (default 0) specifies that the weight must be higher than the given value inn
        order to be included in the fit; vertices with weights below this value have their weights
        truncated to 0.
      * shape (default 'Gaussian') specifies the shape of the potential function (see mesh_register)
      * suffix (default None) specifies any additional arguments that should be appended to the 
        potential function description list that is produced by this function; i.e., schira_anchors
        produces a list, and the contents of suffix, if given and not None, are appended to that
        list (see mesh_register).

    Example:
    The schira_anchors function is intended for use with mesh_register, as follows:
    # Define our Schira Model:
    model = neuropythy.registration.SchiraModel()
    # Make sure our mesh has polar angle, eccentricity, and weight data:
    mesh.prop('polar_angle',  polar_angle_vertex_data);
    mesh.prop('eccentricity', eccentricity_vertex_data);
    mesh.prop('weight',       variance_explained_vertex_data);
    # register the mesh using the retinotopy and model:
    registered_mesh = neuropythy.registration.mesh_register(
       mesh,
       ['mesh', schira_anchors(mesh, model, weight_cutoff=0.2)],
       max_step_size=0.05,
       max_steps=10000)
    '''
    if not isinstance(mdl, SchiraModel):
        raise RuntimeError('given model is not a SchiraModel instance!')
    if not isinstance(mesh, CorticalMesh):
        raise RuntimeError('given mesh is not a CorticalMesh object!')
    n = len(mesh.vertex_labels)
    # make sure we have our polar angle/eccen/weight values:
    polar_angle = polar_angle if polar_angle is not None \
        else mesh.prop('polar_angle') if mesh.has_property('polar_angle') \
        else mesh.prop('PRF_polar_angle') if mesh.has_property('PRF_polar_angle') \
        else None
    if polar_angle is None:
        raise RuntimeError('No polar angle data given to schira_anchors!')
    if isinstance(polar_angle, dict):
        # a dictionary is okay, we just need to fix it to a list:
        tmp = polar_angle
        polar_angle = [tmp[i] if i in tmp else None for i in range(n)]
    if len(polar_angle) != n:
        raise RuntimeError('Polar angle data has incorrect length!')
    # Now Polar Angle...
    eccentricity = eccentricity if eccentricity is not None \
        else mesh.prop('eccentricity') if mesh.has_property('eccentricity') \
        else mesh.prop('PRF_eccentricity') if mesh.has_property('PRF_eccentricity') \
        else None
    if eccentricity is None:
        raise RuntimeError('No eccentricity data given to schira_anchors!')
    if isinstance(eccentricity, dict):
        tmp = eccentricity
        eccentricity = [tmp[i] if i in tmp else None for i in range(n)]
    if len(eccentricity) != n:
        raise RuntimeError('Eccentricity data has incorrect length!')
    # Now Weight...
    weight = weight if weight is not None \
        else mesh.prop('weight') if mesh.has_property('weight') \
        else mesh.prop('variance_explained') if mesh.has_property('variance_explained') \
        else mesh.prop('PRF_variance_explained') if mesh.has_property('PRF_variance_explained') \
        else mesh.prop('retinotopy_weight') if mesh.has_property('retinotopy_weight') \
        else None
    if weight is None:
        weight = 1
    if isinstance(weight, dict):
        tmp = weight
        weight = [tmp[i] if i in tmp else None for i in range(n)]
    if isinstance(weight, Number):
        weight = [weight for i in range(n)]
    if len(weight) != n:
        raise RuntimeError('Weight data has incorrect length!')
    # let's go through and fix up the weights/polar angles/eccentricities into appropriate lists
    if weight_cutoff is None:
        data = [[i, mdl.angle_to_cortex(polar_angle[i], eccentricity[i]), weight[i]]
                for i in range(n)
                if (polar_angle[i] is not None and eccentricity[i] is not None 
                    and weight[i] is not None and weight[i] != 0)]
    else:
        data = [[i, mdl.angle_to_cortex(polar_angle[i], eccentricity[i]), weight[i]]
                for i in range(n)
                if (polar_angle[i] is not None and eccentricity[i] is not None 
                    and weight[i] is not None and weight[i] >= weight_cutoff)]
    # okay, we've partially parsed the data that was given; now we can construct the final list of
    # instructions:
    return ['anchor', shape,
            [d[0] for d in data for k in range(len(d[1]))],
            np.asarray([pt for d in data for pt in d[1]]).T,
            'scale', [d[2] for d in data for k in range(len(d[1]))]
           ] + ([] if suffix is None else suffix)

_empirical_retinotopy_names = {
    'polar_angle':  ['PRF_polar_angle',  'empirical_polar_angle',  'measured_polar_angle'
                     'polar_angle'],
    'eccentricity': ['PRF_eccentricity', 'empirical_eccentricity', 'measured_eccentricity'
                     'eccentricity'],
    'weight':       ['PRF_variance_explained',       'PRF_weight',
                     'measured_variance_explained',  'measured_weight',
                     'empirical_variance_explained', 'empirical_weight'
                     'variance_explained',           'weight']}
# handy function for picking out properties automatically...
def empirical_retinotopy_data(hemi, retino_type):
    '''
    empirical_retinotopy_data(hemi, t) yields a numpy array of data for the given hemisphere object
    and retinotopy type t; it does this by looking at the properties in hemi and picking out any
    combination that is commonly used to denote empirical retinotopy data. These common names are
    stored in _empirical_retintopy_names, in order of preference, which may be modified.
    The argument t should be one of 'polar_angle', 'eccentricity', 'weight'.
    '''
    dat = _empirical_retinotopy_names[retino_type.lower()]
    return next((hemi.prop(s) for s in dat if hemi.has_property(s)), None)
    
def register_retinotopy(hemi,
                        schira_model=SchiraModel(), radius=pi/4.0,
                        polar_angle=None, eccentricity=None, weight=None, weight_cutoff=None,
                        sigma=0.5, edge_scale=1.0, angle_scale=1.0, schira_scale=15.0,
                        max_steps=30000, max_step_size=0.05,
                        registration_name='retinotopy'):
    '''
    register_retinotopy(hemi) yields the result of registering the given hemisphere's polar angle
    and eccentricity data to the SchiraModel, a registration in which the vertices are aligned with
    the Schira model of retinotopy. The registration is added to the hemisphere's topology unless
    the option registration_name is set to None.

    Options:
      * schira_model specifies the instance of the Schira model to use (default: SchiraModel()).
      * polar_angle, eccentricity, and weight specify the property names for the respective
        quantities; these may alternately be lists or numpy arrays of values. If weight is not given
        or found, then unity weight for all vertices is assumed. By default, each will check the
        hemisphere's properties for properties with compatible names; it will prefer the properties
        PRF_polar_angle, PRF_ecentricity, and PRF_variance_explained if possible.
      * weight_cutoff specifies the minimum value a vertex must have in the weight property in order
        to be considered as retinotopically relevant.
      * sigma specifies the standard deviation of the Gaussian shape for the Schira model anchors.
      * edge_scale, angle_scale, and schira_scale all specify the relative strengths of the various
        components of the potential field.
      * max_steps (default 30,000) specifies the maximum number of registration steps to run.
      * max_step_size (default 0.05) specifies the maxmim distance a single vertex is allowed to
        move in a single step of the minimization.
      * registration_name (default: 'retinotopy') specifies the name of the registration to register
        with the hemisphere's topology object.
    '''
    # Step 1: figure out what properties we're using...
    (ang, ecc, wgt) = [
        (hemi.prop(arg) if isinstance(arg, basestring) else
         arg            if hasattr(arg, '__iter__')    else
         None           if arg is not None             else
         empirical_retinotopy_data(hemi, argstr))
        for (arg, argstr) in [(polar_angle, 'polar_angle'),
                              (eccentricity, 'eccentricity'),
                              (weight, 'weight')]]
    if ang is None: raise ValueError('polar angle data not found')
    if ecc is None: raise ValueError('eccentricity data not found')
    ## we also want to make sure weight is 0 where there are none values
    wgt = np.asarray(
        [(0 if w is None else w)*(0 if a is None else 1)*(0 if e is None else 1)
         for (a,e,w) in zip(ang, ecc, [1 for e in ecc] if wgt is None else wgt)])
    ang = np.asarray([0 if a is None else a for a in ang])
    ecc = np.asarray([0 if e is None else e for e in ecc])
    # Step 2: get the properties over to the fsaverage_sym hemisphere
    lhemi = hemi if hemi.chirality == 'LH' else hemi.subject.RHX
    sym = freesurfer_subject('fsaverage_sym').LH
    sym.interpolate(lhemi, ang, apply='polar_angle')
    sym.interpolate(lhemi, ecc, apply='eccentricity')
    sym.interpolate(lhemi, wgt, apply='weight')
    # Step 3: make the projection
    msym = sym.projection(radius=radius)
    # Step 4: run the mesh registration
    r = mesh_register(
        msym,
        [['edge', 'harmonic', 'scale', edge_scale],
         ['angle', 'infinite-well', 'scale', angle_scale],
         ['perimeter', 'harmonic'],
         schira_anchors(msym, schira_model,
                        weight_cutoff=weight_cutoff,
                        suffix=['sigma', sigma, 'scale', schira_scale])],
        max_steps=max_steps,
        max_step_size=max_step_size)
    # Step 5: prepare the original subject's map for being warped over to the registration
    msub = lhemi.projection(mesh='fsaverage_sym', radius=radius)
    subvtcs = msub.vertex_labels
    msub.prop('polar_angle',  ang[subvtcs])
    msub.prop('eccentricity', ecc[subvtcs])
    msub.prop('weight',       wgt[subvtcs])
    ## okay, r is the registered coordinates; we can unproject them
    symrsphere = msym.unproject(r)
    ## make a new coordinate matrix for the registration
    symregcoords = np.array(sym.coordsinates, copy=True)
    symregcoords[:, msym.vertex_labels] = symrsphere
    symregmesh = sym.LH.surface(symregcoords)
    ## now, address the subject's coordinates in the original topology and unaddress in this
    ## new registered mesh
    addr = sym.topology.registrations['fsaverage_sym'].address(lhemi.coordinates[:,subvtcs])
    subrsphere = symregmesh.unaddress(addr)
    msub.coordinates = msub.reproject(subrsphere)
    if registration_name is not None:
        subregcoords = np.array(lhemi.coordinates, copy=True)
        subregcoords[:, subvtcs] = subrsphere
        hemi.topology.register(registration_name, subregcoords)
    # We return the subject's map
    return msub

# The topology and registration stuff is below:
class JavaTopology:
    '''
    JavaTopology(triangles, registrations) creates a topology object object with the given triangle
    mesh, defined by a 3xn matrix of triangle indices, and with the registration coordinate matrices
    given in the dictionary registrations. This class should only be instantiated by the neuropythy
    library and should generally not be constructed directly. See Hemisphere.topology objects to
    access a subject's topologies.
    '''
    def __init__(self, triangles, registrations):
        if _java is None:
            init_registration()
        # First: make a java object for the topology:
        faces = serialize_numpy(triangles.T, 'i')
        topo = _java.jvm.nben.geometry.spherical.MeshTopology.fromBytes(faces)
        # Okay, make our registration dictionary
        d = {k: topo.registerBytes(serialize_numpy(v, 'd'))
             for (k,v) in registrations.iteritems()}
        # That's all really
        self.__dict__['_java_object'] = topo
        self.__dict__['registrations'] = d
    def __getitem__(self, attribute):
        return self.registrations[attribute]
    def __setitem__(self, attribute, dat):
        self.registrations[attribute] = self._java_object.registerBytes(serialize_numpy(dat, 'd'))
    def keys(self):
        return self.registrations.keys()
    def iterkeys(self):
        return self.registrations.iterkeys()
    def values(self):
        return self.registrations.values()
    def itervalues(self):
        return self.registrations.itervalues()
    def items(self):
        return self.registrations.items()
    def iteritems(self):
        return self.registrations.iteritems()
    def __len__(self):
        return len(self.registrations)
    
    # These let us interpolate...
    def interpolate(fromtopo, data, order=2, fill=None):
        usable_keys = []
        for k in registrations.iterkeys():
            if k in fromtopo.registrations:
                usable_keys.append(k)
        if not usable_keys:
            raise RuntimeError('no registration found that links topologies')
        the_key = usable_keys[0]
        # Prep the data into java arrays
        jmask = serialize_numpy(np.asarray([1 if d is not None else 0 for d in data]), 'd')
        jdata = serialize_numpy(np.asarray([d if d is not None else 0 for d in data]), 'd')
        # okay, next step is to call out to the java...
        maskres = self._java_object.interpolateBytes(
            fromtopo.registrations[the_key],
            self.registrations[the_key].coordinates,
            order, jdata)
        datares = self._java_object.interpolateBytes(
            fromtopo.registrations[the_key],
            self.registrations[the_key].coordinates,
            order, jmask)
        # then interpret the results...
        return [datares[i] if maskres[i] == 1 else fill for i in range(len(maskres))]
