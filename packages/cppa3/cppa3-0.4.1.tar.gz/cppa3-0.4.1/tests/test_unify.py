
import unittest, cppa3, logging, lxml, os
from cppa3 import unify

from cppa3.unify import unify

from inspect import getsourcefile
from os.path import abspath, dirname, join

from copy import deepcopy

NSMAP = {'cppa': 'http://docs.oasis-open.org/ebcore/ns/cppa/v3.0' }

class CPPA3TestCase( unittest.TestCase ):

    def setUp(self):
        logging.getLogger('').handlers = []
        logging.basicConfig(level=logging.DEBUG,
                            filename="cppa3_test.log")
        thisdir = dirname(abspath(getsourcefile(lambda:0)))
        self.testdatadir = join(thisdir,'data')
        if 'CPPA3XSDDIR' in os.environ:
            # If we have the location of the CPPA3 XSD,  use it to validate inputs and
            # outputs
            cppa3dir = os.environ['CPPA3XSDDIR']
            cppa3xsd = os.path.join(cppa3dir,'cppa3.xsd')
            xmlschemadoc = lxml.etree.parse(cppa3xsd)
            self.schema = lxml.etree.XMLSchema(xmlschemadoc)
        else:
            # Else no schema validation
            self.schema = None

    def do_unification(self, id):
        logging.info('------------------------------------------')
        logging.info('Running test {}'.format(id))
        #logging.basicConfig(level=logging.DEBUG,
        #                    filename="cppa3_test.log")
        cppa_file = os.path.join(self.testdatadir,'cpp_a_'+id+'.xml')
        cppb_file = os.path.join(self.testdatadir,'cpp_b_'+id+'.xml')
        acpp =  lxml.etree.parse(cppa_file)
        bcpp =  lxml.etree.parse(cppb_file)
        if self.schema != None:
            if self.schema.validate(acpp) and self.schema.validate(bcpp):
                pass
            else:
                err = str(self.schema.error_log.last_error)
                raise cppa3.unify.UnificationException('Invalid input: {}'.format(err))
        cpa = unify(acpp, bcpp)
        if self.schema != None and self.schema.validate(cpa):
            logging.error('CPA {} is invalid'.format(id))
            raise cppa3.unify.UnificationException('CPA {} is invalid'.format(id))

        cpa_file_to_test_against = os.path.join(self.testdatadir,'cppa_ab_'+id+'.xml')
        if os.path.isfile(cpa_file_to_test_against):
            base_cpa =  lxml.etree.parse(cpa_file_to_test_against)
            base_cpa_clean = reset_timestamped_values_for_compare(base_cpa)
            base_cpa_clean_string = lxml.etree.tostring(base_cpa_clean,
                                                        pretty_print = True)
            cpa_clean = reset_timestamped_values_for_compare(cpa)
            cpa_clean_string = lxml.etree.tostring(cpa_clean,
                                                   pretty_print = True)
            if base_cpa_clean_string != cpa_clean_string:
                logging.error('Regression test failed for CPA {}'.format(id))
                logging.debug('Expected: {}'.format(base_cpa_clean_string))
                logging.debug('Found: {}'.format(cpa_clean_string))
                raise Exception('Regression test failed for CPA {}'.format(id))

        else:
            cpa_file= os.path.join(cpa_file_to_test_against)
            fd = open(cpa_file, 'wb')
            fd.write(lxml.etree.tostring(cpa, pretty_print=True))
            fd.close()

        logging.info('------------------------------------------')


    """
    General tests using NamedProtocolBinding
    """

    # One Service with complementary Roles one matching Action, matching send-receive, success
    def test_0001(self):
        self.do_unification('0001')

    #def test_000X(self):
    #    self.do_unification('0002')


    # One Service with with complementary Roles one non-matching Action, failure

    def test_0002(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0002')

    # One Service with with complementary Roles one matching Action, non-matching send-receive, failure
    def test_0003(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0003' )

    #Sample NamedProtocol for e-SENS
    def test_0007(self):
        self.do_unification('0007')

    #More complete use of NamedProtocol for e-SENS
    def test_0008(self):
        self.do_unification('0008')

    #Another complete use of NamedProtocol for e-SENS
    def test_0009(self):
        self.do_unification('0009')

    #Sample NamedProtocol for e-SENS
    def test_0010(self):
        self.do_unification('0010')

    # CPP B does not have any services specification with matching roles
    def test_0011(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0011' )

    # CPP B does not have any Service for matching roles
    def test_0012(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0012' )


    # A has two ServiceSpecification, only one of which is relevant for B
    def test_0013(self):
        self.do_unification('0013')

    # B has two ServiceSpecification, only one of which is relevant for A
    def test_0014(self):
        self.do_unification('0014')

    # A has one ActionBinding more in a ServiceBinding than B, and it is a mandatory one
    def test_0015(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0015' )

    # A has one ActionBinding more in a ServiceBinding than B, but it is an optional one
    def test_0016(self):
        self.do_unification('0016')

    # B has one ActionBinding more in a ServiceBinding than A, and it is a mandatory one
    def test_0017(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0017' )

    # A has one ActionBinding more in a ServiceBinding than B, but it is an optional one
    def test_0018(self):
        self.do_unification('0018')

    # No matching Role pair for A and B
    def test_0019(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0019' )

    # Some extra tests
    # Multiple ServiceSpecifications
    def test_0200(self):
        self.do_unification('0200')

    def test_0201(self):
        self.do_unification('0201')

    def test_0202(self):
        self.do_unification('0202')

    def test_0203(self):
        self.do_unification('0203')

    # Extra test, failing ActivationDate
    def test_0210(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0210' )

    def test_0211(self):
        self.assertRaises( cppa3.unify.UnificationException, self.do_unification, '0211' )



    """
    Certificates and Trust Anchors for Signing, Encryption and TLS
    """

    # Certificate and Trust Anchor test for Signing cert - positive - Send.
    def test_0020(self):
        self.do_unification('0020')

    # Certificate and Trust Anchor test for Signing cert - negative -Send .
    def test_0021(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0021')

    # Certificate and Trust Anchor test for Encryption cert - positive -Send.
    def test_0022(self):
        self.do_unification('0022')

    # Certificate and Trust Anchor test for Encryption cert - negative.
    def test_0023(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0023')

    # Certificate and Trust Anchor test for Signing cert - positive - Receive.
    def test_0024(self):
        self.do_unification('0024')

    # Certificate and Trust Anchor test for Signing cert - negative - Receive.
    def test_0025(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0025')


    # Certificate and Trust Anchor test for Encryption cert - positive -Receive.
    def test_0026(self):
        self.do_unification('0026')

    # Certificate and Trust Anchor test for TLS Server cert - positive - Send.
    def test_0027(self):
        self.do_unification('0027')

    # Certificate and Trust Anchor test for TLS Server cert - negative - Send.
    def test_0028(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0028')

    # Certificate and Trust Anchor test for TLS Server cert - negative - Receive.
    def test_0029(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0029')

    # Certificate and Trust Anchor test for TLS Server cert - positive - Receive.
    def test_0030(self):
        self.do_unification('0030')

    # Certificate and Trust Anchor test for TLS Client cert - positive - Send.
    def test_0031(self):
        self.do_unification('0031')

    # Certificate and Trust Anchor test for TLS Client cert - negative - Send.
    def test_0032(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0032')

    # Certificate and Trust Anchor test for TLS Client cert - positive - Receive.
    def test_0033(self):
        self.do_unification('0033')

    # Certificate and Trust Anchor test for TLS Client cert - negative - Receive.
    def test_0034(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0034')

    """
    TLS tests
    """

    # Cipher specified on one side
    def test_0040(self):
        self.do_unification('0040')

    # Cipher specified on other side
    def test_0041(self):
        self.do_unification('0041')

    # Cipher specified on both sides,  intersection exists
    def test_0042(self):
        self.do_unification('0042')

    # Cipher specified on both sides,  intersection does not exist
    def test_0043(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0043')

    # Version mismatch

    """
    User Authentication
    """

    # Specified on both sides consistently:  success
    def test_0050(self):
        self.do_unification('0050')

    # Specified on both sides inconsistently:  failure
    def test_0051(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0051')

    # Specified on both sides inconsistently:  failure
    def test_0052(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0052')

    # Specified on both sides inconsistently:  failure
    def test_0053(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0053')


    """
    Payload Profile
    """

    # Single part, matching partname, matching namespace, matching root element,
    # matching location, matching cardinality
    def test_0100(self):
        self.do_unification('0100')


    # Single part, non-matching partname, matching namespace, matching root element,
    # matching location, matching cardinality
    def test_0101(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0101')

    # Single part, matching partname, non-matching namespace, matching root element,
    # matching location, matching cardinality
    def test_0102(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0102')

    # Single part, matching partname, matching namespace, non-matching root element,
    # matching location, matching cardinality
    def test_0103(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0103')

    # Single part, matching partname, matching namespace, matching root element,
    # non-matching location, , matching cardinality
    def test_0104(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0104')

    # Single part, matching partname, matching namespace, matching root element,
    # matching location, non-matching cardinality
    def test_0105(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0105')

    # Two parts, matching partnames
    def test_0106(self):
        self.do_unification('0106')


    # Mismatch in number of parts
    def test_0107(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '0107')


    """
    ebBP attributes test

    @@@ to do
    """

    """
    ebMS3 tests
    """

    # ebMS3 test

    def test_1000(self):
        # two delivery channels,  the first one is compatible and chosen
        self.do_unification('1000')

    def test_1001(self):
        # two delivery channels,  the first one is non compatible so the second must be chosen
        self.do_unification('1001')

    def test_1006(self):
        # two delivery channels,  the first one is non compatible so the second must be chosen
        self.do_unification('1006')

    def test_1007(self):
        # example involving wider variety of services
        self.do_unification('1007')


    def test_1010(self):
        # E-SENS AS4 PoC
        self.do_unification('1010')

    def test_1011(self):
        # E-SENS AS4 PoC for A and B
        self.do_unification('1011')


    # MEPs
    # 1100 range

    # Simple Push MEP Send
    def test_1100(self):
        self.do_unification('1100')

    # Simple Push MEP Receive
    def test_1101(self):
        self.do_unification('1101')

    # Simple Pull MEP Send
    def test_1102(self):
        self.do_unification('1102')

    # Simple Pull MEP Receive
    def test_1103(self):
        self.do_unification('1103')

    # Inconsistency: A expects push,  B pull
    def test_1104(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '1104')

    # Inconsistency: A expects pull,  B push
    def test_1105(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '1105')

    # Two Way MEP push-and-push Send
    def test_1120(self):
        self.do_unification('1120')

    # Two Way MEP push-and-push Receive
    def test_1121(self):
        self.do_unification('1121')

    # Two Way MEP in one CPP confused with One Way in another
    def test_1122(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '1122')

    # Two Way MEP inconsistent in referred to action
    def test_1123(self):
        #self.do_unification('1123')
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '1123')

    # Two Way MEP sync Send
    def test_1124(self):
        self.do_unification('1124')

    # Two Way MEP sync Receive
    def test_1125(self):
        self.do_unification('1125')

    # Two Way MEP push-and-pull Send
    def test_1126(self):
        self.do_unification('1126')

    # Two Way MEP pull-and-push Send
    #def test_1127(self):
    #    self.do_unification('1127')

    # Two Way MEP pull-and-pull Send
    def test_1128(self):
        self.do_unification('1128')

    # Example that shows negotiation with various options for MEP Bindings

    # Example that shows negotiation with various options for MEP Bindings

    # Example that shows negotiation with various options for MEP Bindings

    # Pull MEP Send with secure Pull Channel
    def test_1140(self):
        self.do_unification('1140')

    # Pull MEP Receive with secure Pull Channel
    def test_1141(self):
        self.do_unification('1141')

    # Pull MEP Send with a specified MPC
    def test_1142(self):
        self.do_unification('1142')

    # Simple Pull MEP Receive with a specified MPC
    def test_1143(self):
        self.do_unification('1143')

    # Simple Push MEP Send with a specified MPC and Username security
    def test_1144(self):
        self.do_unification('1144')

    # Simple Push MEP Receive with a specified MPC and Username security
    def test_1145(self):
        self.do_unification('1145')

    # Error:  conflict in specified MPC,  gevallen A t/m F

    # Simple AS4 Push MEP Send with a single Payload part and a Compressed Payload
    def test_1146(self):
        self.do_unification('1146')

    # Simple Push MEP Send with a mandatory property
    def test_1147(self):
        self.do_unification('1147')


    # 1200 range
    # Reliable Messaging:  AS4 reception awareness

    # Specified on both sides consistently:  success
    def test_1200(self):
        self.do_unification('1200')

    # Specified on one side only:  failure
    #def test_1201(self):
    #    self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '1201')

    # PersistDuration
    def test_1202(self):
        self.do_unification('1202')

    # Specified on one sides only:  failure

    # Specified on both sides, inconsistent for duplicate elimination:  failure

    # AS4 and ReceiptHandling, Synchronous, Reception Awareness
    # Specified on both sides consistently:  success
    def test_1205(self):
        self.do_unification('1205')

    # AS4 and ReceiptHandling, Asynchronous, Reception Awareness
    def test_1206(self):
        self.do_unification('1206')

    # AS4 and ReceiptHandling, Synchronous, Non-Repudiation

    # AS4 and ReceiptHandling, Synchronous, Non-Repudiation


    # 1300 range
    # Compression and Packaging

    # 1400 range
    # Advanced features

    # Alternate Channel
    def test_1400(self):
        self.do_unification('1400')


    # External Payload
    def test_1410(self):
        self.do_unification('1410')

    # Extensibility

    # 1500
    # Cartesian



    """
    Web Services Tests
    """
    # 2000 base case

    # Fault

    # 2100
    # WS-Security: Signing, Encryption, Signing and Encryption, User Authentication

    # To do:
    # - timestamps

    # Presence match
    def test_2100(self):
        self.do_unification('2100')

    # Presence mismatch 1
    def test_2101(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2101')

    # Presence mismatch 2
    def test_2102(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2102')

    # WSS Version mismatch
    def test_2103(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2103')

    # Signature, minimal content, match
    def test_2110(self):
        self.do_unification('2110')

    # Presence mismatch 1
    def test_2111(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2111')

    # Presence mismatch 2
    def test_2112(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2112')

    # SignatureAlgorithm value mismatch 1
    def test_2113(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2113')

    # DigestAlgorithm value mismatch 1
    def test_2114(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2114')


    # Multiple SignatureAlgorithms
    # All considered equally acceptable
    def test_2115(self):
        self.do_unification('2115')

    # Multiple SignatureAlgorithms, no intersection
    def test_2116(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2116')

    # SignElements
    def test_2117(self):
        self.do_unification('2117')

    # presence mismatch
    def test_2118(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2118')

    # value mismatch
    def test_2119(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2119')

    # Multiple DigestAlgorithms
    def test_2120(self):
        self.do_unification('2120')

    # @@@ add some variations

    # SignAttachments
    def test_2125(self):
        self.do_unification('2125')

    # Presence mismatch
    def test_2126(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2126')

    # Value mismatch
    def test_2127(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2127')

    # Encryption
    # Base case, data encryption and certificate reference
    def test_2140(self):
        self.do_unification('2140')

    # Multiple options for data encryption
    def test_2141(self):
        self.do_unification('2141')

    # Multiple options for data encryption
    def test_2142(self):
        self.do_unification('2142')

    # Base case and key transport
    def test_2145(self):
        self.do_unification('2145')

    # Encrypt Elements
    def test_2146(self):
        self.do_unification('2146')

    # Encrypt Attachments
    def test_2147(self):
        self.do_unification('2147')

    # Encrypt External Payloads
    def test_2148(self):
        self.do_unification('2148')

    # Encrypt Attachments, mismatch
    def test_2149(self):
        self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2149')



    # User Authentication

    # Specified on both sides consistently:  success
    def test_2170(self):
        self.do_unification('2170')

    # Specified on both sides inconsistently:  failure
    #def test_2170(self):
    #    self.assertRaises(cppa3.unify.UnificationException, self.do_unification, '2171')



    # Packaging


    """
    EDIINT tests
    """

    # 3000 range

    # AS1

    # AS2
    def test_3000(self):
        self.do_unification('3000')


    # AS3

    # Signing

    # Encryption

    # Signing and Encryption

    # Compression

    """
    ebMS2 tests
    """

    # Simple Push MEP Send, no RM, no Security, synchronous errors
    # synReplyMode:  (msh)SignalsOnly
    def test_4000(self):
        self.do_unification('4000')

    # Simple Push MEP Send, no RM, no Security, asynchronous errors
    # synReplyMode:  none
    def test_4001(self):
        self.do_unification('4001')

    # @@@ add some non-matching cases

    # Simple Push MEP Send, RM, toParty, no Security, synchronous receipts
    # 4010
    def test_4010(self):
        self.do_unification('4010')

    # Simple Push MEP Send, RM, toParty, no Security, asynchronous receipts


    # @@@ mismatch in actor


    # 4020
    # Simple Push MEP Send, RM, nextMSH, no Security, synchronous errors
    def test_4020(self):
        self.do_unification('4020')

    # Simple Push MEP Send, RM, nextMSH, no Security, asynchronous errors

    # 4030
    # Simple Push MEP Send, no RM, signing, signed synchronous errors
    def test_4030(self):
        self.do_unification('4030')

    # Simple Push MEP Send, no RM, signing, signed asynchronous errors
    def test_4031(self):
        self.do_unification('4031')

    #def test_09900(self):
    #    self.do_unification('0100')


    # Synchronous Business Response

    # Two Way MEP,  asynchronous
    """
    "responseOnly"
    "signalsAndResponse"
    """

    # Two Way MEP,  synchronous

    """
    Extensibility

    """
    def test_0100(self):
        self.do_unification('0100')



def reset_timestamped_values_for_compare(cpa):
    cpa_to_edit = deepcopy(cpa)
    for path in [
        'child::cppa:AgreementInfo/cppa:Description',
        'child::cppa:AgreementInfo/cppa:ActivationDate',
        'child::cppa:AgreementInfo/cppa:ExpirationDate',
        'descendant::cppa:Password']:
        element_to_edit_l = cpa_to_edit.xpath(path,
                                              namespaces = NSMAP)
        if len(element_to_edit_l) > 0:
            for el in element_to_edit_l:
                value = el.text
                logging.error('Resetting {} from {}'.format(path, value))
                el.text = 'NONE'
    return cpa_to_edit




