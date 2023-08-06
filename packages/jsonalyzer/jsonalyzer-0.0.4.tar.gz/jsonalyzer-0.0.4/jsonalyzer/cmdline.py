#!/usr/bin/env python
""" json analyzer """

# TODO
# - release first cut pip
# - decouple worker from output printer
# - allow user to specify url directly
# - add support for flattened keys
# - add support to dump specific headers 
# - add key ==, >=, <=, >, < value callback
# - update README with examples and TODO
# - add nports - revisit output format

import os
import json
import click

from jsonalyzer import defaults
from jsonalyzer import utils

def _load_callback(ctx, param, value):
  """ Load jsonalzyer callback """
  if value is None:
    return value

  module_src, callback_func = value.strip().split(':')

  mod = None
  try:
    if os.path.exists(module_src):
      mod = utils.load_module_frm_file(module_src)
    else:
      mod = utils.load_module_by_name(module_src)
    return getattr(mod, callback_func)
  except Exception as load_callback_exception:
    raise click.BadParameter(str(load_callback_exception))

def _load_json_frm_str(ctx, param, value):
  """ Load json from string """
  if value is None:
    return value
  try:
    return utils.load_json_frm_str(value)
  except Exception as exception:
    raise click.BadParameter(str(exception))

def validate_protocol(ctx, param, value):
  """ Validate web command's argument - protocol """
  if value not in defaults.VALID_PROTOCOLS:
    raise click.BadParameter('%s: Valid values:' % defaults.VALID_PROTOCOLS)
  return value

def output_printer(output):
  """ Common output printer """
  color = 'green'
  if 'color' in output:
    color = output['color']
  elif output['status'] != 'OK':
    if output['status'] == 'WARNING':
      color = 'yellow'
    else:
      color = 'red'

  click.echo(click.style(output['msg'], fg=color))
  print json.dumps(output['ds'], indent=2)
  return True

def common_worker(loader, **kwargs):
  """ Common worker - load the json, run the callback on it """
  try:
    json_ds = loader(**kwargs)
    if kwargs['flatten']:
      json_ds = utils.flatten_ds(json_ds)
  except Exception as exception:
    click.echo(click.style('ERROR: Failed to load json. Dumping parameters', 
                           fg='red'))
    # stringify the functions otherwise as json can't encode them
    for key in ['callback', 'output_printer']:
      kwargs[key] = str(kwargs[key])
    click.echo(json.dumps(kwargs, indent=2))
    return 1

  output = kwargs['callback'](json_ds, **kwargs)
  kwargs['output_printer'](output)

  if output['status'] == 'OK':
    return 0

  if output['status'] == 'WARNING':
    return 1

  return 2

@click.group()
@click.option('--verbose/--no-verbose', help='verbose mode',
              default=False)
@click.pass_context
def jsonalyzer(ctx, **kwargs):
  """ Top level command for jsonalyzer """
  if ctx.obj is None:
    ctx.obj = {}
  for k in kwargs:
    ctx.obj[k] = kwargs[k]
  ctx.obj['output_printer'] = output_printer

@jsonalyzer.command('web')
@click.argument('PROTOCOL', callback=validate_protocol)
@click.option('-H', '--host', help='host. Default: %s' % defaults.HOST,
              default=defaults.HOST)
@click.option('--uri', help='uri. Default: %s' % defaults.URI,
              default=defaults.URI)
@click.option('--port', help='url port',
              type=click.IntRange(min=1, max=65535),
              default=None)
@click.option('--timeout', help='connection timeout. ' +
              'Default: %d' % defaults.CONN_TIMEOUT,
              default=defaults.CONN_TIMEOUT)
@click.option('--username', help='username',
              default=None)
@click.option('--password', help='password',
              default=defaults.URI)
@click.option('--headers',
              help='comma separated HTTP headers to dump in output',
              default=None)
@click.option('--callback',
              help='callback to act upon json. filepath:func or module_name:func',
              callback=_load_callback,
              default=defaults.CALLBACK)
@click.option('--params', help='stringified json to pass to callback',
              callback=_load_json_frm_str,
              default=None)
@click.option('--flatten/--no-flatten', help='flatten ds',
              default=False)
@click.pass_context
def load_from_web(ctx, **kwargs):
  """ 
  web http|https [options]
  """
  kwargs.update(ctx.obj)
  ctx.exit(common_worker(utils.load_json_frm_url, **kwargs))
  
@jsonalyzer.command('file')
@click.argument('FILE', type=click.Path(exists=True))
@click.option('--callback',
              help='callback to act upon json. filepath:func or module_name:func',
              callback=_load_callback,
              default=defaults.CALLBACK)
@click.option('--params', help='stringified json to pass to callback',
              callback=_load_json_frm_str,
              default=None)
@click.option('--flatten/--no-flatten', help='flatten ds',
              default=False)
@click.pass_context
def load_from_file(ctx, **kwargs):
  """ 
  file filepath [options]
  """
  kwargs.update(ctx.obj)
  ctx.exit(common_worker(utils.load_json_frm_file, **kwargs))

if __name__ == '__main__':
  jsonalyzer(obj={})
