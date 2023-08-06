#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file contains basic definitions and associated methods for
dclab.
"""
from __future__ import division, print_function

import codecs
import copy
import numpy as np
from pkg_resources import resource_filename  # @UnresolvedImport

__all__ = ["GetKnownIdentifiers", "LoadConfiguration", 
           "LoadDefaultConfiguration", "cfg",
           "MapParameterStr2Type",
           "MapParameterType2Str", "GetParameterChoices",
           "GetParameterDtype"]


def GetParameterChoices(key, subkey, ignore_axes=[]):
    """ Returns the choices for a parameter, if any
    """
    ## Manually defined types:
    choices = []
    
    if key == "Plotting":
        if subkey == "KDE":
            choices = ["Gauss", "Multivariate"]

        elif subkey in ["Axis X", "Axis Y"]:
            choices = copy.copy(uid)
            # remove unwanted axes
            for choice in ignore_axes:
                if choice in choices:
                    choices.remove(choice)
   
        elif subkey in ["Rows", "Columns"]:
            choices = [ unicode(i) for i in range(1,6) ]
        elif subkey in ["Scatter Marker Size"]:
            choices = [ unicode(i) for i in range(1,5) ]
    return choices


def GetParameterDtype(key, subkey, cfg=None):
    """ Returns dtype of the parameter as defined in dclab.cfg
    """
    #default
    dtype = str

    ## Define dtypes and choices of cfg content
    # Iterate through cfg to determine standard dtypes
    # (also use cfg_init).    
    if cfg is None:
        cfg = cfg_init
    
    if cfg_init.has_key(key) and cfg_init[key].has_key(subkey):
        dtype = cfg_init[key][subkey].__class__
    else:
        try:
            dtype = cfg[key][subkey].__class__
        except KeyError:
            dtype = float

    return dtype


def GetKnownIdentifiers():
    return uid
    
    
def LoadConfiguration(cfgfilename, cfg=None, capitalize=True):
    """ Load a configuration file
    
    
    Parameters
    ----------
    cfgfilename : absolute path
        Filename of the configuration
    cfg : dict
        Dictionary to update/overwrite. If `cfg` is not set, a new
        dicitonary will be created.
    capitalize : bool
        Capitalize dictionary entries. This is useful to
        prevent duplicate entries in configurations dictionaries
        like "Flow Rate" and "flow rate". It is not useful when
        dictionary entries are not capitalized, e.g. for other
        configuration files like index files of ShapeOut sessions.
        
    
    Returns
    -------
    cfg : dict
        Dictionary with configuration in librtdc format.
        
    
    Notes
    -----
    If a [General] section is loaded and if the keyword "Channel Width"
    is not defined and if the flow rate is >= 0.16µl/s, then we
    set the Channel Width to 30 µm.
    """
    if cfg is None:
        cfg = dict()
    
    with codecs.open(cfgfilename, 'r', 'utf-8') as f:
        code = f.readlines()
    
    for line in code:
        # We deal with comments and empty lines
        # We need to check line length first and then we look for
        # a hash.
        line = line.split("#")[0].strip()
        if len(line) != 0:
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]
                if not cfg.has_key(section):
                    cfg[section] = dict()
                continue
            var, val = line.split("=", 1)
            var,val = MapParameterStr2Type(var, val, capitalize=capitalize)
            if len(var) != 0 and len(unicode(val)) != 0:
                cfg[section][var] = val
    
    # 30µm channel?
    if ( cfg.has_key("General") and
         not cfg["General"].has_key("Channel Width") and
         cfg["General"].has_key("Flow Rate [ul/s]") and
         cfg["General"]["Flow Rate [ul/s]"] >= 0.16     ):
        cfg["General"]["Channel Width"] = 30
    
    return cfg


def LoadDefaultConfiguration():
    return LoadConfiguration(cfgfile)



def MapParameterStr2Type(var, val, capitalize=True):
    if not ( isinstance(val, str) or isinstance(val, unicode) ):
        # already a type:
        return var.strip(), val
    var = var.strip()
    val = val.strip()
    if capitalize:
        # capitalize var
        if len(var) != 0:
            varsubs = var.split()
            newvar = u""
            for vs in varsubs:
                newvar += vs[0].capitalize()+vs[1:]+" "
            var = newvar.strip()
    # Find values
    if len(var) != 0 and len(val) != 0:
        # check for float
        if val.startswith("[") and val.endswith("]"):
            if len(val.strip("[],")) == 0:
                # empty list
                values = []
            else:
                values = val.strip("[],").split(",")
                values = [float(v) for v in values]
            return var, values
        elif val.lower() in ["true", "y"]:
            return var, True
        elif val.lower() in ["false", "n"]:
            return var, False
        elif val[0] in ["'", '"'] and val[-1] in ["'", '"']:
            return var, val.strip("'").strip('"').strip()
        elif val in GetKnownIdentifiers():
            return var, val
        else:
            try:
                return var, float(val.replace(",","."))
            except ValueError:
                return var, val


def MapParameterType2Str(var,val):
    var = var.strip()
    if len(var) != 0:
        if isinstance(val, list):
            out = "["
            for item in val:
                out += "{}, ".format(item)
            out = out.strip(" ,") + "]"
            return var, out
        elif isinstance(val, bool):
            return var, str(val)
        elif isinstance(val, str):
            return var, "'{}'".format(val.strip())
        elif isinstance(val, int):
            return var, "{:d}".format(val)
        elif isinstance(val, float):
            return var, "{:.12f}".format(val)
        else:
            return var, str(val)


### Define Standard name maps
# Unique identifier (UID)
uid = [
        "AreaPix",
        "Area",
        "Area Ratio",
        "Aspect",
        "Circ",
        "Defo",
        "Frame",
        "Pos Lat",
        "Time",
        "FC0max",
        "FC0width",
        "FL-1max",
        "FL-1width",
        "FL-2max",
        "FL-2width",
        "FL-3max",
        "FL-3width",
       ]
# Axes label (same order as UID)
axl = [
        u"Cell Size [px²]",
        u"Cell Size [µm²]",
        u"Convex to Measured Area Ratio",
        u"Aspect Ratio of Bounding Box",
        u"Circularity",
        u"Deformation",
        u"Frame Number",
        u"Lateral Position in Channel [px]",
        u"Frame Time [s]",
        u"Fluorescence Intensity Maximum [ADC] (Ch.0)",
        u"Fluorescence Peak Width [µs]",
        u"FL-1 (green) Maximum [ADC]",
        u"FL-1 (green) width [us]",
        u"FL-2 (orange) Maximum [ADC]",
        u"FL-2 (orange) width [us]",
        u"FL-3 (red) Maximum [ADC]",
        u"FL-3 (red) width [us]",
       ]
# Unique RTDC_DataSet variable names (same order as UID)
rdv = [
        "area",
        "area_um",
        "area_ratio",
        "aspect",
        "circ",
        "deform",
        "frame",
        "pos_lat",
        "time",
        "fc0m",
        "fc0w",
        "fl1m",
        "fl1w",
        "fl2m",
        "fl2w",
        "fl3m",
        "fl3w",
       ]
# tdms file definitions (same order as UID)
# group, [names], lambda
# The order of [names] must be the same as the order of the arguments
# for lambda!
tfd = [
        # area -> area in pixels
        ["Cell Track",
         "area",
         lambda x: x
        ],
        # area_um (set by RTDC_DataSet)
        ["Cell Track",
         "area",
         lambda x: np.zeros(x.shape) # set to zero
         ],
        # area_ratio
        ["Cell Track",
         ["area", "raw area"],
         lambda area, area_raw: area/area_raw
         ],
        # aspect
        ["Cell Track",
         ["ax1", "ax2"], #(perpendicular to flow, parallel to flow)
         lambda ax1, ax2: ax2 / ax1
         ],
        # circ
        ["Cell Track",
         "circularity",
         lambda x: x
         ],
        # deform
        ["Cell Track",
         "circularity",
         lambda x: 1-x
         ],
        # frame
        ["Cell Track",
         "time",
         lambda x: x
        ],
        # pos_lat
        ["Cell Track",
         "y",
         lambda x: x
         ],
        # time (set by RTDC_DataSet)
        ["Cell Track",
         "time",
         lambda x: np.zeros(x.shape) # time in seconds
         ],
        # FC0 maxiumum channel
        ["Cell Track",
         "FC0_max",
         lambda x: x
        ],
        # FC0 width channel
        ["Cell Track",
         "FC0_width",
         lambda x: x
        ],
        # For 3-channel setup use FL-1 .. FL-3 annotation
        # FL-1 maximum of peak (green channel)
        ["Cell Track",
         "FL1max",
         lambda x: x
        ],
        # FL-1 width channel
        ["Cell Track",
         "FL1width",
         lambda x: x
        ],
        # FL-2 maximum of peak (orange channel)
        ["Cell Track",
         "FL2max",
         lambda x: x
        ],
        # FL-2 width channel
        ["Cell Track",
         "FL2width",
         lambda x: x
        ],
        # FL-3 maximum of peak (red channel)
        ["Cell Track",
         "FL3max",
         lambda x: x
        ],
        # FL-3 width channel
        ["Cell Track",
         "FL3width",
         lambda x: x
        ],
        ]


# mapping `Measuement` class attributes to configuration file names
cfgmap = dict()        # area_um -> Area
cfgmaprev = dict()     # Area -> area_um
axlabels = dict()      # Area -> Cell Size [µm²]
axlabelsrev = dict()   # Cell Size [µm²] -> Area

# here the name maps are defined
for _u,_a,_r in zip(uid, axl, rdv):
    cfgmap[_r] = _u
    cfgmaprev[_u] = _r
    axlabels[_u] = _a
    axlabelsrev[_a] = _u


### Load standard configuration
cfgfile = resource_filename(__name__, 'dclab.cfg')
cfg = LoadDefaultConfiguration()
cfg_init = copy.deepcopy(cfg)

