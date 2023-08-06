import string
import json

def get_output_template(json_ds):
  return {
    'ds': json_ds,
    'msg': '',
    'status': 'OK'
  }

def no_op(json_ds, **kwargs):
  output = get_output_template(json_ds)
  output['msg'] = 'OK'
  return output

def check_has_key(json_ds, **kwargs):

  output = get_output_template(json_ds)

  if 'params' not in kwargs:
    output['status'] = 'CRITICAL'
    output['msg'] = "ERROR: Did not pass --params"
    return output

  if 'key' not in kwargs['params']:
    output['status'] = 'CRITICAL'
    output['msg'] = "ERROR: Did not set \"key\" in --params"
    return output

  target_key = kwargs['params']['key']

  if target_key not in json_ds:
    output['msg'] = 'ERROR: Key %s not found' % target_key
    output['status'] = 'CRITICAL'
    return output

  output['msg'] = 'OK: Found key - %s = %s' % (target_key, json_ds[target_key])
  return output

def check_key_value(json_ds, **kwargs):

  output = check_has_key(json_ds, **kwargs)

  if output['status'] != 'OK':
    return output

  if 'value' not in kwargs['params']:
    output['status'] = 'CRITICAL'
    output['msg'] = "ERROR: Did not set \"value\" in --params"
    return output

  target_key = kwargs['params']['key']
  target_value = kwargs['params']['value']

  value = json_ds[target_key]
  if value != target_value:
    output['msg'] = 'ERROR: Key %s value == %s != %s' % (target_key, target_value,
                                                         value)
    output['status'] = 'CRITICAL'
    return output

  output['msg'] = 'OK: Found key - %s == %s' % (target_key, json_ds[target_key])
  return output

def check_key_value_limits(json_ds, **kwargs):
  output = check_has_key(json_ds, **kwargs)

  if output['status'] != 'OK':
    return output

  if 'warning' not in kwargs['params']:
    output['status'] = 'CRITICAL'
    output['msg'] = "ERROR: Did not set \"warning\" in --params"
    return output

  if 'critical' not in kwargs['params']:
    output['status'] = 'CRITICAL'
    output['msg'] = "ERROR: Did not set \"critical\" in --params"
    return output

  target_key = kwargs['params']['key']

  value = float(json_ds[target_key])
  warning = float(kwargs['params']['warning'])
  critical = float(kwargs['params']['critical'])

  if value >= critical:
    output['status'] = 'CRITICAL'
    output['msg'] = 'ERROR: %s = %.2f >= critical limit %.2f' % (target_key,
                                                                 value, critical)
  if value >= warning:
    output['status'] = 'WARNING'
    output['msg'] = 'ERROR: %s = %.2f >= warning limit %.2f' % (target_key, 
                                                                value, warning)
    return output

  output['msg'] = 'OK: %s = %.2f < %.2f' % (target_key, value, warning)
  return output
