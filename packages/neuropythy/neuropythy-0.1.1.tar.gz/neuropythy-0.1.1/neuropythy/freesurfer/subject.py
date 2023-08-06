####################################################################################################
# neuropythy/freesurfer/subject.py
# Simple tools for use with FreeSurfer in Python
# By Noah C. Benson

import numpy as np
import numpy.linalg
import scipy as sp
import scipy.spatial as space
import nibabel.freesurfer.io as fsio
import nibabel.freesurfer.mghformat as fsmgh
import os, math
import itertools
import pysistence
from   pysistence import make_dict
from   neuropythy.cortex import CorticalMesh
from   neuropythy.topology import Topology
import neuropythy.geometry as geo

# These static functions are just handy
def spherical_distance(pt0, pt1):
    '''spherical_distance(a, b) yields the angular distance between points a and b, both of which
       should be expressed in spherical coordinates as (longitude, latitude).'''
    dtheta = pt1[0] - pt0[0]
    dphi   = pt1[1] - pt0[1]
    a = np.sin(dphi/2)**2 + np.cos(pt0[1]) * np.cos(pt1[1]) * np.sin(dtheta/2)**2
    return 2 * np.arcsin(np.sqrt(a))

class PropertyBox(list):
    '''PropertyBox is a simple class for lazily loading properties into a hemisphere or mesh. It
       should generally not be used directly and instead obtained from the Hemisphere class. Note
       that a PropertyBox object should behave like a list.'''
    def __init__(self, loader):
        self._loading_fn = loader
    def __len__(self):
        if 'data' not in self.__dict__: self.__load_data()
        return len(self.data)
    def __getitem__(self, key):
        if 'data' not in self.__dict__: self.__load_data()
        return self.data[key]
    def __iter__(self):
        if 'data' not in self.__dict__: self.__load_data()
        return iter(self.data)
    def __reversed__(self):
        if 'data' not in self.__dict__: self.__load_data()
        return reversed(self.data)
    def __contains__(self, item):
        if 'data' not in self.__dict__: self.__load_data()
        return item in self.data
    def __load_data(self):
        f = self._loading_fn
        dat = f()
        self.__dict__['data'] = dat

class Hemisphere:
    '''FreeSurfer.Hemisphere encapsulates the data contained in a subject's freesurfer hemisphere.
    This includes the various surface data as well as certain volume data.'''
    

    ################################################################################################
    # Lazy/Static Interface
    # This code handles the lazy interface; only three data are non-lazy and these are coordinates,
    # faces, and options; they may be set directly.

    # The following methods and static variable allow one to set particular members of the object
    # directly:
    @staticmethod
    def _check_property(self, name, val):
        if not isinstance(val, np.ndarray) and not isinstance(val, list):
            raise ValueError('property values must be lists or numpy arrays')
        return True
    @staticmethod
    def _check_properties(self, val):
        if not isinstance(val, dict):
            raise ValueError('properties must be a dictionary')
        for (k, v) in val.iteritems(): Hemisphere._check_property(self, k, v)
        if type(val) is pysistence.persistent_dict.PDict:
            return val
        else:
            return make_dict(**val)
    @staticmethod
    def _check_options(self, val):
        # Options just have to be a dictionary and are converted to an immutable one
        if not isinstance(val, dict):
            raise ValueError('options must be a dictionary')
        if type(val) is pysistence.persistent_dict.PDict:
            return val
        else:
            return make_dict(**val)
    __settable_members = {
        'properties': lambda m,v: Hemisphere._check_properties(m,v),
        'options': lambda m,v: Hemisphere._check_options(m,v)}

    # This static variable and these functions explain the dependency hierarchy in cached data
    def __make_surface(self, coords, faces, name, reg=None):
        return CorticalMesh(
            coords,
            faces,
            subject = self.subject,
            hemisphere = self,
            meta_data = self.meta_data.using(
                **{'subject': self.subject,
                   'hemisphere': self,
                   'name': name,
                   'registration': reg}))
    def _load_surface_data(self, name):
        path = self.subject.surface_path(name, self.name)
        if not os.path.exists(path):
            return None
        else:
            data = fsio.read_geometry(path)
            data[0].setflags(write=False)
            data[1].setflags(write=False)
            return data
    def _load_surface_data_safe(self, name):
        try:
            return self._load_surface_data(name)
        except:
            return (None, None)
    def _load_surface(self, name, preloaded=None, reg=None):
        data = self._load_surface_data(name) if preloaded is None else preloaded
        return self.__make_surface(data[0], data[1], name, reg=reg)
    def _load_sym_surface(self, name):
        path = self.subject.surface_path(name, self.name)
        if not os.path.exists(path):
            return None
        else:
            data = fsio.read_geometry(path)
            data[0].setflags(write=False)
            data[1].setflags(write=False)
            return self.__make_surface(data[0], data[1], name)
    def _load_ribbon(self):
        path = self.subject.volume_path('ribbon', self.name)
        if not os.path.exists(path):
            return None
        else:
            data = fsmgh.load(path)
            # for now, no post-processing, just loading of the MGHImage
            return data
    def _make_topology(self, sphere, fsave, fssym):
        if sphere is None:
            return None
        names = [self.subject.id, 'fsaverage', 'fsaverage_sym'];
        surfs = [sphere, fsave, fssym]
        return Topology(
            sphere.faces, 
            {names[i]: surfs[i].coordinates.T for i in range(len(names)) if surfs[i] is not None})
    @staticmethod
    def _check_meta_data(opts):
        md = opts.get('meta_data', {})
        if not isinstance(md, dict):
            raise ValueError('hemisphere meta-data must be a dictionary')
        if type(md) is pysistence.persistent_dict.PDict:
            return md
        else:
            return make_dict(**md)
        
    __lazy_members = {
        'meta_data':            (('options',), lambda hemi,opts: Hemisphere._check_meta_data(opts)),
        'white_surface':        ((), lambda hemi: hemi._load_surface('white')),
        'pial_surface':         ((), lambda hemi: hemi._load_surface('pial')),
        'inflated_surface':     ((), lambda hemi: hemi._load_surface('inflated')),

        'sphere_surface_data':  ((), lambda hemi: hemi._load_surface_data('sphere')),
        'fs_surface_data':      ((), lambda hemi: hemi._load_surface_data_safe('sphere.reg')),
        'sym_surface_data':     ((), 
                                 lambda hemi: \
                                    hemi._load_surface_data_safe('fsaverage_sym.sphere.reg')),
        'faces':                (('sphere_surface_data',), lambda hemi,dat: dat[1]),

        'sphere_surface':       (('sphere_surface_data','topology'), 
                                 lambda hemi,dat,topo: hemi._load_surface(
                                     'sphere',
                                     preloaded=dat,
                                     reg=(topo.registrations[hemi.subject.id]
                                          if hemi.subject.id in topo.registrations
                                          else None))),
        'fs_sphere_surface':    (('fs_surface_data','topology'),
                                 lambda hemi,dat,topo: (
                                    hemi.sphere_surface if hemi.subject.id == 'fsaverage'
                                    else None if dat == (None,None)
                                    else hemi._load_surface(
                                            'sphere.reg',
                                            preloaded=dat,
                                            reg=(topo.registrations['fsaverage']
                                                 if 'fsaverage' in topo.registrations
                                                 else None)))),
        'sym_sphere_surface':   (('sym_surface_data','topology'),
                                 lambda hemi,dat,topo: (
                                    hemi.sphere_surface if hemi.subject.id == 'fsaverage_sym'
                                    else None if dat is None
                                    else hemi._load_surface(
                                            'fsaverage_sym.sphere.reg',
                                            preloaded=dat,
                                            reg=(topo.registrations['fsaverage_sym']
                                                 if 'fsaverage_sym' in topo.registrations
                                                 else None)))),

        'vertex_count':         (('sphere_surface_data',), lambda hemi,dat: dat[0].shape[1]),
        'midgray_surface':      (('white_surface', 'pial_surface'),
                                 lambda hemi,W,P: hemi.__make_surface(
                                     0.5*(W.coordinates + P.coordinates),
                                     W.faces,
                                     'midgray')),
        'occipital_pole_index': (('inflated_surface',),
                                 lambda hemi,mesh: np.argmin(mesh.coordinates[1])),
        'ribbon':               ((), lambda hemi: hemi._load_ribbon()),
        'chirality':            (('name',), 
                                 lambda hemi,name: 'LH' if name == 'LH' or name == 'RHX' else 'RH'),
        'topology':             (('sphere_surface_data', 'fs_surface_data', 'sym_surface_data'),
                                 lambda hemi,sph,fs,sym: Topology(sph[1],
                                                                  {hemi.subject.id: sph[0],
                                                                   'fsaverage': fs[0],
                                                                   'fsaverage_sym': sym[0]}))}
    
    # This function will clear the lazily-evaluated members when a given value is changed
    def __update_values(self, name):
        for (sname, (deps, fn)) in Hemisphere.__lazy_members.items():
            if name in deps and sname in self.__dict__:
                del self.__dict__[sname]

    # This is the most important function, given the encapsulation of this class:
    def __setattr__(self, name, val):
        if name in Hemisphere.__settable_members:
            fn = Hemisphere.__settable_members[name]
            self.__dict__[name] = fn(self, val)
            self.__update_values(name)
        elif name in Hemisphere.__lazy_members:
            raise ValueError('The member %s is a lazy value and cannot be set' % name)
        else:
            raise ValueError('Unrecognized Hemisphere member: %s' % name)

    # The getattr method makes sure that lazy members are computed when requested
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in Hemisphere.__lazy_members:
            (deps, fn) = Hemisphere.__lazy_members[name]
            tmp = fn(self, *map(lambda x: getattr(self, x), deps))
            self.__dict__[name] = tmp
            return tmp
        else:
            raise ValueError('Unrecognized member of Hemisphere: %s' % name)

    # Make a surface out of coordinates, if desired
    def surface(self, coords, name=None):
        '''
        hemi.surface(coords) yields a new surface with the given coordinate matrix and the topology
        of this hemisphere, hemi. The coordinate matrix must have hemi.vertex_count points.
        '''
        coords = np.asarray(coords)
        coords = (coords   if coords.shape[1] == self.vertex_count else
                  coords.T if coords.shape[0] == self.vertex_count else
                  None)
        if coords is None: raise ValueError('Coordinate matrix was invalid size!')
        return self.__make_surface(coords, self.faces, name)

    
    ################################################################################################
    # The Constructor
    def __init__(self, subject, type, **args):
        if not isinstance(subject, Subject):
            raise ValueError('Argument subject must be a FreeSurfer.Subject object')
        if type.upper() not in set(['RH', 'LH', 'RHX', 'LHX']):
            raise ValueError('Argument type must be RH, LH, RHX, or LHX')
        self.__dict__['subject'] = subject
        self.__dict__['name'] = type.upper()
        self.__dict__['directory'] = os.path.join(subject.directory, 'surf')
        self.properties = args.pop('properties', make_dict())
        self.options = args
        self.__init_properties()
    
    ################################################################################################
    # The display function
    def __repr__(self):
        return "Hemisphere(" + self.name + ", <subject: " + self.subject.id + ">)"

    
    ################################################################################################
    # Property code
    def add_property(self, name, prop=Ellipsis):
        '''hemi.add_property(name, prop) adds (or overwrites) the given property with the given name
           in the given hemi. The name must be a valid dictionary key and the prop argument must be
           a list of numpy array of values, one per vertex.
           hemi.add_property(d) adds all of the properties in the given dictionary of properties, 
           d.
           Note that in either case, if the value of prop or the value in a dictionary item is
           None, then the item is removed from the property list instead of being added.'''
        if prop is Ellipsis:
            if isinstance(name, dict):
                for (n,p) in name.iteritems():
                    self.add_property(n, p)
            else:
                raise ValueError('add_property must be called with a name and propery or a dict')
        else:
            if prop is None:
                self.remove_property(name)
            else:
                Hemisphere._check_property(self, name, prop)
                self.__dict__['properties'] = self.properties.using(**{name: prop})

    def property_names(self):
        '''hemi.property_names() yields a set of property names for the given hemi.'''
        return set(self.properties.keys())

    def has_property(self, name):
        '''hemi.has_property(name) yields True if the given hemisphere contains the property with
           the given name and False otherwise.'''
        return name in self.properties

    def remove_property(self, name):
        '''hemi.remove_property(name) removes the property with the given name from the given hemi.
           The name argument may also be an iterable collection of names, in which case all are
           removed.'''
        if hasattr(name, '__iter__'):
            for n in name: self.remove_property(n)
        elif name in self.properties:
            self.__dict__['properties'] = self.properties.without(name)
    
    def property_value(self, name):
        '''hemi.property_value(name) yields a list of the property values with the given name. If
           name is an iterable, then property_value automatically threads across it. If no such
           property is found in the mesh, then None is returned.'''
        if hasattr(name, '__iter__'):
            return map(lambda n: self.property_value(n), name)
        else:
            return self.properties.get(name, None)
            
    def prop(self, name, arg=Ellipsis):
        '''hemi.prop(...) is a generic function for handling mesh properties. It may be called
           with a variety of arguments:
             * hemi.prop(name) is equivalent to hemi.property_value(name) if name is either not
               an iterable or is an iterable that is not a dictionary
             * hemi.prop(d) is equivalent to hemi.add_property(d) if d is a dictionary
             * hemi.prop(name, val) is equivalent to hemi.add_property(name, val) if val is not
               None
             * hemi.prop(name, None) is equivalent to hemi.remove_property(name)'''
        if arg is Ellipsis:
            if isinstance(name, dict):
                self.add_property(name)
            else:
                return self.property_value(name)
        else:
            self.add_property(name, arg)

    def interpolate(self, from_hemi, property_name, 
                    apply=True, method='automatic', mask=None, null=None, n_jobs=1):
        '''
        hemi.interpolate(from_hemi, prop) yields a list of property values that have been resampled
        onto the given hemisphere hemi from the property with the given name prop of the given 
        from_mesh. If the optional apply is set to True (the default) or to a new property name
        string, the property is added to hemi as well; otherwise it is only returned. Optionally,
        prop may be a list of numpy array of values the same length as the mesh's vertex list; in
        this case, the apply option must be a new property name string, otherwise it is treated as
        False. Note that in order to work, the hemi and from_hemi objects must share a registration
        such as fsaverage or fsaverage_sym.

        Options:
          * mask (default: None) indicates that the given True/False or 0/1 valued list/array should
            be used; any point whose nearest neighbor (see below) is in the given mask will, instead
            of an interpolated value, be set to the null value (see null option).
          * null (default: None) indicates the value that should be placed in the returned result if
            either a vertex does not lie in any triangle or a vertex is masked out via the mask
            option.
          * smoothing (default: 2) assuming that the method is 'interpolate' or 'automatic', this
            is the exponent used to smooth the interpolated surface; 1 is pure linear interpolation
            while 2 represents a slightly smoother version of this. Note that this is not an order
            of interpolation option.
          * method (default: 'automatic') specifies what method to use for interpolation. The only
            currently supported methods are 'automatic' or 'nearest'. The 'nearest' method does not
            actually perform a nearest-neighbor interpolation but rather assigns to a destination
            vertex the value of the source vertex whose veronoi-like polygon contains the
            destination vertex; note that the term 'veronoi-like' is used here because it uses the
            Voronoi diagram that corresponds to the triangle mesh and not the true delaunay
            triangulation. The 'automatic' checks every destination vertex and assigns it the
            'nearest' value if that value would not be a number, otherwise it interpolates linearly
            within the vertex's source triangle.
          * n_jobs (default: 1) is passed along to the cKDTree.query method, so may be set to an
            integer to specify how many processors to use, or may be -1 to specify all processors.
        '''
        if from_hemi.chirality != self.chirality:
            raise ValueError('hemispheres have opposite chiralities')
        if isinstance(property_name, basestring):
            if not from_hemi.has_property(property_name):
                raise ValueError('given property ' + property_name + ' is not in from_hemi!')
            data = from_hemi.prop(property_name)
        elif type(property_name).__module__ == np.__name__:
            data = property_name
            property_name = apply if isinstance(apply, basestring) else None
        elif hasattr(property_name, '__iter__'):
            if all(isinstance(s, basestring) for s in property_name):
                return {p: self.interpolate(from_hemi, p, 
                                            method=method, mask=mask,
                                            null=null, n_jobs=n_jobs)
                        for p in property_name}
            else:
                data = np.asarray(property_name)
                property_name = apply if isinstance(apply, basestring) else None
        else:
            raise ValueError('property_name is not a string or valid list')
        # pass data along to the topology object...
        result = self.topology.interpolate_from(from_hemi.topology, data,
                                                method=method, mask=mask,
                                                null=null, n_jobs=n_jobs)
        if result is not None:
            if apply is True and property_name is not None:
                self.prop(property_name, result)
            elif isinstance(apply, basestring):
                self.prop(apply, result)
        return result

    # This [private] function and this variable set up automatic properties from the FS directory
    # in order to be auto-loaded, a property must appear in this dictionary:
    _auto_properties = {
        'sulc':      ('convexity',              lambda f: fsio.read_morph_data(f)),
        'thickness': ('thickness',              lambda f: fsio.read_morph_data(f)),
        'area':      ('white_surface_area',     lambda f: fsio.read_morph_data(f)),
        'area.mid':  ('midgray_surface_area',   lambda f: fsio.read_morph_data(f)),
        'area.pial': ('pial_surface_area',      lambda f: fsio.read_morph_data(f)),
        'curv':      ('curvature',              lambda f: fsio.read_morph_data(f)),

        'prf_eccen': ('PRF_eccentricity',       lambda f: fsio.read_morph_data(f)),
        'prf_angle': ('PRF_polar_angle',        lambda f: fsio.read_morph_data(f)),
        'prf_size':  ('PRF_size',               lambda f: fsio.read_morph_data(f)),
        'prf_varex': ('PRF_variance_explained', lambda f: fsio.read_morph_data(f)),

        'retinotopy_eccen': ('eccentricity',    lambda f: fsio.read_morph_data(f)),
        'retinotopy_angle': ('polar_angle',     lambda f: fsio.read_morph_data(f)),
        'retinotopy_areas': ('visual_area',     lambda f: fsio.read_morph_data(f))}
    # properties grabbed out of MGH or MGZ files in the sufsio.read_morph_data(f)),
    _mgh_properties = {}
    # funciton for initializing the auto-loading properties
    def __init_properties(self):
        dir = self.directory
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]            
        autoprops = Hemisphere._auto_properties
        for file in files:
            if len(file) > 2 and file[0:2].upper() == self.chirality and file[3:] in autoprops:
                (name, fn) = autoprops[file[3:]]
                #self.prop(name, PropertyBox(lambda: fn(os.path.join(dir, file))))
                self.prop(name, fn(os.path.join(dir, file)))
        # We also want to auto-add labels:
        dir = os.path.join(self.subject.directory, 'label')
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        for file in files:
            if len(file) > 9 and file[0:2].upper() == self.chirality and file[-6:] == '.label':
                if len(file) < 17 or file[-13:-6] != '.thresh':
                    lbl = set(fsio.read_label(os.path.join(dir, file)))
                    self.prop(
                        file[3:-6],
                        [True if k in lbl else False for k in range(self.vertex_count)])
                #else:
                #    (lbl, sclr) = fsio.read_label(os.path.join(dir, file), read_scalars=True)
                #    lbl = {lbl[i]: i for i in range(len(lbl))}
                #    self.prop(
                #        file[3:-13] + '_threshold',
                #        [sclr[lbl[k]] if k in lbl else None for k in range(self.vertex_count)])
        # And MGH/MGZ files in surf:
        dir = os.path.join(self.subject.directory, 'surf')
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        for f in files:
            if (f[-4:].lower() == '.mgh' or f[-4:].lower() == '.mgz') and \
                    f[2] == '.' and f[0:2].upper() == self.chirality and \
                    f[3:-4] in Hemisphere._mgh_properties:
                (name, fn) = Hemisphere._mgh_properties[f[3:-4]]
                self.prop(name, fn(os.path.join(dir, f)))

    # This method is a convenient way to get the occipital pole coordinates for the various
    # surfaces in a hemisphere...
    def occipital_pole(self, surfname):
        surfname = surfname.lower()
        if not surfname.lower().endswith('_surface'):
            surfname = surfname + '_surface'
        surf = self.__getattr__(surfname)
        opIdx = self.occipital_pole_index
        return surf.coordinates[:, opIdx]

    # These methods, values, and the projection fn are all related to map projection
    @staticmethod
    def _orthographic_projection(X, params): 
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        return X[1:3]
    @staticmethod
    def _orthographic_projection_inverse(X, params): 
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        r = params['sphere_radius']
        Xnorm = X / r
        return np.asarray([r * np.sqrt(1.0 - (Xnorm ** 2).sum(0)), X[0], X[1]])
    @staticmethod
    def _equirectangular_projection(X, params):
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        X = X / np.sqrt((X ** 2).sum(0))
        r = params['sphere_radius']
        return r / math.pi * np.asarray([np.arctan2(X[1], X[0]), np.arcsin(X[2])])
    @staticmethod
    def _equirectangular_projection_inverse(X, params):
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        r = params['sphere_radius']
        X = math.pi * X / r
        return np.asarray([np.cos(X[0]) * r, 
                           np.sin(X[0]) * r,
                           np.sin(X[1]) * r])
    @staticmethod
    def _mercator_projection(X, params):
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        X = X / np.sqrt((X ** 2).sum(0))
        r = params['sphere_radius']
        return r * np.asarray([np.arctan2(X[1], X[0]),
                               np.log(np.tan(0.25 * math.pi + 0.5 * np.arcsin(X[2])))])
    @staticmethod
    def _mercator_projection_inverse(X, params):
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        r = params['sphere_radius']
        X = X / r
        return r * np.asarray([np.cos(X[0]),
                               np.sin(X[0]),
                               np.sin(2 * (np.arctan(np.exp(X[1])) - 0.25*math.pi))])
    @staticmethod
    def _sinusoidal_projection(X, params):
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        X = X / np.sqrt((X ** 2).sum(0))
        r = params['sphere_radius']
        phi = np.arcsin(X[2])
        return r / math.pi * np.asarray([np.arctan2(X[1], X[0]) * np.cos(phi), phi])
    @staticmethod
    def _sinusoidal_projection_inverse(X, params):
        X = np.asarray(X)
        X = X if X.shape[0] < 4 else X.T
        r = params['sphere_radius']
        X = math.pi * X / r
        z = np.sin(X[1])
        cosphi = np.cos(X[1])
        return np.asarray([np.cos(X[0] / cosphi) * r,
                           np.sin(X[0] / cosphi) * r,
                           np.sin(X[1]) * r])

    __projection_methods = {
        'orthographic':    lambda X,p: Hemisphere._orthographic_projection(X,p),
        'equirectangular': lambda X,p: Hemisphere._equirectangular_projection(X,p),
        #'mollweide':       lambda X,p: Hemisphere._mollweide_projection(X,p),
        'mercator':        lambda X,p: Hemisphere._mercator_projection(X,p),
        'sinusoidal':      lambda X,p: Hemisphere._sinusoidal_projection(X,p)}
    __projection_methods_inverse = {
        'orthographic':    lambda X,p: Hemisphere._orthographic_projection_inverse(X,p),
        'equirectangular': lambda X,p: Hemisphere._equirectangular_projection_inverse(X,p),
        #'mollweide':       lambda X,p: None,
        'mercator':        lambda X,p: Hemisphere._mercator_projection_inverse(X,p),
        'sinusoidal':      lambda X,p: Hemisphere._sinusoidal_projection_inverse(X,p)}
    def __interpret_projection_params(self, params):
        # Figure out which spherical surface we're using...
        if 'surface' not in params or params['surface'].lower() == 'native':
            params['surface'] = 'native'
            params['mesh'] = self.sphere_surface
        elif params['surface'].lower() == 'fsaverage':
            params['surface'] = 'fsaverage'
            params['mesh'] = self.fs_sphere_surface
        elif params['surface'].lower() == 'fsaverage_sym':
            params['surface'] = 'fsaverage_sym'
            params['mesh'] = self.sym_sphere_surface
        elif params['surface'] in self.topology.registrations:
            surfname = params['surface']
            params['mesh'] = self.__make_surface(
                self.topology.registrations[surfname].coordinates.T,
                self.faces,
                surfname)
        else:
            raise ValueError('Unrecognized spherical surface: %s' % params['surface'])
        sphere = params['mesh']
        # important parameters: center and radius => indices
        if 'center' not in params:
            params['center'] = sphere.coordinates[:, self.occipital_pole_index]
        elif isinstance(params['center'], int):
            params['center'] = sphere.coordinates[:, params['center']]
        if 'radius' not in params:
            params['radius'] = math.pi / 4.0
        elif not isinstance(params['radius'], (int, long, float)) or params['radius'] <= 0:
            raise ValueError('radius parameter must be a positive integer')
        # also, we need to worry about the method...
        if 'method' not in params:
            params['method'] = 'equirectangular'
        elif params['method'].lower() not in Hemisphere.__projection_methods:
            raise ValueError('method given to projection not recognized: %s' % params['method'])
        # Finally, we need to look at exclusions...
        # (#TODO)
        return params
    @staticmethod
    def __select_projection_subset(mesh, center, radius):
        # Figure out which vertices and faces to include, yield the indices of each
        # use the spherical coordinates...
        center = np.asarray(center)
        sc = mesh.spherical_coordinates
        center_sc = [np.arctan2(center[0], center[1]),
                     np.arcsin(center[2] / np.sqrt(sum(center ** 2)))]
        return mesh.select(lambda u: spherical_distance(center_sc, sc[0:2,u]) < radius)
    def projection(self, **params):
        params = self.__interpret_projection_params(params)
        submesh = Hemisphere.__select_projection_subset(
            params['mesh'],
            params['center'],
            params['radius'])
        params['sphere_radius'] = np.mean(np.sqrt((submesh.coordinates ** 2).sum(0)))
        FR = geo.alignment_matrix_3D(params['center'], [1.0, 0.0, 0.0])
        IR = geo.alignment_matrix_3D([1.0, 0.0, 0.0], params['center'])
        fwdprojfn = Hemisphere.__projection_methods[params['method']]
        invprojfn = Hemisphere.__projection_methods_inverse[params['method']]
        fwdfn = lambda X,p: fwdprojfn(np.dot(FR, X), p)
        invfn = lambda X,p: np.dot(IR, invprojfn(X, p))
        params['forward_function'] = fwdfn
        params['inverse_function'] = invfn
        params = make_dict(params)
        submesh.coordinates = fwdfn(submesh.coordinates, params)
        submesh.options = submesh.options.using(projection_parameters=params)
        for p in self.property_names():
            try:
                submesh.prop(p, np.asarray(self.prop(p))[submesh.vertex_labels])
            except:
                pass
        return submesh

class Subject:
    '''FreeSurfer.Subject objects encapsulate the data contained in a FreeSurfer
       subject directory.'''

    ################################################################################################
    # Lazy/Static Interface
    # This code handles the lazy interface; only three data are non-lazy and these are coordinates,
    # faces, and options; they may be set directly.

    # The following methods and static variable allow one to set particular members of the object
    # directly:
    @staticmethod
    def _check_options(self, val):
        # Options just have to be a dictionary and are converted to an immutable one
        if not isinstance(val, dict):
            raise ValueError('options must be a dictionary')
        if type(val) is pysistence.persistent_dict.PDict:
            return val
        else:
            return make_dict(**val)
    __settable_members = {
        'options': lambda m,v: Subject._check_options(m,v)}

    # This static variable and these functions explain the dependency hierarchy in cached data
    @staticmethod
    def _check_meta_data(opts):
        md = opts.get('meta_data', {})
        if not isinstance(md, dict):
            raise ValueError('subject meta-data must be a dictionary')
        if type(md) is pysistence.persistent_dict.PDict:
            return md
        else:
            return make_dict(**md)
    def _load_hemisphere(self, name):
        return Hemisphere(self, name)
    __lazy_members = {
        'meta_data': (('options',), lambda mesh,opts: Subject._check_meta_data(opts)),
        'LH':  ((), lambda mesh: mesh._load_hemisphere('LH')),
        'RH':  ((), lambda mesh: mesh._load_hemisphere('RH')),
        'LHX': ((), lambda mesh: mesh._load_hemisphere('LHX')),
        'RHX': ((), lambda mesh: mesh._load_hemisphere('RHX'))}
    
    # This function will clear the lazily-evaluated members when a given value is changed
    def __update_values(self, name):
        for (sname, (deps, fn)) in Subject.__lazy_members.items():
            if name in deps and sname in self.__dict__:
                del self.__dict__[sname]

    # This is the most important function, given the encapsulation of this class:
    def __setattr__(self, name, val):
        if name in Subject.__settable_members:
            fn = Subject.__settable_members[name]
            self.__dict__[name] = fn(self, val)
            self.__update_values(name)
        elif name in Subject.__lazy_members:
            raise ValueError('The member %s is a lazy value and cannot be set' % name)
        else:
            raise ValueError('Unrecognized Subject member: %s' % name)

    # The getattr method makes sure that lazy members are computed when requested
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in Subject.__lazy_members:
            (deps, fn) = Subject.__lazy_members[name]
            tmp = fn(self, *map(lambda x: getattr(self, x), deps))
            self.__dict__[name] = tmp
            return tmp
        else:
            raise ValueError('Unrecognized member of Subject: %s' % name)

    
    ################################################################################################
    # The Constructor
    def __init__(self, subject, **args):
        (dir, name) = os.path.split(subject)
        if not os.path.isdir(subject):
            if dir is '':
                dir = args.pop('subjects_dir', os.environ['SUBJECTS_DIR'])
        elif dir is '':
            dir = '.'
        subpath = os.path.join(dir, name)
        if not os.path.isdir(subpath):
            raise ValueError('Subject directory not found: %s' % subpath)
        if not os.path.isdir(os.path.join(subpath, 'surf')):
            raise ValueError('Subject surf directory not found')
        self.__dict__['subjects_dir'] = dir
        self.__dict__['id'] = name
        self.__dict__['directory'] = subpath
        self.options = args
    
    ################################################################################################
    # The display function
    def __repr__(self):
        return "Subject(" + self.id + ")"


    ################################################################################################
    # Standard Methods

    def surface_path(self, type, hemi):
        hemi = hemi.upper()
        if hemi == 'RHX':
            if not os.path.isdir(os.path.join(self.directory, 'xhemi', 'surf')):
                raise ValueError('Subject does not have an xhemi/surf directory')
            path = os.path.join(self.directory, 'xhemi', 'surf', 'lh.' + type)
        elif hemi == 'LHX':
            if not os.path.isdir(os.path.join(self.directory, 'xhemi', 'surf')):
                raise ValueError('Subject does not have an xhemi/surf directory')
            path = os.path.join(self.directory, 'xhemi', 'surf', 'rh.' + type)
        elif hemi == 'LH':
            path = os.path.join(self.directory, 'surf', 'lh.' + type)
        elif hemi == 'RH':
            path = os.path.join(self.directory, 'surf', 'rh.' + type)
        else:
            raise ValueError('Argument hemi must be LH, RH, LHX, or RHX')
        if not os.path.isfile(path):
            raise ValueError('file %s not found' % path)
        return path
    def volume_path(self, type, hemi):
        # hemi may be None, in which case we have only these surfaces:
        if hemi is None:
            nm = type + '.'
        else:
            nm = hemi.lower() + '.' + type + '.'
        flnm = os.path.join(self.directory, 'mri', nm + 'mgz')
        if not os.path.isfile(flnm):
            flnm = os.path.join(self.directory, 'mri', nm + 'mgh')
            if not os.path.isfile(flnm):
                raise ValueError('no such file (or mgz equivalent) found: ' + flnm)
        return flnm
            

####################################################################################################
# Some FreeSurfer specific functions

def cortex_to_ribbon_map_smooth(sub, hemi=None, k=12, distance=4, sigma=0.35355):
    '''cortex_to_ribbon_map_smooth(sub) yields a dictionary whose keys are the indices of the ribbon
         voxels for the given FreeSurfer subject sub and whose values are a tuple of both (0) a list
         of vertex labels associated with the given voxel and (1) a list of the weights associated
         with each vertex (both in identical order).

       These associations are determined by finding the k nearest neighbors (of the midgray surface)
       to each voxel then finding the lines from white-to-pial that pass within a certain distance
       of the voxel center and weighting each appropriately.

       The following options are accepted:
         * k (default: 4) is the number of vertices to find near each voxel center
         * distance (default: 3) is the cutoff for including a vertex in a voxel region
         * hemi (default: None) specifies which hemisphere to operate over; this may be 'lh', 'rh',
           or None (to do both)
         * sigma (default: 1 / (2 sqrt(2))) specifies the standard deviation of the Gaussian used
           to weight the vertices contributing to a voxel'''
    
    # we can speed things up slightly by doing left and right hemispheres separately
    if hemi is None:
        return (cortex_to_ribbon_map(sub, k=k, distance=distance, sigma=sigma, hemi='lh'),
                cortex_to_ribbon_map(sub, k=k, distance=distance, sigma=sigma, hemi='rh'))
    if not isinstance(hemi, basestring):
        raise ValueError('hemi must be a string \'lh\', \'rh\', or None')
    if hemi.lower() == 'lh' or hemi.lower() == 'left':
        hemi = sub.LH
    elif hemi.lower() == 'rh' or hemi.lower() == 'right':
        hemi = sub.RH

    # first we find the indices of all voxels that are in the ribbon
    ribdat = hemi.ribbon.get_data()
    idcs = np.transpose(ribdat.nonzero()) + 1  # voxel transforms assume 1-based indexing
    # we also need the transformation from surface to voxel
    #tmtx = hemi.ribbon.header.get_ras2vox()
    tmtx = np.linalg.inv(hemi.ribbon.header.get_vox2ras_tkr())

    # now we want to make an octree from the midgray voxels
    txcoord = lambda mtx: np.dot(tmtx[0:3], np.vstack((mtx, np.ones(mtx.shape[1]))))
    midgray = txcoord(hemi.midgray_surface.coordinates)
    near = space.KDTree(midgray.T)
    
    # then we find the k nearest vertices for each voxel with a distance cutoff
    (d, nei) = near.query(idcs, k=k, distance_upper_bound=distance, p=2)
    ## we want the i'th row of d and nei to be a list of the i'th-nearests to each voxel center
    d = d.T
    nei = nei.T
    
    # okay, now we want to find the closest point along each line segment... we do this iteratively;
    # in the process we replace the d array with the distance of the nearest point along the segment
    # between pial and white for the given vertex. Any inf value will be left alone and will become
    # a zero when run through exp

    ## grab the pial and white matter coordinates...
    pialX = txcoord(hemi.pial_surface.coordinates)
    whiteX = txcoord(hemi.white_surface.coordinates)
    pial2white = whiteX - pialX
    pial2white_norm = np.sqrt(np.sum(pial2white ** 2, 0))
    same_idcs = np.where(pial2white_norm < 1e-9)
    pial2white_norm[same_idcs] = 1
    pial2white[:, same_idcs] = 0
    pial2white_normed = pial2white / pial2white_norm
    ## At this point we also want a transpose of indices
    idcs = idcs.T
    ## Iterate over the neighbors
    for i in range(d.shape[0]):
        # which elements are finite? (which do we care about)
        (finite_vox_idcs,) = np.where(d[i] != np.inf)
        # we do a closest-point search along the segment from white to pial in these locations
        ## to start, we project out the normal
        finite_vtx_idcs = nei[i, finite_vox_idcs]
        finite_vox_inplane = idcs[:, finite_vox_idcs] - pialX[:, finite_vtx_idcs]
        finite_p2w_normed = pial2white_normed[:, finite_vtx_idcs]
        finite_vox_prods = np.sum(finite_vox_inplane * finite_p2w_normed, 0)
        finite_vox_ipnorm = np.sqrt(np.sum(finite_vox_inplane ** 2, 0))
        ## If the product is less than 0, that means the voxel center is outside of the pial surface
        (inval,) = np.where((finite_vox_prods < -0.1 * finite_vox_ipnorm) \
                                + (finite_vox_prods > 1.1 * finite_vox_ipnorm))
        if len(inval) > 0:
            # annotate that these are invalid globally
            d[i, finite_vox_idcs[inval]] = np.inf
            # and locally
            finite_vox_idcs = np.delete(finite_vox_idcs, inval)
            finite_vox_inplane = np.delete(finite_vox_inplane, inval, 1)
            finite_p2w_normed = np.delete(finite_p2w_normed, inval, 1)
            finite_vox_prods = np.delete(finite_vox_prods, inval)
        ## otherwise, find the distance along the plane to the voxel center...
        finite_vox_inplane -= finite_p2w_normed * finite_vox_prods
        ## the distance to the line is just the norm of this then
        mindist2s = np.sum(finite_vox_inplane ** 2, 0)
        # We now have the in-plane distances to the closest vertices; we can just save this
        d[i, finite_vox_idcs] = mindist2s
    ## At this point we've filled the d-values (those not infinite) to the in-plane squared-
    ## distances from the relevant voxel center to the surface segment; we can turn d into weights;
    ## all infinite distances will automatically get a weight of 0
    d = np.exp(-0.5 * d / (sigma * sigma))
    ## we want to divide weights by the total weight so that all weight columns add up to 1...
    wtot = np.sum(d, 0)
    ### we have to check if any of these values are 0 and give them a nearest-vertex assignment
    zero_idcs = np.where(wtot < 1e-9)
    if len(zero_idcs) > 0:
        (d0s, nei0s) = near.query(idcs.T[zero_idcs], k=1, p=2)
        nei[0, zero_idcs] = nei0s
        d[0, zero_idcs] = 1.0
        d[1:, zero_idcs] = 0.0
        wtot[zero_idcs] = 1.0
    ### okay, now divide
    d /= wtot
    
    # With d = weights and nei = indices, we can now build the dictionary
    vlab = np.array(hemi.white_surface.vertex_labels)
    res = {}
    for i in range(idcs.shape[1]):
        (wh,) = np.where(d[:,i] > 0)
        res[tuple(idcs[:,i].tolist())] = (
            vlab[nei[wh, i]].tolist(),
            d[wh, i].tolist())
    return res

def _line_voxel_overlap(vx, xs, xe):
    '''
    _line_voxel_overlap((i,j,k), xs, xe) yields the fraction of the vector from xs to xe that
      overlaps with the voxel (i,j,k); i.e., the voxel that starts at (i,j,k) and ends at
      (i,j,k) + 1.
    '''
    # We want to consider the line segment from smaller to larger coordinate:
    seg = [(x0,x1) if x0 <= x1 else (x1,x0) for (x0,x1) in zip(xs,xe)]
    # First, figure out intersections of start and end values
    isect = [(min(seg_end, vox_end), max(seg_start, vox_start))
             if seg_end >= vox_start and seg_start <= vox_end
             else None
             for ((seg_start, seg_end), (vox_start, vox_end)) in zip(seg, [(x,x+1) for x in vx])]
    # If any of these are None, we can't possibly overlap
    if None in isect or any(a == b for (a,b) in isect):
        return 0.0
    return np.linalg.norm([e - s for (s,e) in isect]) / np.linalg.norm([e - s for (s,e) in zip(xs,xe)])

def cortex_to_ribbon_map_lines(sub, hemi=None):
    '''
    cortex_to_ribbon_map_lines(sub) yields a dictionary whose keys are the indices of the ribbon 
      voxels for the given FreeSurfer subject sub and whose values are a tuple of both (0) a list of
      vertex labels associated with the given voxel and (1) a list of the weights associated with
      each vertex (both in identical order).

    These associations are determined by projecting the vectors from the white surface vertices to 
      the pial surface vertices into the the ribbon and weighting them by the fraction of the vector 
      that lies in the voxel.

    The following options are accepted:
      * hemi (default: None) specifies which hemisphere to operate over; this may be 'lh', 'rh', or
        None (to do both)
    '''
    
    # we can speed things up slightly by doing left and right hemispheres separately
    if hemi is None:
        return (cortex_to_ribbon_map_lines(sub, hemi='lh'),
                cortex_to_ribbon_map_lines(sub, hemi='rh'))
    if not isinstance(hemi, basestring):
        raise ValueError('hemi must be a string \'lh\', \'rh\', or None')
    if hemi.lower() == 'lh' or hemi.lower() == 'left':
        hemi = sub.LH
    elif hemi.lower() == 'rh' or hemi.lower() == 'right':
        hemi = sub.RH
    else:
        raise RuntimeError('Unrecognized hemisphere: ' + hemi)

    # first we find the indices of all voxels that are in the ribbon
    ribdat = hemi.ribbon.get_data()
    # 1-based indexing is assumed:
    idcs = map(tuple, np.transpose(ribdat.nonzero()) + 1)
    # we also need the transformation from surface to voxel
    tmtx = np.linalg.inv(hemi.ribbon.header.get_vox2ras_tkr())
    # given that the voxels assume 1-based indexing, this means that the center of each voxel is at
    # (i,j,k) for integer (i,j,k) > 0; we want the voxels to start and end at integer values with 
    # respect to the vertex positions, so we subtract 1/2 from the vertex positions, which should
    # make the range 0-1, for example, cover the vertices in the first voxel
    txcoord = lambda mtx: np.dot(tmtx[0:3], np.vstack((mtx, np.ones(mtx.shape[1])))) + 1.5

    # Okay; get the transformed coordinates for white and pial surfaces:
    pialX = txcoord(hemi.pial_surface.coordinates)
    whiteX = txcoord(hemi.white_surface.coordinates)
    
    # make a list of voxels through which each vector passes:
    min_idx = [min(i) for i in idcs]
    max_idx = [max(i) for i in idcs]
    vtx_voxels = [((i,j,k), (id, olap))
                  for (id, (xs, xe)) in enumerate(zip(whiteX.T, pialX.T))
                  for i in range(int(math.floor(min(xs[0], xe[0]))), int(math.ceil(max(xs[0], xe[0]))))
                  for j in range(int(math.floor(min(xs[1], xe[1]))), int(math.ceil(max(xs[1], xe[1]))))
                  for k in range(int(math.floor(min(xs[2], xe[2]))), int(math.ceil(max(xs[2], xe[2]))))
                  for olap in [_line_voxel_overlap((i,j,k), xs, xe)]
                  if olap > 0]
    
    # and accumulate these lists... first group by voxel index then sum across these
    first_fn = lambda x: x[0]
    vox_byidx = {
        vox: ([q[0] for q in dat], [q[1] for q in dat])
        for (vox,xdat) in itertools.groupby(sorted(vtx_voxels, key=first_fn), key=first_fn)
        for dat in [[q[1] for q in xdat]]}
    return {
        idx: (ids, np.array(olaps) / np.sum(olaps))
        for idx in idcs
        if idx in vox_byidx
        for (ids, olaps) in [vox_byidx[idx]]}

def cortex_to_ribbon_map(sub, hemi=None, method='lines', options={}):
    '''
    cortex_to_ribbon_map(sub) yields a dictionary whose keys are the indices of the ribbon voxels
      for the given FreeSurfer subject sub and whose values are a tuple of both (0) a list of vertex
      labels associated with the given voxel and (1) a list of the weights associated with each
      vertex (both in identical order).

    The following options may be given:
      * hemi (default: None) may be 'lh', 'rh', or None; if Nonem then the result is a tuple of the
        (LH_dict, RH_dict) where LH_dict and RH_dict are the individual results from calling the
        cortex_to_ribbon_map function with hemi set to 'lh' or 'rh', respectively
      * method (default: 'lines') may be 'lines' or 'smooth'; the lines method projects the line
        segments from the white to the pial into the volume and weights each voxel by the length of
        the line segments contained in them; the smooth method uses Gaussian weights based on
        distance of the nearby vertices to the voxel center; see cortex_to_ribbon_map_lines and
        cortex_to_ribbon_map_smooth for more details.
      * options (default: {}) may be set to a dictionary of options to pass along to the lines or
        smooth functions
    '''
    if method.lower() == 'lines':
        return cortex_to_ribbon_map_lines(sub, hemi=hemi, **options)
    elif method.lower() == 'smooth':
        return cortex_to_ribbon_map_smooth(sub, hemi=hemi, **options)
    else:
        raise RuntimeError('Unrecognized method: ' + str(method))


def _cortex_to_ribbon_map_into_volume_array(vol, m, dat):
    dat = np.array(dat)
    for k,v in m.items():
        vol[k[0]-1, k[1]-1, k[2]-1] = np.dot(dat[v[0]], v[1])
    return vol

def cortex_to_ribbon(sub, data, map=None, k=12, distance=6, hemi=None, sigma=0.35355, 
                     default=0, dtype=np.float32):
    '''cortex_to_ribbon(sub, data, args...) applies the cortical-surface to ribbon transformation
         that is represented by the result of cortex_to_ribbon_map(sub, args...). The option 'map'
         may also be given if the cortex_to_ribbon_map calls have already been made, and the option
         'default' may be used to specify what value non-ribbon voxels will take.'''
    hemi = hemi.lower() if isinstance(hemi, basestring) else hemi
    if map is None:
        map = cortex_to_ribbon_map(sub, k=k, distance=distance, hemi=hemi, sigma=sigma)
    if hemi is None:
        if not isinstance(map, tuple) or len(map) != 2:
            raise ValueError('map must match hemi argument')
        if not isinstance(data, tuple) or len(data) != 2:
            raise ValueError('data must match hemi argument')
    if not isinstance(map, tuple):
        map = (map, None) if hemi == 'lh' else (None, map)
    if not isinstance(data, tuple):
        data = (data, None) if hemi == 'lh' else (None, data)
    # start with a duplicate of the left ribbon data
    vol0 = sub.LH.ribbon if hemi is None or hemi == 'lh' else sub.RH.ribbon
    vol0dims = vol0.get_data().shape
    arr = default * np.ones(vol0dims) if default != 0 else np.zeros(vol0dims)
    # apply the surface data maps to the volume
    if hemi is None or hemi == 'lh':
        arr = _cortex_to_ribbon_map_into_volume_array(arr, map[0], data[0])
    if hemi is None or hemi == 'rh':
        arr = _cortex_to_ribbon_map_into_volume_array(arr, map[1], data[1])
    hdr = vol0.header.copy()
    hdr.set_data_dtype(dtype)
    return fsmgh.MGHImage(arr, vol0.affine, hdr, vol0.extra, vol0.file_map)
    
    
    
    
    
