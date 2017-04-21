# pylint: disable=redefined-outer-name
from __future__ import absolute_import

from custodia.compat import configparser
from custodia.plugin import CSStore, CSStoreError

import mock

import pkg_resources

import pytest

from custodiaexample.auth import ExampleAuth
from custodiaexample.authz import ExampleAuthz
from custodiaexample.store import ExampleStore


CONFIG = u"""
[store:otherstore]
handler = SqliteStore

[store:examplestore]
handler = ExampleStore
backing_store = otherstore

[auth:exampleauth]
handler = ExampleAuth
value = example

[authz:exampleauthz]
handler = ExampleAuthz
"""


@pytest.fixture
def parser():
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
    )
    parser.read_string(CONFIG)
    return parser


@pytest.fixture
def exampleauth(parser):
    return ExampleAuth(parser, 'auth:exampleauth')


@pytest.fixture
def exampleauthz(parser):
    return ExampleAuthz(parser, 'authz:exampleauthz')


@pytest.fixture
def examplestore(parser):
    backing_store = mock.create_autospec(CSStore)
    es = ExampleStore(parser, 'store:examplestore')
    es.store = backing_store
    return es


def test_auth_ok(exampleauth):
    request = {
        'headers': {'REMOTE_USER': 'example'},
        'client_id': 'test',
    }
    assert exampleauth.handle(request) is True
    assert request['remote_user'] == 'example'


def test_auth_fail(exampleauth):
    request = {
        'headers': {'REMOTE_USER': 'other'},
        'client_id': 'test',
    }
    assert exampleauth.handle(request) is False
    assert 'remote_user' not in request


def test_authz_ok(exampleauthz):
    request = {
        'path_chain': ['', 'secret', 'example', 'key'],
        'client_id': 'test',
    }
    assert exampleauthz.handle(request) is True


def test_authz_fail(exampleauthz):
    request = {
        'path_chain': ['', 'secret', 'other', 'key'],
        'client_id': 'test',
    }
    assert exampleauthz.handle(request) is None


def test_store(examplestore):
    bs = examplestore.store
    bs.get.return_value = 'example'
    examplestore.get('key')
    bs.get.return_value = 'other'
    pytest.raises(CSStoreError, examplestore.get, 'key')


@pytest.mark.parametrize('group,name,cls', [
    ('custodia.authenticators', 'ExampleAuth', ExampleAuth),
    ('custodia.authorizers', 'ExampleAuthz', ExampleAuthz),
    ('custodia.stores', 'ExampleStore', ExampleStore),
])
def test_plugins(group, name, cls, dist='custodiaexample'):
    ep = pkg_resources.get_entry_info(dist, group, name)
    assert ep.dist.project_name == dist
    assert ep.resolve() is cls
