#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Igalia S.L.
#
# Distributed under terms of the GPLv3 or, at your option,
# under the terms of the Apache 2.0 license.

import unittest, tempfile, random, socket, time, shutil, os, signal, ldap3
from indicium.ldap import LDAPStore
from os import path as P

SCHEMA_PATH = os.getenv("OPENLDAP_SCHEMA_PATH", None)
if SCHEMA_PATH is None or not P.isdir(SCHEMA_PATH):
    SCHEMA_PATH = P.abspath(P.join(P.dirname(__file__), "testdata"))

SLAPD_CONF_TEMPLATE = """\
include  {schema_path}/core.schema
include  {schema_path}/cosine.schema
include  {schema_path}/inetorgperson.schema
include  {schema_path}/nis.schema
argsfile {tempdir}/slapd.args
pidfile  {tempdir}/slapd.pid
logfile  {tempdir}/slapd.log
loglevel 0
moduleload back_bdb
backend bdb
database bdb
suffix "dc=test,dc=org"
rootdn "cn=admin,dc=test,dc=org"
rootpw "{{SHA}}5en6G6MezRroT3XKqkdPOmY/BfQ="
directory "{tempdir}/data"
access to *
    by dn="cn=admin,dc=test,dc=org" write
    by * read
"""


class SlapdTestMixin(object):
    ldap_base    = "dc=test,dc=org"
    ldap_bind_dn = "cn=admin,dc=test,dc=org"
    ldap_bind_pw = "secret"
    __slapd_path = None
    __slapd_pid  = None
    __tempdir    = None

    @classmethod
    def slapd_path(cls):
        if cls.__slapd_path is None:
            dirs = os.getenv("PATH", "").split(":") + \
                    ["/usr/sbin", "/usr/local/sbin", "/sbin"]
            cls.__slapd_path = False
            for d in dirs:
                p = P.join(d, "slapd")
                if P.exists(p) and os.access(p, os.X_OK):
                    cls.__slapd_path = p
                    break
        return cls.__slapd_path

    def slapd_setup(self):
        self.__tempdir = tempfile.mkdtemp("-indicium-ldap-test")
        self.__slapd_pid = None

        # Loop until we find a free port
        while True:
            self.__slapd_port = random.randint(15000, 65000)
            if not self.__check_port(retry=False):
                break

        self.__slapd_uri = "ldap://127.0.0.1:{!s}".format(self.__slapd_port)
        os.mkdir(P.join(self.__tempdir, "data"))

        conffile = SLAPD_CONF_TEMPLATE.format(tempdir=self.__tempdir,
                schema_path=SCHEMA_PATH)
        with open(P.join(self.__tempdir, "slapd.conf"), "w", encoding="utf-8") as f:
            f.write(conffile)

        self.__fork_slapd()
        self.__check_port()

    def slapd_connect(self, bind=True):
        server = ldap3.Server(self.slapd_uri, get_info=ldap3.ALL)
        return ldap3.Connection(server, authentication=ldap3.AUTH_SIMPLE,
                user=self.ldap_bind_dn, password=self.ldap_bind_pw,
                auto_bind=(ldap3.AUTO_BIND_NO_TLS if bind else ldap3.AUTO_BIND_NONE))

    def slapd_create_base(self, conn):
        conn.add(self.ldap_base, ["top", "dcObject", "organization"],
                { "dc": "test", "o": "Test Organization" })

    @property
    def slapd_uri(self):
        return self.__slapd_uri

    @property
    def slapd_log(self):
        path = P.join(self.__tempdir, "slapd.log")
        if not P.isfile(path):
            return "(no slapd log)"
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def __check_port(self, host=None, port=None, retry=50, sleeptime=0.2):
        if host is None:
            host = "127.0.0.1"
        if port is None:
            port = self.__slapd_port
        if not retry:
            retry = 1  # Try at least once

        while retry:
            try:
                s = socket.socket()
                s.connect((host, port))
                return True
            except socket.error:
                time.sleep(sleeptime)
            finally:
                if s: s.close()
            retry -= 1
            return False

    def __fork_slapd(self):
        cmdline = [ self.slapd_path(), "-4", "-d", "128",
                "-f", P.join(self.__tempdir, "slapd.conf"),
                "-h", self.__slapd_uri ]
        self.__slapd_pid = os.fork()
        if self.__slapd_pid:
            time.sleep(0.2)
            return

        # Avoid stderr clobbering the terminal
        nullfd = os.open("/dev/null", os.O_WRONLY)
        os.dup2(nullfd, 2)
        os.close(nullfd)
        os.execl(cmdline[0], *cmdline)

    def slapd_cleanup(self):
        if self.__slapd_pid:
            os.kill(self.__slapd_pid, signal.SIGTERM)
            os.waitpid(self.__slapd_pid, 0)
        if self.__tempdir:
            shutil.rmtree(self.__tempdir)


def with_store(func):
    from functools import wraps
    @wraps(func)
    def wrapper(self, *arg, **kw):
        if not self.slapd_path():
            return self.skipTest("slapd unavailable")
        exc, ret, log = None, None, ""
        store = None
        try:
            self.slapd_setup()
            store = LDAPStore(self.slapd_uri, auto_bind=ldap3.AUTO_BIND_NO_TLS,
                    user=self.ldap_bind_dn, password=self.ldap_bind_pw)
            self.slapd_create_base(store.connection)
            ret = func(self, store, *arg, **kw)
        except Exception as e:
            log = self.slapd_log
            exc = e
        if store: del store
        self.slapd_cleanup()
        if exc is not None:
            import sys
            sys.stderr.write(log)
            raise exc
        return ret
    return wrapper


class TestLDAPStore(unittest.TestCase, SlapdTestMixin):
    test_data_1 = (
        ("/dc=org/dc=test/ou=People", {
            "objectClass"  : "organizationalUnit",
            "ou"           : "People",
        }),
        ("/dc=org/dc=Test/ou=Group", {
            "objectClass"  : "organizationalUnit",
            "ou"           : "Group",
        }),
        ("/dc=org/dc=test/ou=People/uid=user1", {
            "objectClass"  : ["posixAccount", "inetOrgPerson"],
            "cn"           : "Peter",
            "sn"           : "Jackson",
            "uid"          : "user1",
            "homeDirectory": "/home/user1",
            "loginShell"   : "/bin/bash",
            "uidNumber"    : "1",
            "gidNumber"    : "1",
        }),
        ("/dc=org/dc=test/ou=People/uid=user2", {
            "objectClass"  : ["posixAccount", "inetOrgPerson"],
            "cn"           : "John",
            "sn"           : "Doe",
            "uid"          : "user2",
            "homeDirectory": "/home/user2",
            "loginShell"   : "/bin/zsh",
            "uidNumber"    : "2",
            "gidNumber"    : "2",
        }),
        ("/dc=org/dc=test/ou=Group/cn=users", {
            "objectClass"  : "posixGroup",
            "cn"           : "users",
            "gidNumber"    : "5",
            "memberUid"    : ["user1", "user2"],
        }),
    )

    @with_store
    def test_direct_dn_mapping(self, s):
        self.assertTrue(s.contains("dc=test,dc=org"))

    @with_store
    def test_get_base(self, s):
        self.assertTrue(s.contains("/dc=org/dc=test"))
        org = s.get("/dc=org/dc=test")
        self.assertIsNotNone(org)
        self.assertEqual(["Test Organization"], org["o"])

    @with_store
    def test_modify_organization(self, s):
        key = "/dc=org/dc=test"
        self.assertTrue(s.contains(key))
        org = s.get(key)
        self.assertIsNotNone(org)
        org["o"] = ["Some other organization"]
        s.put(key, org)
        self.assertEqual(["Some other organization"], s.get(key)["o"])

    @with_store
    def test_add_orgunit(self, s):
        key, value = self.test_data_1[0]
        s.put(key, value)
        self.assertTrue(s.contains(key))
        self.assertEqual({"ou": ["People"],
            "objectClass": ["organizationalUnit"]} , s.get(key))

    @with_store
    def test_user_groups(self, s):
        [s.put(k, v) for k, v in self.test_data_1]
        self.assertTrue(s.contains("/dc=org/dc=test/ou=Group"))
        self.assertTrue(s.contains("/dc=org/dc=test/ou=Group/cn=users"))
        grp = s.get("/dc=org/dc=test/ou=Group/cn=users")
        members = grp["memberUid"]
        self.assertEqual(2, len(members))
        self.assertEqual(["user1", "user2"], sorted(members))

    @with_store
    def test_get_unexistent(self, s):
        self.assertIsNone(s.get("/dc=org/dc=test/ou=People/uid=somerandomuid"))

    @with_store
    def test_put_no_objectclass(self, s):
        with self.assertRaises(ValueError):
            s.put("/dc=org/dc=test/ou=People", {})

    @with_store
    def test_put_invalid_objectclass(self, s):
        with self.assertRaises(ValueError):
            s.put("/dc=org/dc=test/ou=People", { "objectClass": ["foobar"] })

    @with_store
    def test_modify_invalid_objectclass(self, s):
        key = "/dc=org/dc=test"
        org = s.get(key)
        org["objectClass"] = ["foobar"]
        with self.assertRaises(ValueError):
            s.put(key, org)

    @with_store
    def test_delete(self, s):
        [s.put(k, v) for k, v in self.test_data_1]
        key = "/dc=org/dc=test/ou=People/uid=user1"
        s.delete(key)
        self.assertFalse(s.contains(key))
