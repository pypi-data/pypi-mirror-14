import json
import imp
import importlib
import requests

def load_module_frm_file(filepath):
  try:
    return imp.load_source('callback_module', filepath)
  except Exception as exception:
    raise Exception('Failed to load module: %s %s' % (filepath, exception))

def load_module_by_name(modname):
  try:
    return importlib.import_module(modname)
  except Exception as exception:
    raise Exception('Failed to load module: %s: %s' % (modname, exception))

def load_json_frm_url(**kwargs):
  url = '%s://%s' % (kwargs['protocol'], kwargs['host'])
  if kwargs['port']:
    url += ':%d' % kwargs['port']
  url += kwargs['uri']
  return requests.get(url, verify=False).json()

def load_json_frm_str(jsonstr):
  try:
    return json.loads(jsonstr)
  except Exception as exception:
    raise Exception('Failed to load json string: %s: %s' % (jsonstr, exception))

def load_json_frm_file(filepath, **kwargs):
  return json.loads(open(filepath).read())

def flatten_ds(data_struct, key="", path="", flattened=None):
  """ Flatten a nested data structure """
  if flattened is None:
    flattened = {}
  if type(data_struct) not in(dict, list):
    flattened[((path + ".") if path else "") + key] = data_struct
  elif isinstance(data_struct, list):
    for i, item in enumerate(data_struct):
      flatten_ds(item, "%d" % i, (path + '.' + key if path else key),
                 flattened)
  else:
    for new_key, value in data_struct.items():
      flatten_ds(value, new_key, (path + '.' + key if path else key),
                 flattened)
  return flattened
