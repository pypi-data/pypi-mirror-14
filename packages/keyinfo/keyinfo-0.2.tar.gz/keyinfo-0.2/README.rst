=======
keyinfo
=======

Python library to convert X.509 certificates to and from W3C XML Signature KeyInfo structures


Description
===========

This library provides functionlity to convert X.509 certificates to and from W3C XML Signature 
KeyInfo structures.  

For X.509, the module is based on the python "cryptography" module (which in turn is based on OpenSSL).  
The keyinfo library converts to and from *cryptography.x509.certificate* objects. For XML, the module 
is based on the *lxml* library.  (Future versions may also use the simpler 
ElementTree library).

If you want to generate KeyInfo structures, your code needs to use existing functionality in that library 
to create certificates, or to load certificates in common file formats like PEM. The keyinfo module then
allows you to convert these certificate objects to KeyInfo XML trees.  Then, using the lxml library, you 
can save those trees to file or otherwise process them. There are two functions:
 * to_keyinfo_sig1 export to XML Signature version 1.0.  In this case the issuer and serial number are provided.
 * to_keyinfo_sig11 exports to XML Signature version 1.1. In this case SHA256 and SHA512 X509 digests are provided.

If you want to parse KeyInfo structures, your code needs to parse the XML data using lxml. You can
then use the *from_keyinfo(keyinfo)* function to create a *cryptography.x509.certificate* object.

Validation
==========

When loading certificates from KeyInfo, consistency checks are done between the X509Digest and 
X509Issuerserial element and the X509Certificate objects.  If you want additional certificate validation,
including path validation, you can use pyopenssl or wait for the next release of cryptography that will
provide this functionality.

Tests and Examples
==================

The *tests* subdirectory has a complete test suite and *tests/data* has sample KeyInfo and PEM files 
used by the tests.

Version History
===============

0.2, 2016.04.01.  Provided readme, tests, examples, validation.

0.1.3, 2016.03.27. First public Release.

