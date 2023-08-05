=====================
 Indicium LDAP Store
=====================

.. image:: https://img.shields.io/travis/aperezdc/indicium-ldap.svg?style=flat
   :target: https://travis-ci.org/aperezdc/indicium-ldap
   :alt: Build Status

.. image:: https://img.shields.io/coveralls/aperezdc/indicium-ldap/master.svg?style=flat
   :target: https://coveralls.io/r/aperezdc/indicium-ldap?branch=master
   :alt: Code Coverage

A LDAP-backed key-value store backend for `Indicium
<https://github.com/aperezdc/indicium>`_.


Usage
=====

.. code-block:: python

    # Instantiate and write some data.
    from indicium.ldap import LDAPStore
    store = LDAPStore("ldap://localhost")
    store.put("/dc=org/dc=test", { "dc": "test", "o": "My organization",
            "objectClass": ["top", "dcObject", "organization"] })

    # Read the data back.
    org = store.get("/dc=org/dc=test")

    # Using the DN directly is also possible.
    assert org == store.get("/dc=test,dc=org")

Note that a directory service accessed using LDAP is supposed to have a
certain structure, so depending on the schema and structure used by the
directory server, and therefore the set of useable keys (and whether they are
writeable or not) will vary. In particular:

* Path components of keys are mapped to the DN components of the LDAP
  entities, in reversed order.

* When using ``.put()`` is is *mandatory* to specify an ``objectClass``
  attribute. Note that when writing to existing objects *it is possible*
  to specify a different ``objectClass`` value to mutate the object, but this
  is discouraged and may not work with some directory servers—it may be needed
  to ``.delete()`` the entity first.

* Using ``.put()`` to modify an existing object uses ``MODIFY_REPLACE``
  change operations, which means that values of attributes *will be replaced*,
  or *added*, but never removed. For now the only way of deleting entity
  attributes is to ``.delete()`` the entity first, and then re-create it.


Installation
============

All stable releases are uploaded to `PyPI <https://pypi.python.org>`_, so you
can install them and upgrade using ``pip``::

    pip install indicium-ldap

Alternatively, you can install the latest development code —at your own risk—
directly from the Git repository::

    pip install git://github.com/aperezdc/indicium-ldap


Development
===========

If you want to contribute, please use the usual GitHub workflow:

1. Clone the repository.
2. Hack on your clone.
3. Send a pull request for review.

If you do not have programming skills, you can still contribute by `reporting
issues <https://github.com/aperezdc/indicium-ldap/issues>`__ that you may
encounter. Contributions to the documentation are very welcome, too!
