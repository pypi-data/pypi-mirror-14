#!/usr/bin/env python

from voluptuous import Optional, Required

class Config(object):
  SCHEMA = {
      Required('host'): str,
      Required('fabric_user'): str,
      Required('fabric_password'): str,
      Required('user'): str,
      Required('password'): str,
      Required('global_group'): str,
      Required('shard_groups'): list,
      Optional('port'): int,
      Optional('database_name'): str,
      Optional('timeout'): int,
      Optional('poolsize'): int,
      Optional('bulkquantity'): int,
      Optional('attempts'): int
  }
