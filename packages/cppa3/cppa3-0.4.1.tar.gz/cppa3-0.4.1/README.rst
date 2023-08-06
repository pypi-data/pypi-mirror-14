=====
cppa3
=====

A package to process ebCore CPPA3 documents.

Description
===========

The CPPA3 package provides a collection of Python modules to process OASIS
ebCore CPPA3 documents and related functionality.  CPPA3 is version 3 of
the ebXML Collaboration Protocol Profile and Agreement specification. A CPP is an
XML document representing a party's technical and business collaboration
capabilities.  A CPA is an XML document representing the agreed collaboration
parameters of two parties.  It can be used to configure B2B messaging systems
used to exchange messages between two parties using the agreed settings.
The ebCore Technical Committee (ebXML Core) is maintaining and enhancing the CPPA
specification.

The development of this package tracks the
development of the ebCore CPPA3 schema and specification. This release of the
package is compatible with the draft version 2016_02_17, available from
https://www.oasis-open.org/committees/document.php?document_id=57550. That
version supports configuration covering:

 * the complete ebMS 3.0 Core OASIS Standard (docs.oasis-open.org/ebxml-msg/ebms/v3.0/core/os/)
 * the complete AS4 OASIS Standard (http://docs.oasis-open.org/ebxml-msg/ebms/v3.0/profiles/AS4-profile/v1.0/)
 * some parts of the ebMS 3.0 Part 2 Advanced Features specification (http://docs.oasis-open.org/ebxml-msg/ebms/v3.0/part2/201004/).
 * ebMS 2.0 (https://www.oasis-open.org/standards#ebxmlmsgv2)
 * SOAP messaging
 * and the AS1, AS2 (https://tools.ietf.org/html/rfc4130) and AS3 IETF EDIINT specifications.

Currently, three modules are provided:

* unify.py provides functionality to automatically form a CPA from two CPPs.
* pmode.py provides functionality to generate a (set of) P-Modes from a CPA.
* cpa2.py is an incomplete experimental module that converts a subset of v3 CPAs to version 2.0 CPA.

Various future enhancements of this library are planned.

As the CPPA3 schema is still under development,  it may change in backward-incompatible
ways, and this library will be updated accordingly.

unify.py
========

This module defines a single function:

* *unify*.

This function operates on two CPP XML documents, parsed into element trees using
the Python lxml library, and returns a CPA, if one exists.  If no CPA can be created,
a *UnificationException* is thrown instead.

Internally in the module, the unify function instantiates an object of the CPABuilder
class, and invokes the unify method of that object with the specified CPP documents.
CPA formation is similar to unification in logic programming and involves exploring many (successful
or unsuccessful) paths, possibly repeatedly.  The unify function
memoizes partial search results, and the class provides data structures to locally
store those results (which are specific to the two input CPPs and therefore not
useful in other contexts).  The purpose of memoization is to some extent optimization,
but also keeps the logging human-readable.

pmode.py
========

This module defines the following functions:

* *load_pmodes_from_cpa*
* *validate_pmode*

The *load_pmodes_from_cpa* function operates on
a CPA document and returns a list of processing modes. Using optional parameters,
the function can be restricted to processing modes involving a particular
named or identified party. If *partyname* is specified, it
will skip any definitions not involving a party with that name.
If *partyid* is specified, it will skip any definitions not involving a party with that name.


The *validate_pmode* function operates on list of processing modes and validates this list
against a JSON schema for processing modes that is part of the library.

Test Suite
==========

A test suite is provided for the two modules.  To run the test suite, you can optionally
validate the CPP or CPA documents against the draft CPPA3 XML schema. To do this,
you must download the schema to a readable location on the filesystem, and set the
*CPPA3XSDDIR* environment variable to this location. If the variable is not set, no validation
is done.

History
=======

v0.4,  2016-04-01.  Experimental CPA2 module;  fixes to certificates and trust anchor handling.

v0.3.9, 2016-03-16.  First public release.



