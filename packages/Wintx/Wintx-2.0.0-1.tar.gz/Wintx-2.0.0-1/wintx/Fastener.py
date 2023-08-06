#!/usr/bin/env python
"""Wintx Fastener to connect interfaces to the drivers and handle configurations"""

import ConfigParser
import os
import pkg_resources

from errors import WintxConfigError, WintxDriverError, WintxFunctionNotImplemented

from voluptuous import MultipleInvalid, Invalid as SchemaInvalid
from voluptuous import All, Length, Required, Schema

class Fastener(object):
  """Glue class to redirect wintx.interfaces class methods to a Wintx Driver."""

  CONFIG_SCHEMA_MAIN = {
      Required('driver'): All(str, Length(min=1)),
  }

  def __init__(self, configfile='/etc/wintx.conf'):
    """Constructor for the Fastener class
    Input:
      configfile: string of the absolute path to the wintx configuration file
    """
    self.config_file = configfile
    self.config_instance = ConfigParser.ConfigParser()
    self.main_config = None
    self.driver_config = None
    self.driver = None

    def getDictFromConfig(config_instance, schema, section):
      """Obtains a schema validated dictionary with type converted values from a configuration instance.
         Input:
           config_instance: (ConfigParser) Instance of configuration file
           schema: (Schema) Prepared validation schema
           section: (str) Name of section in configuration file
         Returns:
           (dict) of validated key/value pairs from the given section in the configuration
      """
      if( not config_instance.has_section(section) ):
        raise WintxConfigError('There is no \'main\' section in the config file %s' % self.config_file)
      else:
        return_dict = {}
        for option in config_instance.options(section):
          try:
            return_dict[option] = eval(config_instance.get(section, option))
          except NameError:
            return_dict[option] = config_instance.get(section, option)

        try:
          return_dict = schema(return_dict)
        except MultipleInvalid as err:
          raise WintxConfigError('The section \'%s\' failed validation because the %s' % (section, str(err)))
        except SchemaInvalid as err:
          raise WintxConfigError('The section \'%s\' failed validation because the %s' % (section, str(err)))

        return return_dict

    if( os.path.exists(self.config_file) ):
      if( self.config_instance.read([self.config_file]) ):
        self.main_config = getDictFromConfig(self.config_instance, Schema(self.CONFIG_SCHEMA_MAIN), 'main')
      else:
        raise WintxConfigError('Could not read the config file %s' % self.config_file)
    else:
      raise WintxConfigError('The config file %s does not exist' % self.config_file)

    driver_static = None
    try:
      driver_static = __import__('wintx.drivers.%s' % self.main_config['driver'], fromlist=['wintx.drivers'])
      if( not issubclass(getattr(driver_static, 'Driver'), object) ):
        raise WintxDriverError('Driver %s not found' % self.main_config['driver'])
    except ImportError as err:
      raise WintxDriverError('Driver %s not found' % self.main_config['driver'])
    except AttributeError as err:
      raise WintxDriverError('Driver %s not found' % self.main_config['driver'])

    try:
      driver_config = getattr(driver_static, 'Config')
      if( not issubclass(driver_config, object) ):
        raise WintxDriverError('Driver %s has no configuration schema', self.main_config['driver'])
      if( type(getattr(driver_config, 'SCHEMA')) is not type({}) ):
        raise WintxDriverError('Driver %s has no configuration schema', self.main_config['driver'])
    except AttributeError as err:
      raise WintxDriverError('Driver %s has no configuration schema', self.main_config['driver'])

    if( self.config_instance.has_section(self.main_config['driver']) ):
      self.driver_config = getDictFromConfig(self.config_instance, Schema(driver_config.SCHEMA), self.main_config['driver'])
    else:
      raise WintxConfigError('Driver %s section not found' % self.main_config['driver'])

    self.driver = driver_static.Driver(**self.driver_config)

  def __getattr__(self, name):
    try:
      return getattr(self.driver, name)
    except AttributeError as err:
      raise WintxFunctionNotImplemented('Driver %s does not implement \'%s\'' % (self.main_config['driver'], name))

