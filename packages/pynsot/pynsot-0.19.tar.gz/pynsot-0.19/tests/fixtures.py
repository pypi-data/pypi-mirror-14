#!/usr/bin/env python

"""
Make dummy data and fixtures and stuff.
"""

import collections
import json
import logging
import netaddr
import pytest
import random
import socket
import struct
from pynsot import client
try:
    import faker
except ImportError:
    print "The 'fake-factory' module is required! (Hint: pip install fake-factory)"
    raise

from . import util


log = logging.getLogger(__name__)

# Constants and stuff
fake = faker.Factory.create()

# API URL to use for testing.
API_URL = 'http://localhost:8990/api'


#############
# Responses #
#############
# API responses that we're using for request/resposne mocking.
# When authenticating against API
AUTH_RESPONSE = {
    'status':'ok',
    'data': {'auth_token': 'bogus_token'}
}

# When retrieving Sites.
SITES_RESPONSE = {u'data': {u'limit': None,
  u'offset': 0,
  u'sites': [{u'description': u'Production networks and devices.',
    u'id': 1,
    u'name': u'Production'}],
  u'total': 1},
 u'status': u'ok'}

SITES_LIMIT_RESPONSE = {
    "status": "ok",
    "data": {
        "total": 2,
        "limit": 1,
        "sites": [
            {
                "description": "Production networks, devices, and interfaces.",
                "id": 1,
                "name": "Production"
            }
        ],
        "offset": 0
    }
}

SITES_LIST_RESPONSE = {
    "status": "ok",
    "data": {
        "total": 2,
        "limit": None,
        "sites": [
            {
                "description": "Production networks, devices, and interfaces.",
                "id": 1,
                "name": "Production"
            },
            {
                "description": "Where bass is dropped.",
                "id": 2,
                "name": "Da Club"
            }
        ],
        "offset": 0
    }
}

# When retrieving Devices.
DEVICES_RESPONSE = {u'data': {u'devices': [
    {u'attributes': {'owner': 'jathan'}, u'hostname': u'foo-bar1', u'id': 1, u'site_id': 1},
    {u'attributes': {'owner': 'jathan'}, u'hostname': u'foo-bar2', u'id': 2, u'site_id': 1}
    ],
  u'limit': None,
  u'offset': 0,
  u'total': 2},
 u'status': u'ok'}

DEVICE_RETRIEVE = {u'data': {u'device': {u'attributes': {
   u'owner': u'jathan'},
   u'hostname': u'foo-bar1',
   u'id': 1,
   u'site_id': 1}},
 u'status': u'ok'}

DEVICE_UPDATE = {u'data': {u'device': {u'attributes': {u'monitored': u'',
   u'owner': u'jathan'},
   u'hostname': u'foo-bar1',
   u'id': 1,
   u'site_id': 1}},
 u'status': u'ok'}

DEVICE_HOSTNAME_RETRIEVE = {u'data': {u'devices': [{u'attributes': {
   u'owner': u'jathan'},
   u'hostname': u'foo-bar1',
   u'id': 1,
   u'site_id': 1}],
   'total': 1,
   'offset': 0,
   'limit': None,
   },
 u'status': u'ok'}


# Networks
NETWORK_CREATE = {'data': {'network': {'attributes': {'owner': 'jathan'},
   'id': 1,
   'ip_version': '4',
   'is_ip': False,
   'network_address': '10.0.0.0',
   'parent_id': None,
   'prefix_length': 8,
   'state': 'allocated',
   'site_id': 1}},
 'status': 'ok'}

NETWORK_RETRIEVE = {u'data': {u'network': {u'attributes': {u'owner': u'jathan'},
   u'id': 1,
   u'ip_version': u'4',
   u'is_ip': False,
   u'network_address': u'10.0.0.0',
   u'parent_id': None,
   u'prefix_length': 8,
   u'state': 'allocated',
   u'site_id': 1}},
 u'status': u'ok'}

NETWORK_UPDATE = {u'data': {u'network': {u'attributes': {u'foo': u'bar', u'owner': u'jathan'},
   u'id': 1,
   u'ip_version': u'4',
   u'is_ip': False,
   u'network_address': u'10.0.0.0',
   u'parent_id': None,
   u'prefix_length': 8,
   u'state': 'allocated',
   u'site_id': 1}},
 u'status': u'ok'}

NETWORKS_RESPONSE = {u'data': {u'limit': None,
  u'networks': [
   {u'attributes': {u'owner': u'jathan'},
    u'id': 1,
    u'ip_version': u'4',
    u'is_ip': False,
    u'network_address': u'10.0.0.0',
    u'parent_id': None,
    u'prefix_length': 8,
    u'state': 'allocated',
    u'site_id': 1},
   {u'attributes': {u'owner': u'jathan'},
    u'id': 2,
    u'ip_version': u'4',
    u'is_ip': False,
    u'network_address': u'10.0.0.0',
    u'parent_id': 1,
    u'prefix_length': 24,
    u'state': 'allocated',
    u'site_id': 1}],
  u'offset': 0,
  u'total': 2},
 u'status': u'ok'}

NETWORK_CIDR_RETRIEVE = {u'data':
  {u'networks': [{u'attributes': {u'owner': u'jathan'},
   u'id': 1,
   u'ip_version': u'4',
   u'is_ip': False,
   u'network_address': u'10.0.0.0',
   u'parent_id': None,
   u'prefix_length': 8,
   u'state': 'allocated',
   u'site_id': 1}],
   "total": 1,
   "limit": None,
   "offset": 0,
   },
 u'status': u'ok'}


# When retrieving Attributes.
ATTRIBUTE_CREATE = {u'data': {u'attribute': {u'constraints': {u'allow_empty': False,
    u'pattern': u'',
    u'valid_values': []},
   u'description': u'',
   u'display': False,
   u'id': 3,
   u'multi': True,
   u'name': u'multi',
   u'required': False,
   u'resource_name': u'Device',
   u'site_id': 1}},
 u'status': u'ok'}

ATTRIBUTES_RESPONSE = {u'data': {u'attributes': [{u'constraints': {u'allow_empty': True,
     u'pattern': u'',
     u'valid_values': []},
    u'description': u'',
    u'display': False,
    u'id': 2,
    u'multi': False,
    u'name': u'monitored',
    u'required': False,
    u'resource_name': u'Device',
    u'site_id': 1},
   {u'constraints': {u'allow_empty': False,
     u'pattern': u'',
     u'valid_values': []},
    u'description': u'',
    u'display': True,
    u'id': 1,
    u'multi': False,
    u'name': u'owner',
    u'required': False,
    u'resource_name': u'Device',
    u'site_id': 1},
   {u'constraints': {u'allow_empty': False,
    u'pattern': u'',
    u'valid_values': []},
   u'description': u'',
   u'display': False,
   u'id': 3,
   u'multi': True,
   u'name': u'multi',
   u'required': False,
   u'resource_name': u'Device',
   u'site_id': 1}],
  u'limit': None,
  u'offset': 0,
  u'total': 3},
 u'status': u'ok'}

ATTRIBUTES_NAME_RESPONSE = {u'data': {u'attributes': [{u'constraints': {u'allow_empty': True,
     u'pattern': u'',
     u'valid_values': []},
    u'description': u'',
    u'display': False,
    u'id': 2,
    u'multi': False,
    u'name': u'monitored',
    u'required': False,
    u'resource_name': u'Device',
    u'site_id': 1},],
  u'limit': None,
  u'offset': 0,
  u'total': 1},
 u'status': u'ok'}

ATTRIBUTES_ID_RESPONSE = {
    "status": "ok",
    "data": {
        "attribute": {
            "multi": False,
            "resource_name": "Device",
            "description": "",
            "display": False,
            "required": False,
            "site_id": 1,
            "id": 2,
            "constraints": {
                "pattern": "",
                "valid_values": [],
                "allow_empty": True
            },
            "name": "monitored"
        }
    }
}


# Dummy config data used for testing dotfile and client
CONFIG_DATA = {
    'email': 'jathan@localhost',
    'url': 'http://localhost:8990/api',
    'auth_method': 'auth_token',
    'secret_key': 'MJMOl9W7jqQK3h-quiUR-cSUeuyDRhbn2ca5E31sH_I=',
}


@pytest.fixture
def config():
    return CONFIG_DATA


# Payload used to create Network & Device attributes used for testing.
TEST_ATTRIBUTES = {
    'attributes': [
        {
            'name': 'cluster',
            'resource_name': 'Device',
            'description': 'Device cluster.',
            'constraints': {'allow_empty': True},
        },
        {
            'name': 'foo',
            'resource_name': 'Device',
            'description': 'Foo for Devices.',
        },
        {
            'name': 'owner',
            'resource_name': 'Device',
            'description': 'Device owner.',
        },
        {
            'name': 'cluster',
            'resource_name': 'Network',
            'description': 'Network cluster.',
            'constraints': {'allow_empty': True},
        },
        {
            'name': 'foo',
            'resource_name': 'Network',
            'description': 'Foo for Networks.',
        },
        {
            'name': 'owner',
            'resource_name': 'Network',
            'description': 'Network owner.',
        },
    ]
}

# Payload used to list Attribute values.
VALUES_RETRIEVE = {u'status': u'ok', u'data': {u'values': [{u'resource_name': u'Device', u'name': u'owner', u'resource_id': 26683, u'attribute': 83, u'value': u'jathan', u'id': 1780986}], u'total': 1, u'limit': None, u'offset': 0}}


# Changes
CHANGES_LIST_RESPONSE = {
    "status": "ok",
    "data": {
        "changes": [
            {
                "resource_name": "Device",
                "resource": {
                    "attributes": {
                        "owner": "john",
                        "monitor": "collected"
                    },
                    "hostname": "foo-bar3",
                    "site_id": 1,
                    "id": 26687
                },
                "resource_id": 26687,
                "site": {
                    "description": "Production networks, devices, and interfaces.",
                    "name": "Production",
                    "id": 1
                },
                "id": 266658,
                "change_at": 1455656717,
                "user": {
                    "id": 51,
                    "email": "admin@localhost"
                },
                "event": "Update"
            }
        ],
        "total": 1,
        "limit": None,
        "offset": 0
    }
}
