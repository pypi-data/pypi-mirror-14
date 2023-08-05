ldaptools
=========

Helper modules to work with LDAP directories and test LDAP tools against OpenLDAP.

- `ldaptools.ldif_utils`: simple parser for LDIF files
- `ldaptools.ldap_source`: generate a stream of LDAP entries from an LDAP URL
- `ldaptools.synchronize`: synchronization class to synchronize a source of LDAP records with a target
- `ldaptools.paged`: an LDAPObject implementating paged search requests
- `ldaptools.ldapsync`: a command line client to the Synchronize class
- `ldaptools.slapd`: launch a standalone slapd server, manipulate its configuration, it helps
  in writing tests against OpenLDAP.

ldapsync
========

        usage: ldapsync [-h] --object-class-pivot OBJECT_CLASS_PIVOT
                        [--attributes-file ATTRIBUTES_FILE] [--attributes ATTRIBUTES]
                        --source-uri SOURCE_URI --source-base-dn SOURCE_BASE_DN
                        [--source-bind-dn SOURCE_BIND_DN]
                        [--source-bind-password SOURCE_BIND_PASSWORD] --target-uri
                        TARGET_URI --target-base-dn TARGET_BASE_DN
                        [--target-bind-dn TARGET_BIND_DN]
                        [--target-bind-password TARGET_BIND_PASSWORD] [--fake]
                        [--verbose]

        Synchronize an LDIF file or a source LDAP directory to another directory Base
        DN of the source is remapped to another DN in the target directory

        optional arguments:
          -h, --help            show this help message and exit
          --object-class-pivot OBJECT_CLASS_PIVOT
                                an objectClass and an attribute name which is the
                                unique identifier for this class
          --attributes-file ATTRIBUTES_FILE
                                a file containing the list of attributes to
                                synchronize
          --attributes ATTRIBUTES
                                a list of attribute names separated by spaces
          --source-uri SOURCE_URI
                                URL of an LDAP directory (ldapi://, ldap:// or
                                ldaps://) or path of and LDIF file
          --source-base-dn SOURCE_BASE_DN
                                base DN of the source
          --source-bind-dn SOURCE_BIND_DN
                                bind DN for a source LDAP directory
          --source-bind-password SOURCE_BIND_PASSWORD
                                bind password for a source LDAP directory
          --target-uri TARGET_URI
                                URL of the target LDAP directory
          --target-base-dn TARGET_BASE_DN
                                base DN of the target LDAP directory
          --target-bind-dn TARGET_BIND_DN
                                bind DN for a target LDAP directory
          --target-bind-password TARGET_BIND_PASSWORD
                                bind password for a target LDAP directory
          --fake                compute synchronization actions but do not apply
          --verbose             print all actions to stdout

Exemple
-------

Synchronize tree of organizational units and people between an LDIF file and a local OpenLDAP directory::

        ldapsync --attributes 'uid cn givenName sn dc ou o description mail member' \
                 --object-class-pivot 'inetOrgPerson uid' \
                 --object-class-pivot 'organizationalUnit ou' \
                 --object-class-pivot 'dcobject dc' \
                 --source-uri dump.ldif \
                 --source-base-dn dc=myorganization,dc=fr \
                 --target-uri ldapi:// \
                 --target-base-dn o=myorganization,dc=otherorganization,dc=fr \
                 --verbose

Synchronize tree of organizational units and people between two LDAP directories::

        ldapsync --attributes 'uid cn givenName sn dc ou o description mail member' \
                 --object-class-pivot 'inetOrgPerson uid' \
                 --object-class-pivot 'organizationalUnit ou' \
                 --object-class-pivot 'dcobject dc' \
                 --source-uri ldap://ldap.myorganization.fr \
                 --source-bind-dn uid=admin,ou=people,dc=myorganization,dc=fr
                 --source-bind-password password
                 --source-base-dn dc=myorganization,dc=fr \
                 --target-uri ldap://ldap.otherorganization.fr
                 --target-bind-dn uid=admin,o=myorganization,dc=otherorganization,dc=fr
                 --target-bind-password password
                 --target-base-dn o=myorganization,dc=otherorganization,dc=fr \
                 --verbose

Changelog
=========

0.9
---

* paged: fix paged search when the response contains no paged result extended control
* improvements to tox script


0.8
---

* improve display of actions and errors
* lowercase attributes in dn of LDIF sources
* fix bug when removing attributes from source outside the permitted attributes
* allow specifying case insensitive attributes for compare

0.7
---

* ldapsync: add a --source-filter parameter

0.6
---

* add empty attribute to new entry if attribute is present in target entry
* remove attributes outside of the specified attributes from source entries
* return an empty list of target base DN does no exist
* convert attribute names to istr
* fix typo

0.5
---

* setup.py: add long description

0.4
---

* remove debugging print

0.3
---

* setup.py: add dependency on setuptools

0.2
---

* improvements to tox script

0.1
---

* initial release
