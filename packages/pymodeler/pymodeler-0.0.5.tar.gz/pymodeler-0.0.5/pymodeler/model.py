#!/usr/bin/env python
"""
A Model object is just a container for a set of Parameter.
Implements __getattr__ and __setattr__.

The model has a set of default parameters stored in Model._params. 
Careful, if these are changex, they will be changed for all 
subsequent instances of the Model.

The parameters for a given instance of a model are stored in the
Model.params attribute. This attribute is a deepcopy of 
Model._params created during instantiation.

"""
from collections import OrderedDict as odict
import numpy as np
import copy
import yaml

from pymodeler.parameter import Parameter

def indent(string,width=0): 
    return '{0:>{1}}{2}'.format('',width,string)

class Model(object):
    # `_params` is a tuple of parameters
    # _params = (('parameter name', 'default value', 'help description'),)
    _params = ()
    # `_mapping` is an alternative name mapping
    # for the parameters in _params
    _mapping = ()

    def __init__(self,*args,**kwargs):
        self.params = self.defaults
        self.set_attributes(**kwargs)
        #pars = dict(**kwargs)
        #for name, value in pars.items():
        #    # Raise AttributeError if attribute not found
        #    self.__getattr__(name) 
        #    # Set attribute
        #    self.__setattr__(name,value)
        
        # In case no properties were set, cache anyway
        self._cache()

    def __getattr__(self,name):
        # Return 'value' of parameters
        # __getattr__ tries the usual places first.
        #if name in self._mapping:
        #    return self.__getattr__(self._mapping[name])
        #if name in self._params:
        #    return self.getp(name).value
        #else:
        #    # Raises AttributeError
        #    return object.__getattribute__(self,name)
        if name in self.defaults or name in self.mappings:
            return self.getp(name).value
        else:
            # Raises AttributeError
            return object.__getattribute__(self,name)

    def __setattr__(self, name, value):
        ## Call 'set_value' on parameters
        ## __setattr__ tries the usual places first.
        #if name in self._mapping.keys():
        #    return self.__setattr__(self._mapping[name],value)
        #if name in self._params:
        #    self.setp(name, value)
        #else:
        #    return object.__setattr__(self, name, value)
        if name in self.defaults or name in self.mappings:
            self.setp(name, value)
        else:
            # Why is this a return statement
            return object.__setattr__(self, name, value)

    def __str__(self,indent=0):
        ret = '{0:>{2}}{1}'.format('',self.name,indent)
        if len(self.params)==0:
            pass
        else:            
            ret += '\n{0:>{2}}{1}'.format('','Parameters:',indent+2)
            width = len(max(self.params.keys(),key=len))
            for name,value in self.params.items():
                par = '{0!s:{width}} : {1!r}'.format(name,value,width=width)
                ret += '\n{0:>{2}}{1}'.format('',par,indent+4)
        return ret

    @property
    def defaults(self):
        """Ordered dictionary of default parameters."""
        # Deep copy is necessary so that default parameters remain unchanged
        return copy.deepcopy(odict([(p[0],p[1]) for p in self._params]))

    @property
    def mappings(self):
        """Ordered dictionary of mapping."""
        return odict(self._mapping)

    @property
    def name(self):
        return self.__class__.__name__

    def getp(self, name):
        """ 
        Get the named parameter.

        Parameters
        ----------
        name : string
            The parameter name.

        Returns
        -------
        param : 
            The parameter object.
        """
        name = self.mappings.get(name,name)
        return self.params[name]

    def setp(self, name, value=None, bounds=None, free=None, errors=None):
        """ 
        Set the value (and bounds) of the named parameter.

        Parameters
        ----------
        name : string
            The parameter name.
        value: 
            The value of the parameter
        bounds: None
            The bounds on the parameter
        Returns
        -------
        None
        """
        name = self.mappings.get(name,name)
        self.params[name].set(value,bounds,free,errors)
        self._cache(name)

    def set_attributes(self, **kwargs):
        """
        Set a group of attributes (parameters and members).  Calls
        `setp` directly, so kwargs can include more than just the
        parameter value (e.g., bounds, free, etc.).
        """
        kwargs = dict(kwargs)
        for name,value in kwargs.items():
            # Raise AttributeError if param not found
            self.__getattr__(name) 
            # Set attributes
            try: self.setp(name,**value)
            except TypeError:
                try:  self.setp(name,*value)
                except (TypeError,KeyError):  
                    self.__setattr__(name,value)
        
    def todict(self):
        ret = odict(name = self.__class__.__name__)
        ret.update(self.params)
        return ret

    def dump(self):
        return yaml.dump(self.todict())

    def _cache(self, name=None):
        """ 
        Method called in _setp to cache any computationally
        intensive properties after updating the parameters.

        Parameters
        ----------
        name : string
           The parameter name.

        Returns
        -------
        None
        """
        pass

        
if __name__ == "__main__":
    import argparse
    description = "python script"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('args',nargs=argparse.REMAINDER)
    opts = parser.parse_args(); args = opts.args
