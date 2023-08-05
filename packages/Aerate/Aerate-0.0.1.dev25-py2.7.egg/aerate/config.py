# -*- coding: utf-8 -*-
"""
    aerate.config
    ~~~~~~~~~~~~~
    Creates a Config object that is used across the Aerate inferface. An
    instance of this object is inserted on creation of an app.
    :copyright: (c) 2016 by Arable Labs, Inc.
    :license: BSD, see LICENSE for more details.
"""
import aerate
import os
import types
import errno


class Config(object):
    """ Helper class used through the code to access configuration settings.
    Before the main API object is instantiated, returns the default
    settings in the aerate __init__.py module, otherwise returns the values set
    within the falconapp during initialization.
    """
    def __init__(self):
        self._config = {}

    def reset(self):
        self._config = {}

    # Do the right thing when we try to introspect this object.
    def keys(self):
        return self._config.keys()

    def get(self, key):
        if key in self._config:
            return self._config[key]
        else:
            return None

    def __getattr__(self, name):
        try:
            # Try to use a user-set value:
            return self._config[name]
        except:
            # fallback to the module-level default value
            return getattr(aerate, name)

    def set(self, key, val):
        self._config[key] = val

    def from_object(self, obj):
        """Updates the values from the given object.  An object must be an
        actual object reference: that object is used directly.
        Objects are usually either modules or classes.
        Just the uppercase variables in that object are stored in the config.
        Example usage::
            app.config.from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config.from_object(default_config)
        You should not use this function to load the actual configuration but
        rather configuration defaults.
        :param obj: an import name or object
        """
        for key in dir(obj):
            if key.isupper():
                self._config[key] = getattr(obj, key)

    def from_pyfile(self, filename, silent=False):
        """Updates the values in the config from a Python file.  This function
        behaves as if the file was imported as module with the
        :meth:`from_object` function.
        :param filename: the filename of the config. This must be an absolute
                         filename.
        :param silent: set to ``True`` if you want silent failure for missing
                       files.
        """
        filename = os.path.join(filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename) as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

config = Config()
