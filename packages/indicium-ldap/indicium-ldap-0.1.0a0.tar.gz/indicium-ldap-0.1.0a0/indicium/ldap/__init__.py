#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Igalia S.L.
#
# Distributed under terms of the GPLv3 or, at your option,
# under the terms of the Apache 2.0 license.

from .. import base
import ldap3


def _key_to_dn(key):
    from ..key import split
    return ",".join(reversed(split(key)))


class LDAPStore(base.Store):
    __slots__ = ("_conn",)

    def __init__(self, uri=None, connection=None, *arg, **kw):
        self._conn = None
        if connection is None:
            kw["raise_exceptions"] = False
            connection = ldap3.Connection(uri, *arg, **kw)
        self._conn = connection

    def __del__(self):
        if self._conn:
            self._conn.unbind()
            self._conn = None

    @property
    def connection(self):
        return self._conn

    def get(self, key):
        if self._conn.search(_key_to_dn(key), "(objectClass=*)",
                search_scope=ldap3.BASE, attributes=ldap3.ALL_ATTRIBUTES):
            # TODO: Handle responses with more than a single result
            return self._conn.response[0]["attributes"]
        return None

    def put(self, key, value):
        dn = _key_to_dn(key)
        if self._conn.search(dn, "(objectClass=*)", search_scope=ldap3.BASE):
            changes = {}
            for k, v in value.items():
                changes[k] = [(ldap3.MODIFY_REPLACE, v)]
            if not self._conn.modify(dn, changes):
                raise ValueError("{!r}: {!s}".format(key,
                    self._conn.result))
        elif "objectClass" in value:
            object_class = value["objectClass"]
            if not self._conn.add(dn, object_class, value):
                raise ValueError("{!r}: {!s}".format(key,
                    self._conn.result))
        else:
            raise ValueError("{!r}: no objectClass".format(key))

    def delete(self, key):
        self._conn.delete(_key_to_dn(key))

    def contains(self, key):
        # No need to retrieve any attributes
        if self._conn.search(_key_to_dn(key), "(objectClass=*)",
                search_scope=ldap3.BASE):
            return True
        return False

    def query(self, pattern, limit=None, offset=0):
        raise NotImplementedError
