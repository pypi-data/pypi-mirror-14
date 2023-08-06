#!/usr/bin/env python

from voluptuous import Optional, Required

class Config(object):
  SCHEMA = {
      Required('user'): str,
      Required('password'): str,
      Required('database'): str,
      Optional('host'): str,
      Optional('use_ssl'): bool,
      Optional('timeout'): str,
      Optional('ssl_ca'): str,
      Optional('ssl_cert'): str,
      Optional('ssl_key'): str,
      Optional('compress'): bool,
      Optional('port'): int,
    }
