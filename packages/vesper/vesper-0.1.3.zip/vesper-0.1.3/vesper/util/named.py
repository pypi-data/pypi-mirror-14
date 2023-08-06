"""
Module containing `Named` class.

A `Named` object is just an object with a name.
"""


class Named(object):
    
    """Named object."""
    
    
    def __init__(self, name):
        self._name = name
        
        
    @property
    def name(self):
        return self._name
