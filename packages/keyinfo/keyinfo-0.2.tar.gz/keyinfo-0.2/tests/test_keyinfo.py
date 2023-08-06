
import unittest, logging

from keyinfo import keyinfo
from lxml import etree

from inspect import getsourcefile
from os.path import abspath, dirname, join

from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

class KeyInfoTestCase( unittest.TestCase ):

    def setUp(self):
        logging.getLogger('').handlers = []
        logging.basicConfig(level=logging.DEBUG,
                            filename="keyinfo_test.log")
        thisdir = dirname(abspath(getsourcefile(lambda:0)))
        self.testdatadir = join(thisdir,'data')

    def convert_pem_to_keyinfo(self, filename):
        filepath = join(self.testdatadir, filename)
        with open(filepath,'r') as f:
            data = f.read()
        cert = load_pem_x509_certificate(data,
                                         default_backend())
        keyinfoxml = keyinfo.to_keyinfo_sig1(cert)
        keyinfoxml_sig11 = keyinfo.to_keyinfo_sig11(cert)
        return keyinfoxml, keyinfoxml_sig11

    def load_keyinfo(self,filename):
        xmlfile = join(self.testdatadir, filename)
        parsedxml = etree.parse(xmlfile)
        return keyinfo.from_keyinfo(parsedxml)

    def test_load_pem(self):
        self.convert_pem_to_keyinfo('party_P2_signing_certificate.pem')

    def test_load_keyinfo(self):
        self.load_keyinfo('party_P1_signing_keyinfo.xml')

    def test_issuer_serial(self):
        self.assertRaises(Exception, self.load_keyinfo,
                          'party_P1_signing_keyinfo_bad_serial.xml')

    def test_issuer_serial2(self):
        self.assertRaises(Exception, self.load_keyinfo,
                          'party_P1_signing_keyinfo_bad_issuer.xml')

    def test_load_sig11(self):
        self.load_keyinfo('ca_A_CA_keyinfo_sig11.xml')

    def test_digest_check(self):
        self.assertRaises(Exception, self.load_keyinfo,
                          'party_P1_signing_keyinfo_sig11_bad_digest.xml')

