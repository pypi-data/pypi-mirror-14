__author__ = 'pvde'

"""
To do:

- Rename certificate IDs and IDREFs to avoid ID clashes.
- Remove Certificates that aren't referenced.

- TrustAnchors?
- Instead of just validating the XSD, check that the certificates are valid using pyca.

- Support for ChannelFeature for e.g. WSSecurityBinding, and test samples that show the
benefits of reuse.

- Check that packaging specifications are created and present in CPA
(Seems to work ??)

- Improve handling of dependencies.  Not just one check,  but as channels are added, re-run.
(Seems to work ??)

- Support and tests for WS-ReliableMessaging.

"""

import lxml.etree, logging, datetime, isodate, traceback, hashlib, base64, uuid, re

from isodate.duration import Duration

from copy import deepcopy

logging.basicConfig(level=logging.DEBUG)

NSMAP = {'cppa': 'http://docs.oasis-open.org/ebcore/ns/cppa/v3.0',
         'ds': 'http://www.w3.org/2000/09/xmldsig#',
         'xml': 'http://www.w3.org/XML/1998/namespace'}

def unify(acpp, bcpp):
    unifier = CPABuilder()
    return unifier.unify(acpp, bcpp)

class UnificationException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CPABuilder():

    def __init__(self):
        self.reset_caches()

        self.protocolhandlers = {cppa('NamedChannel'): self.unify_named_channel,
                                 cppa('EDIINTChannel'): self.unify_ediint_channel,
                                 cppa('ebMS2Channel'): self.unify_ebms2_channel,
                                 cppa('WSChannel'): self.unify_ws_channel,
                                 cppa('ebMS3Channel'): self.unify_ebms3_channel,
                                 cppa('TransportChannel') : self.unify_transport_channel }

        self.packaging_handlers = {cppa('SOAPWithAttachmentsEnvelope'): self.unify_soap_with_attachments_envelope,
                                   cppa('SimpleSOAPEnvelope'): self.unify_simple_soap_envelope,
                                   cppa('MIMEEnvelope'): self.unify_mime_envelope}

        self.mimepart_handlers = {cppa('CompressedSimpleMIMEPart'): self.unify_compressed_mime_part,
                                  cppa('MIMEMultipartRelated'): self.unify_mime_multipart_related,
                                  cppa('ExternalPayload'): self.unify_external_payload,
                                  cppa('SimpleMIMEPart'): self.unify_simple_mime_part}

    def reset_caches(self):
        self.included_service_specifications_counter = 0

        self.included_certificates = {}

        self.unify_channels_results = {}
        self.unify_channels_exceptions = {}

        self.unify_transport_results = {}
        self.unify_transport_exceptions = {}

        self.unify_payload_profile_results = {}
        self.unify_payload_profile_exceptions = {}

        self.unify_package_results = {}
        self.unify_package_exceptions = {}

        self.depends_on = {}

        self.included_components = {}

        self.shortened = {}
        self.collisions = {}

    def unify(self, acpp, bcpp, partyrole=None, counterpartyrole=None):
        self.reset_caches()
        cpa = lxml.etree.Element(cppa('CPA'),
                                 nsmap = NSMAP)
        acppid, bcppid = self.unify_profileinfo(cpa, acpp, bcpp)

        acpapartyinfo = self.initialize_partyinfo(cpa, acpp, 'PartyInfo')
        bcpapartyinfo = self.initialize_partyinfo(cpa, bcpp, 'CounterPartyInfo')
        logging.info("Unifying {} {}".format(acppid, bcppid))

        aServiceSpecifications = acpp.xpath('//cppa:ServiceSpecification',
                                                 namespaces=NSMAP)

        for aServiceSpecification in aServiceSpecifications:
            try:
                self.unify_servicebinding_list(cpa,
                                               acpp,
                                               bcpp,
                                               aServiceSpecification,
                                               acppid,
                                               bcppid,
                                               partyrole,
                                               counterpartyrole)
            except UnificationException as e:
                logging.info('Exception in Service Specification: {}'.format(e.value))

        if self.included_service_specifications_counter == 0:
            # There has to be at least one role pair
            # for which there is at least one matching binding
            situation = 'No matching service specifications for {}-{}'.format(acppid,
                                                                              bcppid)
            logging.info(situation)
            raise UnificationException(situation)
        else:
            logging.info('Matched {} service specification(s)'.format(self.included_service_specifications_counter))

        if 'actionbinding' in self.included_components:
            for ab in self.included_components['actionbinding']:
                if ab in self.depends_on and 'deliverychannel' in self.depends_on[ab]:
                    for dc in self.depends_on[ab]['deliverychannel']:
                        self.confirm_included('deliverychannel', dc)
                if ab in self.depends_on and 'payloadprofile' in self.depends_on[ab]:
                    for pp in self.depends_on[ab]['payloadprofile']:
                        self.confirm_included('payloadprofile', pp)

        if 'deliverychannel' in self.included_components:
            for ch in self.included_components['deliverychannel']:
                if ch in self.depends_on and 'deliverychannel' in self.depends_on[ch]:
                    for ch2 in self.depends_on[ch]['deliverychannel']:
                        self.confirm_included('deliverychannel', ch2)

            for ch in self.included_components['deliverychannel']:
                cpa.append(self.unify_channels_results[ch])

            for ch in self.included_components['deliverychannel']:
                if ch in self.depends_on and 'transport' in self.depends_on[ch]:
                    for tid in self.depends_on[ch]['transport']:
                        self.confirm_included('transport', tid)

        if 'transport' in self.included_components:
            for tp in self.included_components['transport']:
                cpa.append(self.unify_transport_results[tp])

        if 'payloadprofile' in self.included_components:
            for pp in self.included_components['payloadprofile']:
                cpa.append(self.unify_payload_profile_results[pp])

        if 'deliverychannel' in self.included_components:
            for ch in self.included_components['deliverychannel']:
                if ch in self.depends_on and 'package' in self.depends_on[ch]:
                    for ppid in self.depends_on[ch]['package']:
                        (a, b, c, d) = ppid
                        pp = self.unify_package_results[ppid]
                        logging.info("Unifying {}-{} {}-{}: {}".format(a, b, c, d, pp.tag))
                        pp.set('id', self.cppaid(a, b, c, d))
                        cpa.append(self.unify_package_results[ppid])

        return self.c14n(cpa)

    def c14n(self, tree):
        newtree = lxml.etree.Element(tree.tag, nsmap=NSMAP)
        newtree.text = tree.text
        for att in tree.attrib:
            newtree.attrib[att] = tree.attrib[att]
        for element in tree:
            #print str(element)
            if element is None:
                pass
            elif type(element) is lxml.etree._Element:
                newtree.append(self.c14n(element))
            else:
                newtree.append(element)
        return newtree

    def unify_profileinfo(self, cpa, acpp, bcpp):
        acppid = acpp.xpath('child::cppa:ProfileInfo/cppa:ProfileIdentifier/text()',
                            namespaces=NSMAP)[0]
        bcppid = bcpp.xpath('child::cppa:ProfileInfo/cppa:ProfileIdentifier/text()',
                            namespaces=NSMAP)[0]
        agreementinfo = lxml.etree.SubElement(cpa,
                                              cppa('AgreementInfo'))
        agreementid = lxml.etree.SubElement(agreementinfo,
                                            cppa('AgreementIdentifier'))
        agreementid.text = "{}_{}".format(acppid, bcppid)
        agreementdescription = lxml.etree.SubElement(agreementinfo, cppa('Description'))
        agreementdescription.text = "Agreement formed from {} and {} at {}".format(acppid,
                                                                                   bcppid,
                                                                                   datetime.datetime.now().isoformat())
        agreementdescription.set(xml('lang'), 'en')
        for pid in [acppid, bcppid]:
            pid2 = lxml.etree.SubElement(agreementinfo, cppa('ProfileIdentifier'))
            pid2.text = pid

        self.init_activationdate(acpp, bcpp, agreementinfo)
        return acppid, bcppid

    def init_activationdate(self, acpp, bcpp, agreementinfo):
        now = datetime.datetime.now()
        try:
            aphasein = acpp.xpath('child::cppa:ProfileInfo/cppa:PhaseIn/text()',
                                  namespaces=NSMAP)[0]
            aduration = isodate.isoduration.parse_duration(aphasein)
        except:
            aduration = datetime.timedelta(0)
        try:
            bphasein = bcpp.xpath('child::cppa:ProfileInfo/cppa:PhaseIn/text()',
                                  namespaces=NSMAP)[0]
            bduration = isodate.isoduration.parse_duration(bphasein)
        except:
            bduration = datetime.timedelta(0)

        if aduration < bduration:
            earliest = now + bduration
        else:
            earliest = now + aduration

        for cpp in [acpp, bcpp]:
            activationl = cpp.xpath('child::cppa:ProfileInfo/cppa:ActivationDate/text()',
                                    namespaces=NSMAP)
            if len(activationl) > 0:
                activation = isodate.isodatetime.parse_datetime(activationl[0])
                if activation > earliest:
                    earliest = activation

        activationdate = lxml.etree.SubElement(agreementinfo, cppa('ActivationDate'))
        activationdate.text = earliest.isoformat()

        expirationdefault = None
        for cpp in [acpp, bcpp]:
            expirationL = cpp.xpath('child::cppa:ProfileInfo/cppa:ExpirationDate/text()',
                                    namespaces=NSMAP)
            if len(expirationL) > 0:
                expiration = isodate.isodatetime.parse_datetime(expirationL[0])
                if expiration < earliest:
                    situation = 'Service expires at {} before earliest activation {}'.format(expirationL[0],
                                                                                             earliest.isoformat())
                    logging.info(situation)
                    raise UnificationException(situation)
                if expirationdefault is None:
                    expirationdefault = expiration
                elif expiration < expirationdefault:
                    expirationdefault = expiration

        if not expirationdefault is None:
            expirationdate = lxml.etree.SubElement(agreementinfo, cppa('ExpirationDate'))
            expirationdate.text = expirationdefault.isoformat()

    def initialize_partyinfo(self, cpa, cpp, element):
        partyinfo = lxml.etree.SubElement(cpa, cppa(element))

        inelement = cpp.xpath('child::cppa:PartyInfo',
                              namespaces=NSMAP)[0]
        for pname in inelement.xpath('child::cppa:PartyName',
                               namespaces= NSMAP):
            partyinfo.append( deepcopy(pname))
        for pid in inelement.xpath('descendant-or-self::cppa:PartyId',
                             namespaces= NSMAP):
            partyinfo.append( deepcopy(pid))
        for certificate in inelement.xpath('child::cppa:Certificate',
            namespaces= NSMAP):
            partyinfo.append(deepcopy(certificate))
        return partyinfo

    def unify_servicebinding_list(self, cpa, acpp, bcpp,
                                  aServiceSpecification, acppid, bcppid,
                                  partyrole, counterpartyrole, bindings_match_mode='all'):
        arole = aServiceSpecification.xpath('child::cppa:PartyRole/@name',
                                      namespaces=NSMAP)[0]
        brole = aServiceSpecification.xpath('child::cppa:CounterPartyRole/@name',
                                      namespaces=NSMAP)[0]

        logging.error('!! {} {} {}'.format(arole, brole, partyrole))

        if (partyrole is None or partyrole == arole) \
                and (counterpartyrole is None or counterpartyrole == brole):

            serviceSpecification = lxml.etree.Element(cppa('ServiceSpecification'))

            lxml.etree.SubElement(serviceSpecification, cppa('PartyRole'), name=arole)
            lxml.etree.SubElement(serviceSpecification, cppa('CounterPartyRole'), name=brole)

            xpqt = '//cppa:ServiceSpecification[cppa:PartyRole/@name = "{}" and cppa:CounterPartyRole/@name = "{}"]'
            xpq = xpqt.format(brole, arole)
            try:
                bServiceSpecification = bcpp.xpath(xpq,
                                                   namespaces=NSMAP)[0]
            except IndexError:
                situation = 'No ServiceSpecification for {} {} in {}'.format(brole,
                                                                             arole,
                                                                             bcppid)
                logging.info(situation)
                if partyrole is not None and counterpartyrole is not None:
                    """
                    We raise an exception if unification was requested for a specific
                    PartyRole-CounterPartyRole combination.
                    Otherwise, we assume it can just be ignored.
                    """
                    raise UnificationException(situation)

            else:
                logging.debug('Included service specifications: {}'.format(self.included_service_specifications_counter))
                aservicebindingL = aServiceSpecification.xpath('child::cppa:ServiceBinding',
                                                               namespaces=NSMAP)

                included_bindings_counter = 0
                last_exception = None
                for aservicebinding in aservicebindingL:
                    try:
                        acpaservicebinding = self.unify_servicebinding_from_acpp_party(acppid,
                                                                                       acpp,
                                                                                       bcppid,
                                                                                       bcpp,
                                                                                       arole,
                                                                                       brole,
                                                                                       aservicebinding,
                                                                                       bServiceSpecification)
                    except UnificationException as e:
                        last_exception = e
                        if bindings_match_mode == 'all':
                            logging.info("UnificationException: {}".format(e.value))
                            raise
                        else:
                            logging.info('Bindings match mode {} so ignoring {}'.format(bindings_match_mode,
                                                                                        e.value))
                    else:
                        included_bindings_counter += 1
                        serviceSpecification.append(acpaservicebinding)

                if included_bindings_counter > 0:
                    cpa.append(serviceSpecification)
                    self.included_service_specifications_counter += 1
                else:
                    situation = 'No Service Bindings matched for {}-{} {}-{}: {}'.format(acppid,
                                                                                         arole,
                                                                                         bcppid,
                                                                                         brole,
                                                                                         last_exception)
                    logging.info(situation)
                    raise UnificationException(situation)
        else:
            logging.info("Skipping role {}".format(arole))

    def unify_servicebinding_from_acpp_party(self,
                                            acppid,
                                            acpp,
                                            bcppid,
                                            bcpp,
                                            arole,
                                            brole,
                                            aservicebinding,
                                            bServiceSpecification):
        acpaservicebinding = lxml.etree.Element(cppa('ServiceBinding'))
        aserviceEl = aservicebinding.xpath('child::cppa:Service',
                                           namespaces=NSMAP)[0]
        aservice = aserviceEl.text
        aservicetype = aserviceEl.get('type')
        logging.info("Processing service {} {}".format(aservice, aservicetype))
        acpaservice = lxml.etree.SubElement(acpaservicebinding, cppa('Service'))
        acpaservice.text = aservice
        if aservicetype is not None:
            acpaservice.set('type', aservicetype)
        if aservicetype is None:
            bserviceq = 'child::cppa:ServiceBinding[cppa:Service="{}"]'.format(aservice)
        else:
            bserviceqt = 'child::cppa:ServiceBinding[cppa:Service[text()="{}" and @type="{}"]]'
            bserviceq = bserviceqt.format(aservice, aservicetype)
        try:
            bservicebinding = bServiceSpecification.xpath(bserviceq,
                                                          namespaces=NSMAP)[0]
        except:
            raise UnificationException('Service {} not found for {} {} in {}'.format(aservice,
                                                                                     brole,
                                                                                     arole,
                                                                                     bcppid))
        else:
            logging.info("Unifying definitions for service {} in role {}".format(aservice, arole))
            self.unify_servicebinding(acppid, acpp,
                                      bcppid, bcpp,
                                      aservice,
                                      aservicebinding, bservicebinding,
                                      acpaservicebinding)
        return acpaservicebinding

    def unify_servicebinding(self, acppid, acpp, bcppid, bcpp, service,
                             aservicebinding, bservicebinding,
                             servicebinding):
        logging.info("Unifying service {} in {} and {}".format(service, acppid, bcppid))

        (identifiers, actions) = self.unify_send_receive(acppid, acpp, bcppid, bcpp, service,
                                                         aservicebinding, bservicebinding,
                                                         servicebinding,
                                                         "send", "receive",
                                                         action_identifiers =[],
                                                         actions=[])
        (identifiers2, actions2) = self.unify_send_receive(acppid, acpp, bcppid, bcpp, service,
                                                           aservicebinding, bservicebinding,
                                                           servicebinding,
                                                           "receive", "send",
                                                           action_identifiers=identifiers,
                                                           actions=actions)
        logging.info("Unified service binding in {} and {} for {}".format(acppid, bcppid, service))
        logging.debug("Identifier list for {}, {}, {}: {}".format(acppid, bcppid, service, identifiers2))
        self.check_b_servicebinding(actions2, bservicebinding)

        for id in identifiers2:
            self.confirm_included('actionbinding', id)
            #if id in self.depends_on and 'deliverychannel' in self.depends_on[id]:
            #    for id2 in self.depends_on[id]['deliverychannel']:
            #        self.confirm_included('deliverychannel', id2)

    def unify_send_receive(self,
                           acppid, acpp,
                           bcppid, bcpp,
                           service,
                           aservicebinding, bservicebinding,
                           abservicebinding,
                           atype, btype,
                           action_identifiers = [],
                           actions = []):

        try:
            asendbindingL = aservicebinding.xpath('child::cppa:ActionBinding[@sendOrReceive="{}"]'.format(atype),
                                                  namespaces=NSMAP)

            #aabc = int(aservicebinding.xpath('count(child::cppa:ActionBinding)', namespaces=NSMAP))
            #babc = int(bservicebinding.xpath('count(child::cppa:ActionBinding)', namespaces=NSMAP))
            #if aabc != babc:
            #    raise UnificationException("Unequal number of actions in service {}: {}-{}".format(service,
            #                                                                                       aabc,
            #                                                                                       babc))

            for abinding in asendbindingL:
                action = abinding.get('action')
                aid = abinding.get('id')

                actionbinding = lxml.etree.Element(cppa('ActionBinding'),
                                                   id=aid, sendOrReceive=atype, action=action)
                a_reply_to = abinding.get('replyTo')
                if a_reply_to is not None:
                    actionbinding.set('replyTo', a_reply_to)

                bexpr = 'child::cppa:ActionBinding[@action="{}" and @sendOrReceive="{}"]'.format(action, btype)

                bbindingL = bservicebinding.xpath(bexpr,
                                                  namespaces=NSMAP)
                if len(bbindingL) == 1:
                    bbinding = bservicebinding.xpath(bexpr,
                                                     namespaces=NSMAP)[0]

                    bid = bbinding.get('id')
                    logging.info("Unifying {}-{} in {} and {} channels {} - {}".format(service,
                                                                                       action,
                                                                                       acppid,
                                                                                       bcppid,
                                                                                       aid,
                                                                                       bid))

                    self.check_action_replyto(service, action, a_reply_to, bbinding,
                                              aservicebinding, bservicebinding)

                    # PayloadProfile
                    appid = abinding.get('payloadProfileId')
                    bppid = bbinding.get('payloadProfileId')
                    if appid is not None and bppid is not None:
                        self.unify_payload_profile(acppid, acpp, bcppid, bcpp, appid, bppid)
                        logging.info('Setting attribute to {} for {} {} {} {}'.format(self.cppaid(acppid, appid, bcpp, bppid),
                                                                                      acppid,
                                                                                      appid,
                                                                                      bcppid, bppid))
                        actionbinding.set('payloadProfileId', self.cppaid(acppid, appid, bcppid, bppid))
                        self.record_dependency((acppid, aid, bcppid, bid),
                                               'payloadprofile',
                                               (acppid, appid, bcppid, bppid))

                    (acppid, acid, bcppid, bcid) = self.unify_actionbinding(acppid, acpp,
                                                                            bcppid, bcpp,
                                                                            service, action,
                                                                            aid, abinding,
                                                                            bid, bbinding,
                                                                            atype)
                    logging.info("Successfully unified {}-{}  ({} {}) to {}: {} {} {}".format(service, action,
                                                                                              acppid, aid,
                                                                                              bcppid, bid,
                                                                                              acid, bcid))

                    # Properties
                    self.unify_properties(aid, abinding, bid, bbinding, actionbinding)

                    action_identifiers.append((acppid, aid, bcppid, bid))
                    actions.append(action)

                    self.record_dependency((acppid, aid, bcppid, bid),
                                           'deliverychannel',
                                           (acppid, acid, bcppid, bcid))

                    acpachannelid = lxml.etree.SubElement(actionbinding, cppa('ChannelId'))
                    acpachannelid.text = self.cppaid(acppid, acid, bcppid, bcid)

                    abservicebinding.append(actionbinding)

                else:
                    use = abinding.get('use')
                    logging.info("No match in {} for {}-{} ({})".format(bcppid, service, action,
                                                                        use))
                    if use != 'optional':
                        raise UnificationException("No match in {} for {}-{}".format(bcppid, service, action))

        except UnificationException as e:
            logging.info("Send_Receive exception: {}".format(e.value))
            raise
        else:
            return action_identifiers, actions

    def check_action_replyto(self, service, action, areplyTo, bbinding, aservicebinding, bservicebinding):
        breplyTo = bbinding.get('replyTo')

        if areplyTo is None and breplyTo is not None \
            or areplyTo is not None and breplyTo is None:
            raise UnificationException('Bindings {} {} inconsistent for replyTo presence'.format(service,
                                                                                                 action))
        if areplyTo is not None and breplyTo is not None:
            arsendbinding = aservicebinding.xpath('child::cppa:ActionBinding[@id="{}"]'.format(areplyTo),
                                                  namespaces=NSMAP)[0]
            brsendbinding = bservicebinding.xpath('child::cppa:ActionBinding[@id="{}"]'.format(breplyTo),
                                                  namespaces=NSMAP)[0]
            araction = arsendbinding.get('action')
            braction = brsendbinding.get('action')

            if araction != braction:
                raise UnificationException('Bindings {} replyTo to different actions {} {}'.format(service,
                                                                                                   araction,
                                                                                                   braction))

    def check_b_servicebinding(self, covered_actions, bservicebinding):
        b_abindingL = bservicebinding.xpath('child::cppa:ActionBinding',
                                            namespaces=NSMAP)
        for b_abinding in b_abindingL:
            action = b_abinding.get('action')
            if action in covered_actions:
                logging.debug('{} found in covered action list'.format(action))
            else:
                use = b_abinding.get('use')
                if use == 'optional':
                    logging.debug('{} not found in covered action list, but it is optional'.format(action))
                else:
                    raise UnificationException('Required binding for action {} not matched'.format(action))

    def unify_actionbinding(self, acppid, acpp, bcppid, bcpp, service, action,
                            aid, abinding, bid, bbinding, direction):
        logging.info("Merging action bindings {} and {} for {} -- {}".format(aid, bid, service, action))

        # Channels
        achannelids = abinding.xpath('child::cppa:ChannelId/text()', namespaces=NSMAP)
        bchannelids = bbinding.xpath('child::cppa:ChannelId/text()', namespaces=NSMAP)

        last_exception = None

        for (acounter, acid) in enumerate(achannelids):
            for (bcounter, bcid) in enumerate(bchannelids):
                logging.info("Attempt to unify {} #{} and {} #{}".format(acid,
                                                                         acounter,
                                                                         bcid,
                                                                         bcounter))
                abchannelid = (acppid, acid, bcppid, bcid)
                try:
                    logging.info("Attempting to unify channel {} for {}".format(bcounter,
                                                                                abchannelid))
                    self.unify_channels(abchannelid, acpp, bcpp, direction)
                except UnificationException as e:
                    last_exception = e
                    logging.info("Failure to unify {} #{} and {} #{}: {}".format(acid,
                                                                                 acounter,
                                                                                 bcid,
                                                                                 bcounter,
                                                                                 e.value))

                else:
                    logging.info("Successfully unified {} #{} and {} #{}".format(acid,
                                                                                 acounter,
                                                                                 bcid,
                                                                                 bcounter))

                    #self.confirm_included('actionbinding', (acppid, aid, bcppid, bid))
                    return abchannelid
        raise UnificationException('Action bindings {} {} failed to unify: {}'.format(aid,
                                                                                      bid,
                                                                                      last_exception.value))

    def unify_channels(self, abchannelid, acpp, bcpp, direction):
        (acppid, acid, bcppid, bcid) = abchannelid

        cached, result = self.memo(acppid,
                                   acid,
                                   bcppid,
                                   bcid,
                                   self.unify_channels_results,
                                   self.unify_channels_exceptions)
        if cached:
            logging.info("Found cached channel for {} {} and {} {}".format(acppid, acid, bcppid, bcid))
            return result
        try:
            result = self.unify_channels_memo(acpp, bcpp, abchannelid, acid, bcid, direction)
        except UnificationException as e:
            logging.info("Exception unifying channel for {} {} and {} {}: {}".format(acppid, acid,
                                                                                     bcppid, bcid,
                                                                                     e.value))
            self.unify_channels_exceptions[acppid,
                                           acid,
                                           bcppid,
                                           bcid] = e
            raise
        else:
            self.unify_channels_results[acppid,
                                        acid,
                                        bcppid,
                                        bcid] = result
            logging.info("Unified channel for {} {} and {} {}".format(acppid, acid, bcppid, bcid))
            return result

    def unify_channels_memo(self, acpp, bcpp, abchannelid, axid, bxid, direction):
        (acppid, acid, bcppid, bcid) = abchannelid
        logging.info("Unifying channel {} {} {} and {} {} {}".format(acppid, acid, axid, bcppid, bcid, bxid))
        abxid = (acppid, axid, bcppid, bxid)
        try:
            if axid is bxid is None:
                return abxid
            elif axid is None or bxid is None:
                raise UnificationException('Missing channel {} versus {}'.format(axid, bxid))
            else:
                adx = acpp.xpath('descendant::node()[@id="{}"]'.format(axid),
                                 namespaces=NSMAP)[0]
                bdx = bcpp.xpath('descendant::node()[@id="{}"]'.format(bxid),
                                 namespaces=NSMAP)[0]
                if adx.tag != bdx.tag:
                    raise UnificationException('Incompatible channel types {} {}'.format(adx.tag, bdx.tag))
                elif adx.tag not in self.protocolhandlers:
                    raise UnificationException('Unsupported channel type {} {}'.format(adx.tag, bdx.tag))
                else:
                    try:
                        handler = self.protocolhandlers[adx.tag ]
                        abdx = lxml.etree.Element(adx.tag)
                        abdxid = self.cppaid(acppid, axid, bcppid, bxid)
                        abdx.set('id', abdxid)
                        return handler(acpp, bcpp, abxid, adx, bdx, abdx, direction)
                    except UnificationException as e:
                        #exception = str(traceback.format_exc())
                        raise UnificationException('Mismatch in channel for protocol {}: {}'.format(adx.tag,
                                                                                                    e.value))
        except UnificationException as e:
            te = 'Channel unification exception for {}: {}'.format(abchannelid, e.value)
            raise UnificationException(te)

    """
    Channel Bindings
    """
    def unify_channel_descriptions(self, abxid, apb, bpb, binding):
        (acppid, axid, bcppid, bxid) = abxid
        description = lxml.etree.SubElement(binding, cppa('Description'))
        description.text = 'Channel formed from {} ({}) in {} and {} ({}) in {}'.format(apb.get('id'),
                                                                                        get_description_value_if_present(apb),
                                                                                        acppid,
                                                                                        bpb.get('id'),
                                                                                        get_description_value_if_present(bpb),
                                                                                        bcppid)

    """
    Named Channel
    """
    def unify_named_channel(self, acpp, bcpp, abxid, apb, bpb, binding, direction):
        (acppid, axid, bcppid, bxid) = abxid

        self.unify_channel_descriptions(abxid, apb, bpb, binding)
        self.unify_simple_subelement(apb, bpb, binding, 'cppa', 'ChannelName')
        self.unify_simple_subelement(apb, bpb, binding, 'cppa', 'SigningCertificateRef',
                                     strictelements=False, required=False)
        self.unify_simple_subelement(apb, bpb, binding, 'cppa', 'EncryptionCertificateRef',
                                     strictelements=False, required=False)

        self.unify_signing_cert_and_anchor(acppid, acpp, bcppid, bcpp, apb, bpb, direction)
        self.unify_encryption_cert_and_anchor(acppid, acpp, bcppid, bcpp, apb, bpb, direction)

        atid = apb.get('transport')
        btid = bpb.get('transport')
        self.unify_transport(acppid, acpp,
                             bcppid, bcpp,
                             atid, btid,
                             direction)

        self.record_dependency(abxid, 'transport', (acppid, atid, bcppid, btid))
        abtid = self.cppaid(acppid, atid, bcppid, btid)
        binding.set('transport', abtid)

        # to do:   match Params
        return binding

    """
    EDIINT
    """
    def unify_ediint_channel(self, acpp, bcpp, abxid, apb, bpb, binding, direction):
        (acppid, axid, bcppid, bxid) = abxid
        self.unify_channel_descriptions(abxid, apb, bpb, binding)
        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding, 'cppa', 'Signature',
                                      self.unify_signature, False, direction)
        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding, 'cppa', 'Encryption',
                                      self.unify_encryption, False, direction)

        atid = apb.get('transport')
        btid = bpb.get('transport')
        self.unify_transport(acppid, acpp,
                             bcppid, bcpp,
                             atid, btid,
                             direction)

        self.record_dependency(abxid, 'transport', (acppid, atid, bcppid, btid))
        abtid = self.cppaid(acppid, atid, bcppid, btid)
        binding.set('transport', abtid)
        return binding

    """
    ebMS2
    """
    def unify_ebms2_channel(self, acpp, bcpp, abxid, apb, bpb, binding, direction):
        (acppid, acid, bcppid, bcid) = abxid
        logging.info("Unifying ebMS2Channel for {} {}".format(acid, bcid))
        self.unify_as_response(acid, apb, bcid, bpb, binding)
        self.unify_channel_descriptions(abxid, apb, bpb, binding)
        self.unify_transport_elements(acppid, acpp, bcppid, bcpp, apb, bpb,
                                      abxid, binding, direction)

        self.unify_package_elements(acppid, acpp, bcppid, bcpp, apb, bpb,
                                    abxid, binding, direction)
        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding,
                                      'cppa', 'ErrorHandling',
                                      self.unify_error_handling, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding,
                                      'cppa', 'ReceiptHandling',
                                      self.unify_receipt_handling, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding,
                                      'cppa', 'ebMS2ReliableMessaging',
                                      self.unify_ebms2_reliable_messaging, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding,
                                      'cppa', 'ebMS2SecurityBinding',
                                      self.unify_ebms2_security_binding, False, direction)

        return binding

    def unify_ebms2_reliable_messaging(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        unify_atts(ael, bel, abel, strictatts=False)
        self.unify_complex_subelement(acpp, bcpp, abxid, ael, bel, abel,
                                      'cppa', 'DuplicateHandling',
                                      self.unify_duplicate_handling, False)
        self.unify_persist_duration(acpp, bcpp, abxid, ael, bel, abel, direction)
        self.unify_retry_handling(acpp, bcpp, abxid, ael, bel, abel, direction)


    def unify_ebms2_security_binding(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'Signature',
                                      self.unify_signature, False, direction)
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'Encryption',
                                      self.unify_encryption, False, direction)

    """
    Web Services
    """
    def unify_ws_channel(self, acpp, bcpp, abxid, apb, bpb, binding, direction):
        (acppid, axid, bcppid, bxid) = abxid
        self.unify_channel_descriptions(abxid, apb, bpb, binding)
        self.unify_simple_subelement(apb, bpb, binding, 'cppa', 'SOAPVersion')
        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding,
                                      'cppa', 'WSSecurityBinding',
                                      self.unify_ws_security, False, direction)
        return binding



    """
    Transport Channels
    """
    def unify_transport_channel(self, acpp, bcpp, abxid, apb, bpb, binding, direction):
        (acppid, acid, bcppid, bcid) = abxid
        self.unify_transport_elements(acppid, acpp, bcppid, bcpp, apb, bpb,
                                      abxid, binding, direction)
        self.unify_channel_descriptions(abxid, apb, bpb, binding)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, binding, 'cppa', 'RequestChannelID',
                                      self.unify_request_channel_id, False, direction)

        return binding

    def unify_request_channel_id(self, acpp, bcpp, abxid, arerc, brerc, abrerc, direction):
        (acppid, axid, bcppid, bxid) = abxid
        logging.info('unify_RequestChannelId for {} {}'.format(abxid, arerc))
        arercid = arerc.text
        brercid = brerc.text
        self.unify_channels((acppid, arercid, bcppid, brercid), acpp, bcpp, None)
        logging.info("Unified RequestChannelId {} {}".format(arercid, brercid))
        abrerc.text = self.cppaid(acppid, arercid, bcppid, brercid)
        self.record_dependency(abxid, 'deliverychannel', (acppid, arercid, bcppid, brercid))

    """
    ebMS3 and AS4
    """
    def unify_ebms3_channel(self, acpp, bcpp, abxid, apb, bpb, ebmsbinding, direction):
        (acppid, acid, bcppid, bcid) = abxid

        self.unify_as_response(acid, apb, bcid, bpb, ebmsbinding)
        self.unify_channel_descriptions(abxid, apb, bpb, ebmsbinding)
        logging.info("Unifying ebMS3Channel for {} {}".format(acid, bcid))

        self.unify_mpc(abxid, apb, bpb, ebmsbinding, direction)

        self.unify_simple_subelement(apb, bpb, ebmsbinding, 'cppa', 'SOAPVersion')

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, ebmsbinding,
                                      'cppa', 'WSSecurityBinding',
                                      self.unify_ws_security, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, ebmsbinding,
                                      'cppa', 'AS4ReceptionAwareness',
                                      self.unify_as4_reception_awareness, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, ebmsbinding,
                                      'cppa', 'ErrorHandling',
                                      self.unify_error_handling, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, ebmsbinding,
                                      'cppa', 'ReceiptHandling',
                                      self.unify_receipt_handling, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, ebmsbinding,
                                      'cppa', 'PullChannelId',
                                      self.unify_pull_channel_id, False, direction)

        self.unify_complex_subelement(acpp, bcpp, abxid, apb, bpb, ebmsbinding,
                                      'cppa', 'AlternateChannel',
                                      self.unify_alternate_channel_id, False, direction)

        self.unify_transport_elements(acppid, acpp, bcppid, bcpp, apb, bpb,
                                      abxid, ebmsbinding, direction)

        self.unify_package_elements(acppid, acpp, bcppid, bcpp, apb, bpb,
                                    abxid, ebmsbinding, direction)

        logging.info("Unified ebMS3Channel for {} {}".format(acid, bcid))
        return ebmsbinding

    def unify_mpc(self, abxid, apb, bpb, ebmsbinding, direction):
        (acppid, acid, bcppid, bcid) = abxid
        logging.info('Unify MPC for {}, {}'.format(acid, bcid))
        for mpcatt in ['mpc', 'submpcext']:
            ampc = apb.get(mpcatt)
            bmpc = bpb.get(mpcatt)
            if ampc == bmpc is None:
                pass
            elif ampc == bmpc:
                # MPC specified on both sides with same value:  reuse value
                ebmsbinding.set(mpcatt, ampc)
            elif ampc is not None and bmpc is not None and ampc != bmpc:
                # MPC specified on both sides with conflicting value: unification fails
                raise UnificationException('Incompatible (sub)MPC {}-{} versus {}-{}'.format(acid,
                                                                                             ampc,
                                                                                             bcid,
                                                                                             bmpc))
            else:
                # The MPC is specified on one side only
                a_as_response = apb.get('asResponse')
                b_as_response = bpb.get('asResponse')
                logging.info(' {} {} {}'.format(a_as_response, b_as_response, direction))
                if direction == 'send' and (a_as_response == "1" or a_as_response == "true"):
                    # Message is transmitted over backchannel of a Pull request
                    if ampc is not None and bmpc is None:
                        ebmsbinding.set(mpcatt, ampc)
                    else:
                        raise UnificationException('Pull client cannot set (sub)MPC for server {} {}'.format(acid,
                                                                                                             bcid))
                elif direction == 'receive' and (b_as_response == "1" or b_as_response == "true"):
                    # Message is transmitted over backchannel of a Pull request
                    if ampc is None and bmpc is not None:
                        ebmsbinding.set(mpcatt, bmpc)
                        logging.info('D')
                    else:
                        logging.info('E')
                        raise UnificationException('Pull client cannot set MPC for server {} {}'.format(acid,
                                                                                                        bcid))
                else:
                    logging.info('F')
                    raise UnificationException('MPC mismatch for {}, {}: {} vs {} '.format(acid,
                                                                                           bcid,
                                                                                           ampc,
                                                                                           bmpc))

    def unify_as_response(self, aid, abinding, bid, bbinding, abbinding):
        aval = abinding.get('asResponse')
        bval = bbinding.get('asResponse')
        if aval == bval:
            if (bval == 'true' or bval == "1"):
                abbinding.set('asResponse', 'true')
        elif (aval == 'true' and bval == '1') or (bval == 'true' and aval == '1'):
            abbinding.set('asResponse', 'true')
        elif (aval == 'false' and bval == '0') or (bval == 'false' and aval == '0'):
            # donothing, default is false
            pass
        elif aval is None:
            if bval == 'false' or bval == "0":
                # donothing, default is false
                pass
            else:
                raise UnificationException('Channels {} {} inconsistent for asResponse'.format(aid,
                                                                                               bid))

    """
    WS-Security
    """
    def unify_ws_security(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        #(acppid, axid, bcppid, bxid) = abxid
        self.unify_simple_subelement(asec, bsec,security, 'cppa', 'WSSVersion', required=False)
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'Signature',
                                      self.unify_signature, False, direction)
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'Encryption',
                                      self.unify_encryption, False, direction)
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'UserAuthentication',
                                      self.unify_user_authentication, False, direction)

    def unify_signature(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        (acppid, axid, bcppid, bxid) = abxid
        self.unify_simple_subelement(asec, bsec,security, 'cppa', 'SignatureAlgorithm', required=False,
                                     intersectifmultiple=True, strictelements=False)
        self.unify_simple_subelement(asec, bsec,security, 'cppa', 'DigestAlgorithm', required=False,
                                     intersectifmultiple=True, strictelements=False)
        self.unify_simple_subelement(asec, bsec,security, 'cppa', 'SigningCertificateRef', required=False,
                                     strictelements=False, intersectifmultiple=True)
        #self.unify_boolean_subelement(asec, bsec,security, 'cppa', 'SignElements', required=False,
        #                              strictelements=True)
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'SignElements',
                                      self.unify_sign_elements, False, direction)
        self.unify_boolean_subelement(asec, bsec,security, 'cppa', 'SignAttachments', required=False,
                                      strictelements=True)
        self.unify_boolean_subelement(asec, bsec,security, 'cppa', 'SignExternalPayloads',
                                      required=False, strictelements=True)

        self.unify_signing_cert_and_anchor(acppid, acpp, bcppid, bcpp, asec, bsec, direction)
        self.unify_encryption_cert_and_anchor(acppid, acpp, bcppid, bcpp, asec, bsec, direction)

    def unify_sign_elements(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        self.unify_expressions(asec, bsec, security)

    def unify_encryption(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        (acppid, axid, bcppid, bxid) = abxid
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'KeyEncryption',
                                      self.unify_key_encryption, False, direction)
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'DataEncryption',
                                      self.unify_data_encryption, False, direction)
        self.unify_simple_subelement(asec, bsec, security, 'cppa', 'EncryptionCertificateRef',
                                     strictelements=False, required=False)

        self.unify_encryption_cert_and_anchor(acppid, acpp, bcppid, bcpp, asec, bsec, direction)

    def unify_key_encryption(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        self.unify_simple_subelement(asec, bsec,security,
                                     'cppa', 'EncryptionAlgorithm',
                                     required=False,
                                     intersectifmultiple=True, strictelements=False)

    def unify_data_encryption(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        self.unify_simple_subelement(asec, bsec,security,
                                     'cppa', 'EncryptionAlgorithm',
                                     required=False,
                                     intersectifmultiple=True, strictelements=False)
        self.unify_complex_subelement(acpp, bcpp, abxid, asec, bsec, security,
                                      'cppa', 'EncryptElements',
                                      self.unify_encrypt_elements, False, direction)
        self.unify_boolean_subelement(asec, bsec,security,
                                      'cppa', 'EncryptAttachments', required=False,
                                      strictelements=True)
        self.unify_boolean_subelement(asec, bsec,security,
                                      'cppa', 'EncryptExternalPayloads', required=False,
                                      strictelements=True)

    def unify_encrypt_elements(self, acpp, bcpp, abxid, asec, bsec, security, direction):
        self.unify_expressions(asec, bsec, security)

    def unify_expressions(self, asec, bsec, security):
        #(acppid, axid, bcppid, bxid) = abxid
        a_expressions_list = sorted(asec.xpath('//cppa:Expression/text()',
                                               namespaces=NSMAP))
        b_expressions_list = sorted(bsec.xpath('//cppa:Expression/text()',
                                               namespaces=NSMAP))
        if len(a_expressions_list) != len(b_expressions_list):
            return UnificationException('Unequal number of expression in {} {}'.format(acppid,
                                                                                       bcppid))
        else:
            for counter, a_expr in enumerate(a_expressions_list):
                b_expr = b_expressions_list[counter]
                if a_expr != b_expr:
                    raise UnificationException('Mismatch in expression: {} {}'.format(a_expr,
                                                                                      b_expr))
                else:
                    expression = lxml.etree.SubElement(security, cppa('Expression'))
                    expression.text = a_expr



    """
    Reliable Messaging
    """
    def unify_as4_reception_awareness(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        self.unify_complex_subelement(acpp, bcpp, abxid, ael, bel, abel,
                                      'cppa', 'DuplicateHandling',
                                      self.unify_duplicate_handling, False)
        self.unify_retry_handling(acpp, bcpp, abxid, ael, bel, abel, direction)

    def unify_duplicate_handling(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        (acppid, axid, bcppid, bxid) = abxid
        self.unify_boolean_subelement(ael, bel,abel, 'cppa', 'DuplicateElimination', required=True,
                                      strictelements=False)
        self.unify_persist_duration(acpp, bcpp, abxid, ael, bel, abel, direction)

    def unify_persist_duration(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        """
        The PersistDuration of the receiver is used
        """
        (acppid, axid, bcppid, bxid) = abxid
        if direction == "send":
            self.unify_persist_duration_send(acppid, bcppid, ael, bel, abel)
        else:
            self.unify_persist_duration_send(acppid, bcppid, bel, ael, abel)

    def unify_persist_duration_send(self, acppid, bcppid, ael, bel, abel):
        b_persistdurationl = bel.xpath('child::cppa:PersistDuration',
                                       namespaces=NSMAP)
        if len(b_persistdurationl) > 0:
            abel.append(self.c14n(deepcopy(b_persistdurationl[0])))

    def unify_retry_handling(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        """
        Retries are handled by the sender, so the configuration for the CPA is
        based on the configuration of the sender.
        @@@ for consideration:  add checks that the last possible retry is within
        the persist duration interval
        """
        (acppid, axid, bcppid, bxid) = abxid
        if direction == "send":
            self.unify_retry_handling_send(acppid, bcppid, ael, bel, abel)
        else:
            self.unify_retry_handling_send(acppid, bcppid, bel, ael, abel)

    def unify_retry_handling_send(self, acppid, bcppid, ael, bel, abel):
        a_RetryHandlingL = ael.xpath('child::cppa:RetryHandling',
                                     namespaces=NSMAP)
        if len(a_RetryHandlingL) > 0:
            abel.append(self.c14n(a_RetryHandlingL[0]))

    """
    Error Handling
    """
    def unify_error_handling(self, acpp, bcpp, abxid, ael, bel, parent, direction):
        logging.info("Unifying ErrorHandling for {}".format(ael))

        self.unify_boolean_subelement(ael, bel, parent, 'cppa', 'ProcessErrorNotifyConsumer',
                                      required = False,
                                      strictelements = False)
        self.unify_boolean_subelement(ael, bel, parent, 'cppa', 'DeliveryFailuresNotifyProducer',
                                      required = False,
                                      strictelements=False)
        self.unify_boolean_subelement(ael, bel, parent, 'cppa', 'ProcessErrorNotifyProducer',
                                      required=False,
                                      strictelements=False)

        self.unify_complex_subelement(acpp, bcpp, abxid, ael, bel, parent, 'cppa', 'ReceiverErrorsReportChannelId',
                                      self.unify_receiver_errors_report_channel_id, False, direction)

    def unify_receiver_errors_report_channel_id(self, acpp, bcpp, abxid, arerc, brerc, abrerc, direction):
        (acppid, axid, bcppid, bxid) = abxid
        logging.info('unify_ReceiverErrorsReportChannelId for {} {}'.format(abxid, arerc))
        arercid = arerc.text
        brercid = brerc.text

        logging.info("Attempting to unify ReceiverErrorsReport channels {} with {}".format(arercid, brercid))
        self.unify_channels((acppid, arercid, bcppid, brercid), acpp, bcpp, None)
        logging.info("Unified ReceiverErrorsReportChannelId {} {}".format(arercid, brercid))
        abrerc.text = self.cppaid(acppid, arercid, bcppid, brercid)

        self.record_dependency(abxid, 'deliverychannel', (acppid, arercid, bcppid, brercid))

    """
    Receipt Handling
    """
    def unify_receipt_handling(self, acpp, bcpp, abxid, ael, bel, parent, direction):
        logging.info("Unifying ReceiptHandling for {}".format(ael))

        self.unify_simple_subelement(ael, bel, parent, 'cppa', 'ReceiptFormat',
                                     required=False, strictelements=True,
                                     intersectifmultiple=False)

        self.unify_complex_subelement(acpp, bcpp, abxid, ael, bel, parent, 'cppa', 'ReceiptChannelId',
                                      self.unify_receipt_channel_id, False, direction)

    def unify_receipt_channel_id(self, acpp, bcpp, abxid, arerc, brerc, abrerc, direction):
        (acppid, axid, bcppid, bxid) = abxid
        logging.info('unify_ReceiptChannelId for {} {}'.format(abxid, arerc))
        arercid = arerc.text
        brercid = brerc.text

        self.unify_channels((acppid, arercid, bcppid, brercid), acpp, bcpp, None)
        logging.info("Unified ReceiptChannelId {} {}".format(arercid, brercid))
        abrerc.text = self.cppaid(acppid, arercid, bcppid, brercid)

        self.record_dependency(abxid, 'deliverychannel', (acppid, arercid, bcppid, brercid))

    """
    self.unify_pull_channel_id
    """
    def unify_pull_channel_id(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        (acppid, axid, bcppid, bxid) = abxid
        logging.info('unify_pull_channel_id for {} {}'.format(abxid, ael))
        apullchannelid = ael.text
        bpullchannelid = bel.text

        logging.info("Attempting to unify Pull channels {} and {}".format(apullchannelid,
                                                                          bpullchannelid))
        self.unify_channels((acppid, apullchannelid, bcppid, bpullchannelid), acpp, bcpp, None)
        logging.info("Unified PullChannelId {} {}".format(apullchannelid,
                                                          bpullchannelid))
        abel.text = self.cppaid(acppid, apullchannelid, bcppid, bpullchannelid)

        self.record_dependency(abxid, 'deliverychannel', (acppid,
                                                         apullchannelid,
                                                         bcppid,
                                                         bpullchannelid))

    """
    self.unify_alternate_channel_id
    """
    def unify_alternate_channel_id(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        (acppid, axid, bcppid, bxid) = abxid
        logging.info('unify_alternate_channel_id for {} {}'.format(abxid, ael))
        aaltchannelid = ael.text
        baltchannelid = bel.text

        logging.info("Attempting to unify Alternate channels {} and {}".format(aaltchannelid,
                                                                               baltchannelid))
        self.unify_channels((acppid, aaltchannelid, bcppid, baltchannelid), acpp, bcpp, None)
        logging.info("Unified AlternateChannelId {} {}".format(aaltchannelid,
                                                          baltchannelid))
        abel.text = self.cppaid(acppid, aaltchannelid, bcppid, baltchannelid)

        self.record_dependency(abxid, 'deliverychannel', (acppid,
                                                         aaltchannelid,
                                                         bcppid,
                                                         baltchannelid))

    """
    Certificates
    """
    def unify_signing_cert_and_anchor(self, acppid, acpp, bcppid, bcpp, acppel, bcppel, direction):
        if direction == "send":
            self.unify_signing_cert_and_anchor_send(acppid, acpp, bcppid, bcpp, acppel, bcppel)
        else:
            self.unify_signing_cert_and_anchor_send(bcppid, bcpp, acppid, acpp, bcppel, acppel)

    def unify_signing_cert_and_anchor_send(self, acppid, acpp, bcppid, bcpp, acppel, bcppel):
        a_signing_certL = acppel.xpath('child::cppa:SigningCertificateRef',
                                       namespaces=NSMAP)
        b_signing_anchorL = bcppel.xpath('child::cppa:SigningTrustAnchorRef',
                                         namespaces=NSMAP)
        if len(a_signing_certL) == 1 and len(b_signing_anchorL) == 1:
            signingcertid = a_signing_certL[0].get('certId')
            banchorid = b_signing_anchorL[0].get('certId')
            logging.info('Checking if cert {} matches anchors {}'.format(signingcertid,
                                                                         banchorid))
            acert = acpp.xpath('cppa:PartyInfo/cppa:Certificate[@id="{}"]'.format(signingcertid),
                               namespaces=NSMAP)[0]
            banchor = bcpp.xpath('cppa:PartyInfo/cppa:TrustAnchor[@id="{}"]'.format(banchorid),
                                 namespaces=NSMAP)[0]
            ax509certL = acert.xpath('descendant-or-self::ds:X509Certificate',
                                     namespaces=NSMAP)
            rootfound = False
            if len(ax509certL) > 0:
                ax509rootcert = remove_all_whitespace(ax509certL[-1].text)
                logging.debug('Root cert is {} ... {} (len: {})'.format(ax509rootcert[0:6],
                                                                        ax509rootcert[-6:],
                                                                        len(ax509rootcert)))

                for b_anchor_ref in banchor.xpath('cppa:AnchorCertificateRef',
                                               namespaces=NSMAP):
                    b_anchor_certid = b_anchor_ref.get('certId')
                    if check_x509_data_content(signingcertid, ax509rootcert, b_anchor_certid, bcpp):
                        rootfound = True
                if not rootfound:
                    for embedded_cert in banchor.xpath('cppa:Certificate', namespaces=NSMAP):
                        certid = embedded_cert.get('id')
                        if check_x509_data_content(signingcertid, ax509rootcert, certid, bcpp):
                            rootfound = True

            if not rootfound:
                raise UnificationException('Cert {} does not match a root cert in {}'.format(signingcertid,
                                                                                                banchorid))
        else:
            logging.info('No signing anchor/cert specified')

    def unify_encryption_cert_and_anchor(self, acppid, acpp, bcppid, bcpp, acppel, bcppel, direction):
        if direction == "send":
            self.unify_encryption_cert_and_anchor_send(acppid, acpp, bcppid, bcpp, acppel, bcppel)
        else:
            self.unify_encryption_cert_and_anchor_send(bcppid, bcpp, acppid, acpp, bcppel, acppel)

    def unify_encryption_cert_and_anchor_send(self, acppid, acpp, bcppid, bcpp, acppel, bcppel):
        a_encryption_anchorL = acppel.xpath('child::cppa:EncryptionTrustAnchorRef',
                                            namespaces=NSMAP)
        b_encryption_certL = bcppel.xpath('child::cppa:EncryptionCertificateRef',
                                          namespaces=NSMAP)
        if len(a_encryption_anchorL) == 1 and len(b_encryption_certL) == 1:
            aanchorid = a_encryption_anchorL[0].get('certId')
            encryptioncertid = b_encryption_certL[0].get('certId')
            logging.info('Checking if cert {} matches anchors {}'.format(encryptioncertid,
                                                                         aanchorid))

            aanchor = acpp.xpath('cppa:PartyInfo/cppa:TrustAnchor[@id="{}"]'.format(aanchorid),
                                 namespaces=NSMAP)[0]
            bcert = bcpp.xpath('cppa:PartyInfo/cppa:Certificate[@id="{}"]'.format(encryptioncertid),
                               namespaces=NSMAP)[0]

            bx509certl = bcert.xpath('descendant-or-self::ds:X509Certificate',
                                     namespaces=NSMAP)
            if len(bx509certl) > 0:
                bx509rootcert = remove_all_whitespace(bx509certl[-1].text)
                logging.debug('Root cert is {} ... {} (len: {})'.format(bx509rootcert[0:6],
                                                                        bx509rootcert[-6:],
                                                                        len(bx509rootcert)))
                rootfound = False
                for a_anchor_ref in aanchor.xpath('cppa:AnchorCertificateRef',
                                               namespaces=NSMAP):
                    a_anchor_certid = a_anchor_ref.get('certId')
                    if check_x509_data_content(encryptioncertid, bx509rootcert, a_anchor_certid, acpp):
                        rootfound = True
                if not rootfound:
                    for embedded_cert in aanchor.xpath('cppa:Certificate', namespaces=NSMAP):
                        certid = embedded_cert.get('id')
                        if check_x509_data_content(encryptioncertid, bx509rootcert, certid, acpp):
                            rootfound = True

                """
                bx509rootcert = bx509certl[-1].text

                bx509rootcert = remove_all_whitespace(bx509certl[-1].text)
                logging.debug('Root cert is {} ... {} (len: {})'.format(bx509rootcert[0:6],
                                                                        bx509rootcert[-6:],
                                                                        len(bx509rootcert)))

                rootfound = False

                for a_anchor_ref in aanchor.xpath('cppa:AnchorCertificateRef',
                                               namespaces=NSMAP):
                    a_anchor_certid = a_anchor_ref.get('certId')
                    a_anchor_cert = acpp.xpath('descendant::cppa:Certificate[@id="{}"]'.format(a_anchor_certid),
                                               namespaces=NSMAP)[0]
                    a_anchor_cert_data = a_anchor_cert.xpath('descendant::ds:X509Certificate/text()',
                                                             namespaces=NSMAP)[0]
                    a_anchor_cert_data = remove_all_whitespace(a_anchor_cert_data)

                    logging.debug('Comparing against {} {} ... {} (len: {})'.format(a_anchor_certid,
                                                                                    a_anchor_cert_data[0:6],
                                                                                    a_anchor_cert_data[-6:],
                                                                                    len(a_anchor_cert_data)))
                    if str(bx509rootcert) == str(a_anchor_cert_data):
                        logging.info('Referenced X509Certificate found in anchor {} cert {}'.format(a_anchor_ref,
                                                                                                    a_anchor_certid))


                        rootfound = True

                """
                if not rootfound:
                    raise UnificationException('Cert {} does not match a root cert in {}'.format(encryptioncertid,
                                                                                                 aanchorid))

        else:
            logging.info('No encryption anchor/cert specified')

    """
    User Authentication

    A username and password are generated as part of CPA formation
    """

    def unify_user_authentication(self, acpp, bcpp, abxid, ael, bel, abel, direction):
        (acppid, aelid, bcppid, belid) = abxid
        usernameel = lxml.etree.SubElement(abel, cppa('Username'))
        usernameel.text = create_username(acppid, aelid, bcppid, belid)
        passwordel = lxml.etree.SubElement(abel, cppa('Password'))
        passwordel.text = create_random_password()
        self.unify_boolean_subelement(ael, bel, abel, 'cppa', 'Digest', required=False)
        self.unify_boolean_subelement(ael, bel, abel, 'cppa', 'Nonce', required=False)
        self.unify_boolean_subelement(ael, bel, abel, 'cppa', 'Created', required=False)

    """
    Transport
    """
    def unify_transport_elements(self, acppid, acpp, bcppid, bcpp, apb, bpb, abxid, binding,
                                 direction):
        atid = apb.get('transport')
        btid = bpb.get('transport')
        if atid is not None and btid is not None:
            self.unify_transport(acppid, acpp,
                                 bcppid, bcpp,
                                 atid,
                                 btid,
                                 direction)

            abtid = self.cppaid(acppid, atid, bcppid, btid)
            binding.set('transport', abtid)
            self.record_dependency(abxid, 'transport', (acppid, atid, bcppid, btid))
        elif (atid is None and btid is not None) or (btid is None and atid is not None):
            raise UnificationException('Element {} and {} inconsistent for transport'.format(apb.get('id'),
                                                                                             bpb.get('id')))

    def unify_transport(self, acppid, acpp, bcppid, bcpp, atid, btid, direction):
        cached, result = self.memo(acppid,
                                   atid,
                                   bcppid,
                                   btid,
                                   self.unify_transport_results,
                                   self.unify_transport_exceptions)
        if cached:
            return result
        try:
            result = self.unify_transport_memo(acppid, acpp, bcppid, bcpp, atid, btid, direction)
        except UnificationException as e:
            self.unify_transport_exceptions[acppid, atid, bcppid, btid] = e
            raise
        else:
            self.unify_transport_results[acppid, atid, bcppid, btid] = result
            return result

    def unify_transport_memo(self, acppid, acpp, bcppid, bcpp, atid, btid, direction):
        try:
            if atid is None and btid is None:
                logging.info("No transport, OK")
                return (acppid, bcppid, atid, btid)
            elif atid is None or btid is None:
                raise Exception('Missing transport {} or {}'.format(atid, btid))
            else:
                atransport = acpp.xpath('descendant::node()[@id="{}"]'.format(atid),
                                        namespaces=NSMAP)[0]
                btransport = bcpp.xpath('descendant::node()[@id="{}"]'.format(btid),
                                        namespaces=NSMAP)[0]
                if atransport.tag != btransport.tag:
                    raise UnificationException('Mismatch in transport type: {} vs {}'.format(atransport.tag,
                                                                                             btransport.tag))
                transportxml = lxml.etree.Element(atransport.tag, id=self.cppaid(acppid,
                                                                                 atransport.get('id'),
                                                                                 bcppid,
                                                                                 btransport.get('id')),
                                                   nsmap=NSMAP)
                description = lxml.etree.SubElement(transportxml, cppa('Description'))
                description.set(xml('lang'),'en')
                description.text = 'Transport formed from {} in {} and {} in {}'.format(atid,
                                                                                        acppid,
                                                                                        btid,
                                                                                        bcppid)

                self.unify_simple_subelement(atransport, btransport, transportxml, 'cppa', 'ClientIPv4',
                                             required=False, strictelements=False,
                                             intersectifmultiple=False)
                self.unify_simple_subelement(atransport, btransport, transportxml, 'cppa', 'ClientIPv6',
                                             required=False, strictelements=False)
                self.unify_simple_subelement(atransport, btransport, transportxml, 'cppa', 'Endpoint',
                                             required=False, strictelements=False)
                self.unify_complex_subelement(acpp, bcpp, (acppid, atid, bcppid, btid), atransport, btransport,
                                              transportxml, 'cppa', 'TransportLayerSecurity',
                                              self.unify_transport_layer_security, False, direction)
                self.unify_complex_subelement(acpp, bcpp, (acppid, atid, bcppid, btid), atransport, btransport,
                                              transportxml, 'cppa', 'UserAuthentication',
                                              self.unify_user_authentication, False, direction)

                return transportxml
        except UnificationException as e:
            raise UnificationException('Transport {} {}: {}'.format(atid, btid, e))

    def unify_transport_layer_security(self, acpp, bcpp, abxid, atls, btls, abtls, direction):

        if direction == "send":
            self.unify_transport_layer_security_send(acpp, bcpp, abxid, atls, btls, abtls)
        else:
            self.unify_transport_layer_security_send(bcpp, acpp, abxid, btls, atls, abtls)

    def unify_transport_layer_security_send(self, acpp, bcpp, abxid, atls, btls, abtls):
        (acppid, axid, bcppid, bxid) = abxid
        logging.info('Unifying TransportLayerSecurity for {} {}'.format(axid,
                                                                        bxid))
        self.unify_simple_subelement(atls, btls, abtls, 'cppa', 'TLSProtocol',
                                     required=False, strictelements=False)
        self.unify_simple_subelement(atls, btls, abtls, 'cppa', 'CipherSuite',
                                     required=False,
                                     intersectifmultiple=True,
                                     strictelements=False)
        self.unify_simple_subelement(atls, btls, abtls, 'cppa', 'ClientCertificateRef',
                                     required=False, strictelements=False)
        self.unify_simple_subelement(atls, btls, abtls, 'cppa', 'ServerCertificateRef',
                                     required=False, strictelements=False)

        self.unify_tls_server_cert_and_anchor_send(acppid, acpp, bcppid, bcpp, atls, btls)
        self.unify_tls_client_cert_and_anchor_send(acppid, acpp, bcppid, bcpp, atls, btls)

    def unify_tls_server_cert_and_anchor_send(self, acppid, acpp, bcppid, bcpp, atls, btls):
        a_server_anchorL = atls.xpath('child::cppa:ServerTrustAnchorRef',
                                            namespaces=NSMAP)
        b_server_certL = btls.xpath('child::cppa:ServerCertificateRef',
                                          namespaces=NSMAP)
        if len(a_server_anchorL) == 1 and len(b_server_certL) == 1:
            aanchorid = a_server_anchorL[0].get('certId')
            server_certid = b_server_certL[0].get('certId')
            logging.info('Checking if cert {} matches anchors {}'.format(server_certid,
                                                                         aanchorid))
            aanchor = acpp.xpath('cppa:PartyInfo/cppa:TrustAnchor[@id="{}"]'.format(aanchorid),
                                 namespaces=NSMAP)[0]
            bcert = bcpp.xpath('cppa:PartyInfo/cppa:Certificate[@id="{}"]'.format(server_certid),
                               namespaces=NSMAP)[0]

            bx509certL = bcert.xpath('descendant-or-self::ds:X509Certificate',
                                     namespaces=NSMAP)
            if len(bx509certL) > 0:
                bx509rootcert = bx509certL[-1].text
                rootfound = False
                for arootcert in aanchor.xpath('cppa:Certificate',
                                               namespaces=NSMAP):
                    arootcertid = arootcert.get('id')
                    if arootcert.xpath('descendant::ds:X509Certificate/text()="{}"'.format(bx509rootcert),
                                       namespaces=NSMAP):
                        logging.info('Referenced X509Certificate found in anchor {} cert {}'.format(aanchorid,
                                                                                                    arootcertid))
                        rootfound = True
                if not rootfound:
                    raise UnificationException('Cert {} does not match a root cert in {}'.format(server_certid,
                                                                                             aanchorid))
        else:
            logging.info('No encryption anchor/cert specified')

    def unify_tls_client_cert_and_anchor_send(self, acppid, acpp, bcppid, bcpp, atls, btls):
        a_client_certL = atls.xpath('child::cppa:ClientCertificateRef',
                                          namespaces=NSMAP)
        b_client_anchorL = btls.xpath('child::cppa:ClientTrustAnchorRef',
                                            namespaces=NSMAP)
        if len(b_client_anchorL) == 1 and len(a_client_certL) == 1:
            banchorid = b_client_anchorL[0].get('certId')
            client_certid = a_client_certL[0].get('certId')
            logging.info('Checking if cert {} matches anchors {}'.format(client_certid,
                                                                         banchorid))
            acert = acpp.xpath('cppa:PartyInfo/cppa:Certificate[@id="{}"]'.format(client_certid),
                               namespaces=NSMAP)[0]
            banchor = bcpp.xpath('cppa:PartyInfo/cppa:TrustAnchor[@id="{}"]'.format(banchorid),
                                 namespaces=NSMAP)[0]

            ax509certL = acert.xpath('descendant-or-self::ds:X509Certificate',
                                     namespaces=NSMAP)
            if len(ax509certL) > 0:
                ax509rootcert = ax509certL[-1].text
                rootfound=False
                for arootcert in banchor.xpath('cppa:Certificate',
                                               namespaces=NSMAP):
                    arootcertid = arootcert.get('id')
                    if arootcert.xpath('descendant::ds:X509Certificate/text()="{}"'.format(ax509rootcert),
                                       namespaces=NSMAP):
                        logging.info('Referenced X509Certificate found in anchor {} cert {}'.format(banchorid,
                                                                                                    arootcertid))
                        rootfound=True
            if not(rootfound):
                raise UnificationException('Cert {} does not match a root cert in {}'.format(client_certid,
                                                                                             banchorid))
        else:
            logging.info('No encryption anchor/cert specified')

    """
    Properties
    """

    def unify_properties(self, aid, abinding, bid, bbinding, actionbinding):
        a_property_list = abinding.xpath('child::cppa:Property',
                                         namespaces=NSMAP)
        b_property_list = bbinding.xpath('child::cppa:Property',
                                         namespaces=NSMAP)
        if len(a_property_list) != len(b_property_list):
            raise UnificationException('Unequal number of properties for {}, {}'.format(aid, bid))
        else:
            xpq = 'child::cppa:Property[@name="{}" and @minOccurs="{}" and @maxOccurs="{}"]'
            for aprop in a_property_list:
                aname = aprop.get('name')
                a_min = aprop.get('minOccurs')
                a_max = aprop.get('maxOccurs')
                bpropl = bbinding.xpath(xpq.format(aname,a_min,a_max),
                                        namespaces=NSMAP)
                if len(bpropl) == 0:
                    raise UnificationException('Mismatch for property {} in {}, {}'.format(aname,
                                                                                           aid,
                                                                                           bid))
                else:
                    actionbinding.append(deepcopy(aprop))

        pass

    """
    Payload Profiles
    """
    def unify_payload_profile(self, acppid, acpp, bcppid, bcpp, aid, bid):
        logging.info('Unifying payload profiles {} {} and {} {}'.format(acppid,
                                                                        aid,
                                                                        bcppid,
                                                                        bid))
        cached, result = self.memo(acppid,
                                   aid,
                                   bcppid,
                                   bid,
                                   self.unify_payload_profile_results,
                                   self.unify_payload_profile_exceptions)
        if cached:
            #return acppid, aid, bcppid, bid
            return result
        try:
            result = self.unify_payload_profile_memo(acppid, acpp, bcppid, bcpp, aid, bid)
        except UnificationException as e:
            self.unify_payload_profile_exceptions[acppid, aid, bcppid, bid] = e
            raise
        else:
            self.unify_payload_profile_results[acppid, aid, bcppid, bid] = result
            #return acppid, aid, bcppid, bid
            return result

    def unify_payload_profile_memo(self, acppid, acpp, bcppid, bcpp, aid, bid):
        try:
            if aid == bid is None:
                logging.info("No payload profile, OK")
                return None
            elif aid is None or bid is None:
                raise Exception('Missing payload profile {} or {}'.format(aid, bid))
            else:
                app = acpp.xpath('descendant::node()[@id="{}"]'.format(aid),
                                        namespaces=NSMAP)[0]
                bpp = bcpp.xpath('descendant::node()[@id="{}"]'.format(bid),
                                        namespaces=NSMAP)[0]

                abpp = lxml.etree.Element(app.tag, id=self.cppaid(acppid,
                                                                  app.get('id'),
                                                                  bcppid,
                                                                  bpp.get('id')),
                                                   nsmap=NSMAP)

                self.unify_payload_parts(acppid, aid, app, bcppid, bid, bpp, abpp)
                return abpp

        except UnificationException as e:
            raise UnificationException('Payload Profile {} {}: {}'.format(aid, bid, e))

    def unify_payload_parts(self, acppid, appid, app, bcppid, bppid, bpp, abpp):
        app_part_list = app.xpath('child::cppa:PayloadPart',
                                  namespaces=NSMAP)
        bpp_part_list = bpp.xpath('child::cppa:PayloadPart',
                                  namespaces=NSMAP)
        alen = len(app_part_list)
        blen = len(bpp_part_list)
        if alen != blen:
            raise UnificationException('Inconsistent number of payload parts {} {}: {}; {} {}: {}'.format(acppid,
                                                                                                          appid,
                                                                                                          alen,
                                                                                                          bcppid,
                                                                                                          bppid,
                                                                                                          blen))
        else:
            for c in range(0,alen):
                appart = app_part_list[c]
                bppart = bpp_part_list[c]
                self.unify_payload_part(acppid, appid, appart, bcppid, bppid, bppart, c, abpp)

    def unify_payload_part(self, acppid, appid, appart, bcppid, bppid, bppart, c, abpp):
        abpart = lxml.etree.Element(appart.tag)
        unify_cardinality(appart, bppart, abpart, '{} {} {}'.format(appid, bppid, c))
        self.unify_simple_subelement(appart, bppart, abpart, 'cppa', 'PartName')
        self.unify_simple_subelement(appart, bppart, abpart, 'cppa', 'MIMEContentType',
                                     required=False)
        self.unify_simple_subelement(appart, bppart, abpart, 'cppa', 'Schema', required=False)
        abpp.append(abpart)

    """
    Packaging
    """
    def unify_package_elements(self, acppid, acpp, bcppid, bcpp,
                               apb, bpb,
                               abxid,
                               ebmsbinding, direction):
        apid = apb.get('package')
        bpid = bpb.get('package')

        if apid is not None and bpid is not None:
            self.unify_package(acppid, acpp,
                               bcppid, bcpp,
                               apid, bpid,
                               abxid,
                               direction)
            abpid = self.cppaid(acppid, apid, bcppid, bpid)
            ebmsbinding.set('package', abpid)
            self.record_dependency(abxid, 'package', (acppid, apid, bcppid, bpid))

    def unify_package(self, acppid, acpp,
                      bcppid, bcpp,
                      apid, bpid,
                      abxid,
                      direction):
        cached, result = self.memo(acppid,
                                   apid,
                                   bcppid,
                                   bpid,
                                   self.unify_package_results,
                                   self.unify_package_exceptions)
        if cached:
            return result
        try:
            result = self.unify_package_memo(acppid, acpp, bcppid, bcpp, apid, bpid, abxid, direction)
        except UnificationException as e:
            self.unify_package_exceptions[acppid, apid, bcppid, bpid] = e
            raise
        else:
            self.unify_package_results[acppid, apid, bcppid, bpid] = result
            return result

    def unify_package_memo(self, acppid, acpp, bcppid, bcpp, apid, bpid, abxid, direction):
        try:
            if apid == bpid is None:
                logging.info("No packaging, OK")
                return None
            elif apid is None or bpid is None:
                raise Exception('Missing package {} or {}'.format(apid, bpid))
            else:
                apackage = acpp.xpath('descendant::node()[@id="{}"]'.format(apid),
                                        namespaces=NSMAP)[0]
                bpackage = bcpp.xpath('descendant::node()[@id="{}"]'.format(bpid),
                                        namespaces=NSMAP)[0]

                if apackage.tag != bpackage.tag:
                    raise UnificationException('Incompatible package types {} {}'.format(apackage.tag,
                                                                                         bpackage.tag))
                elif apackage.tag not in self.packaging_handlers:
                    raise UnificationException('Unsupported package type {} {}'.format(apackage.tag,
                                                                                       bpackage.tag))
                else:
                    try:
                        handler = self.packaging_handlers[apackage.tag]
                        logging.info("Package compatible {} {}".format(apid, bpid))
                        return handler(acpp, acppid, bcpp, bcppid, apackage, bpackage, abxid, direction)
                    except UnificationException as e:
                        raise UnificationException('Mismatch in package {}: {}'.format(apackage.tag,
                                                                                       e))

        except UnificationException as e:
            raise UnificationException('Transport {} {}: {}'.format(apid, bpid, e.value))

    """
    @@@TODO merge the following
    """
    def unify_soap_with_attachments_envelope(self, acpp, acppid, bcpp, bcppid,
                                             apackage, bpackage, abxid, direction):
        swael = lxml.etree.Element(apackage.tag, nsmap=NSMAP)
        self.unify_mime_part_lists(swael, apackage, bpackage, abxid, acpp, bcpp, direction)
        return swael

    def unify_simple_soap_envelope(self, acpp, acppid, bcpp, bcppid, apackage, bpackage,
                                   abxid, direction):
        sel = lxml.etree.Element(apackage.tag, nsmap=NSMAP)
        self.unify_mime_part_lists(sel, apackage, bpackage, abxid, acpp, bcpp, direction)
        return sel

    def unify_mime_envelope(self, acpp, acppid, bcpp, bcppid, apackage, bpackage,
                            abxid, direction):
        sel = lxml.etree.Element(apackage.tag, nsmap=NSMAP)
        self.unify_mime_part_lists(mimepart, apart, bpart, abxid, acpp, bcpp, direction)
        return sel

    def unify_compressed_mime_part(self, apart, bpart, abxid, acpp, bcpp, direction):
        mimepart = lxml.etree.Element(apart.tag, nsmap=NSMAP)
        unify_atts(apart, bpart, mimepart, strictatts=True)
        self.unify_mime_part_lists(mimepart, apart, bpart, abxid, acpp, bcpp, direction)
        return mimepart

    def unify_mime_multipart_related(self, apart, bpart, abxid, acpp, bcpp, direction):
        mimepart = lxml.etree.Element(apart.tag, nsmap=NSMAP)
        unify_atts(apart, bpart, mimepart, strictatts=True)
        self.unify_mime_part_lists(mimepart, apart, bpart, abxid, acpp, bcpp, direction)
        return mimepart

    def unify_simple_mime_part(self, apart, bpart, abxid, acpp, bcpp, direction):
        mimepart = lxml.etree.Element(apart.tag, nsmap=NSMAP)
        aname = apart.get('PartName')
        bname = bpart.get('PartName')
        if aname != bname:
            raise UnificationException('Incompatible PartName {} vs {}'.format(aname,
                                                                               bname))
        else:
            mimepart.set('PartName',aname)
            return mimepart

    def unify_external_payload(self, apart, bpart, abxid, acpp, bcpp, direction):
        mimepart = lxml.etree.Element(apart.tag, nsmap=NSMAP)
        aname = apart.get('PartName')
        bname = bpart.get('PartName')
        if aname != bname:
            raise UnificationException('Incompatible PartName {} vs {}'.format(aname,
                                                                               bname))
        else:
            (acppid, axid, bcppid, bxid) = abxid
            mimepart.set('PartName',aname)
            a_ep_ch_id = apart.xpath('child::cppa:ChannelId/text()',
                                     namespaces=NSMAP)[0]
            b_ep_ch_id = bpart.xpath('child::cppa:ChannelId/text()',
                                     namespaces=NSMAP)[0]
            transportchannelid = (acppid, a_ep_ch_id, bcppid, b_ep_ch_id)
            self.unify_channels(transportchannelid, acpp, bcpp, direction)
            self.record_dependency(abxid, 'deliverychannel', transportchannelid)

            abchannel = lxml.etree.SubElement(mimepart, cppa('ChannelId'))
            abchannel.text = self.cppaid(acppid, a_ep_ch_id, bcppid, b_ep_ch_id)
            return mimepart

    def unify_mime_part_lists(self, parent, apackage, bpackage, abxid, acpp, bcpp, direction):
        apartl = apackage.xpath('child::*[local-name()!="Description"]')
        bpartl = bpackage.xpath('child::*[local-name()!="Description"]')
        alen, blen = len(apartl), len(bpartl)
        if alen != blen:
            raise UnificationException('Mismatch in child count for package: {} {}'.format(alen,
                                                                                           blen))
        else:
            for apart, bpart in zip(apartl, bpartl):
                if apart.tag != bpart.tag:
                    raise UnificationException('Mismatch in child type for package: {} {}'.format(alen,
                                                                                                  blen))
                else:
                    handler = self.mimepart_handlers[apart.tag]
                    parent.append(handler(apart, bpart, abxid, acpp, bcpp, direction))
                    logging.info('### Adding {}'.format(apart))

    """
    Auxiliary functions
    """
    def memo(self, p1, p2, p3, p4, results, exceptions):
        if (p1, p2, p3, p4) in results:
            logging.info("Results cache hit for {} {} {} {}".format(p1, p2, p3, p4))
            return True, results[p1, p2, p3, p4]
        elif (p1, p2, p3, p4) in exceptions:
            logging.info("Exceptions cache hit for {} {}".format(p1, p2, p3, p4))
            raise exceptions[p1, p2, p3, p4]
        else:
            return False, None

    def confirm_included(self, componenttype, id):
        if not componenttype in self.included_components:
            self.included_components[componenttype] = []
        if not id in self.included_components[componenttype]:
            self.included_components[componenttype].append(id)

    def record_dependency(self, source, category, target):
        if not source in self.depends_on:
            self.depends_on[source] = {}
        if not category in self.depends_on[source]:
            self.depends_on[source][category] = [target]
            logging.info("Dependency {} {} {} created".format(source, category,target))
        targetlist = self.depends_on[source][category]
        if target not in targetlist:
            logging.info("Dependency {} {} {} added to list".format(source, category,target))
            targetlist.append(target)
        else:
            logging.info("Dependency {} {} {} already on list".format(source, category,target))

    def unify_simple_subelement(self, ael, bel, abel, childns, childtag,
                                required=True, strictelements=True, strictatts=True,
                                boolean=False,
                                intersectifmultiple=True):
        """
        strictelements:  either both inputs have the subelement or none;  otherwise exceptions
        required:  one of the inputs must have the subelement; otherwise exception (assume strictelements==False)
        strictatts:  if one input has an attribute then the other must have it too with same value
        boolean:  if the value is Boolean
        intersect_if_multiple:  if both inputs may have multiple elements, the unification is
        their intersection if True; if False, there must be a one-to-one unification of subelement
        instances.
        """
        logging.info("Unifying subelement {} for {}".format(childtag, abel.tag))
        try:
            achildL = ael.xpath('child::{}:{}'.format(childns, childtag),
                                namespaces=NSMAP)
            bchildL = bel.xpath('child::{}:{}'.format(childns, childtag),
                                namespaces=NSMAP)

            achildLcount = len(achildL)
            bchildLcount = len(bchildL)

            if strictelements and achildLcount != bchildLcount:
                raise UnificationException('Child count mismatch for {}'.format(childtag))
            elif achildLcount == 0 and bchildLcount > 0:
                for bchild in bchildL:
                    abchild = lxml.etree.Element(ns(NSMAP[childns], childtag),
                                                 nsmap=NSMAP)
                    abchild.text = bchild.text
                    copy_atts(bchild,abchild)
                    abel.append(abchild)
            elif achildLcount >  0 and bchildLcount == 0:
                for achild in achildL:
                    abchild = lxml.etree.Element(ns(NSMAP[childns], childtag),
                                                 nsmap=NSMAP)
                    abchild.text = achild.text
                    copy_atts(achild,abchild)
                    abel.append(abchild)
            elif achildLcount == 1 and bchildLcount == 1:
                abchild = lxml.etree.Element(ns(NSMAP[childns], childtag),
                                             nsmap=NSMAP)
                abchild.text = unify_boolean_or_text(achildL[0],
                                                     bchildL[0],
                                                     boolean)
                unify_atts(achildL[0], bchildL[0],abchild,
                           strictatts=strictatts)
                abel.append(abchild)
            elif achildLcount >= 1 and bchildLcount >= 1:
                if bchildLcount > len(achildL) and not intersectifmultiple:
                    raise UnificationException('Too many {} nodes, {} vs {}'.format(childtag,
                                                                                    len(bchildL),
                                                                                    len(achildL)))
                at_least_one_shared_child = False

                for counter, achild in enumerate(achildL, 1):
                    logging.info("5 {} for {}".format(achild.tag, counter))
                    abchild = lxml.etree.Element(ns(NSMAP[childns], childtag),
                                                 nsmap=NSMAP)

                    bchildmatchfound = False
                    for bchild in bchildL:
                        logging.info("6 {} for {}".format(achild.tag, counter))
                        try:
                            abchild.text = unify_boolean_or_text(achild,
                                                                 bchild,
                                                                 boolean)
                            unify_atts(achild, bchild, abchild,
                                       strictatts=strictatts)
                        except:
                            logging.info("6A {} for {}".format(achild.tag, counter))
                        else:
                            logging.info("6B {} for {}".format(achild.tag, counter))
                            abel.append(abchild)
                            bchildmatchfound = True
                            at_least_one_shared_child = True
                            break

                    # we're here if we did not find a match for achild
                    if not intersectifmultiple and not bchildmatchfound:
                        raise UnificationException('Missing child for {} {}'.format(childtag,
                                                                                    counter))
                if not at_least_one_shared_child:
                    raise UnificationException('Empty intersection for {}'.format(childtag))

            elif required:
                raise UnificationException('Missing child {} {} {}'.format(childtag,
                                                                           achildLcount,
                                                                           bchildLcount))
        except UnificationException as e:
            logging.info("Subelements incompatible for {}: {}".format(childtag, e.value))
            raise
        else:
            logging.info("Subelements compatible for {}".format(childtag))

    def unify_boolean_subelement(self, ael, bel, abel, childns, childtag,
                                 required=True, strictelements=True, strictatts=True):
        return self.unify_simple_subelement(ael, bel, abel, childns, childtag,
                                            required=required,
                                            strictelements=strictelements,
                                            strictatts=strictatts,
                                            boolean=True)

    def unify_complex_subelement(self, acpp, bcpp, idtuple, ael, bel, abel, childns, childtag, handler,
                                 required, direction=None):
        logging.info("Unifying subelement {} for {}".format(childtag, ael.tag))
        try:
            aelementL = ael.xpath('child::{}:{}'.format(childns, childtag),
                                namespaces=NSMAP)
            belementL = bel.xpath('child::{}:{}'.format(childns, childtag),
                                namespaces=NSMAP)
            if required and len(aelementL) == 0 and len(belementL) == 0:
                raise UnificationException('Missing child(ren) {}'.format(childtag))
            elif len(aelementL) != len(belementL):
                raise UnificationException('Mismatch in count for child(ren) {}'.format(childtag))
            elif len(aelementL) == 1 and len(belementL) == 1:
                logging.info('Creating {} element, invoking {}'.format(childtag, handler.func_name))
                abchild = lxml.etree.SubElement(abel,ns(NSMAP[childns], childtag),
                                                nsmap=NSMAP)
                handler(acpp, bcpp, idtuple, aelementL[0], belementL[0], abchild, direction)
                unify_atts(aelementL[0], belementL[0],abchild, strictatts=False)
            elif len(aelementL) == len(belementL) == 0:
                logging.info('Element {} not present'.format(childtag))
            else:
                logging.error('Help .... {} {}'.format(len(aelementL),len(belementL)))
        except UnificationException as e:
            raise
        else:
            logging.info("Subelements compatible for {}".format(childtag))

    def cppaid(self, acppid, acid, bcppid, bcid):
        if (acppid, acid, bcppid, bcid) in self.shortened:
            return self.shortened[acppid, acid, bcppid, bcid]
        else:
            m = hashlib.sha224()
            m.update('{}_{}_{}_{}'.format(acppid,acid, bcppid, bcid))
            longvalue = '_'+base64.b32encode(m.digest())
            for i in range(5, 50):
                short = str(longvalue)[:i]
                if short not in self.collisions:
                    self.shortened[acppid, acid, bcppid, bcid] = short
                    self.collisions[short] = (acppid, acid, bcppid, bcid)
                    return short
                else:
                    logging.error('Collision {} for {} {} {} {}'.format(short,
                                                                        acppid,
                                                                        acid,
                                                                        bcppid,
                                                                        bcid))
                    (a, b, c, d) = self.collisions[short]
                    logging.error('Previous value for {} was {} {} {} {}'.format(short,
                                                                          a,
                                                                          b,
                                                                          c,
                                                                          d))

def check_x509_data_content(anchorid, rootcert, anchor_certid, cpp):
        anchor_cert = cpp.xpath('descendant::cppa:Certificate[@id="{}"]'.format(anchor_certid),
                                namespaces=NSMAP)[0]
        anchor_cert_data = anchor_cert.xpath('descendant::ds:X509Certificate/text()',
                                               namespaces=NSMAP)[0]
        anchor_cert_data = remove_all_whitespace(anchor_cert_data)
        logging.debug('Comparing against {} {} ... {} (len: {})'.format(anchor_certid,
                                                                        anchor_cert_data[0:6],
                                                                        anchor_cert_data[-6:],
                                                                        len(anchor_cert_data)))

        if str(rootcert) == str(anchor_cert_data):
            logging.info('Referenced X509Certificate found in anchor {} cert {}'.format(anchorid,
                                                                                        anchor_certid))
            return True
        else:
            return False



def unify_boolean_or_text(el1, el2, boolean):
    if boolean:
        return unify_boolean(el1, el2)
    else:
        return unify_text(el1, el2)

def unify_text(e1, e2):
    if e1.text == e2.text:
        return e1.text
    else:
        raise UnificationException('{}: {} vs {}'.format(e1.tag, e1.text, e2.text))

def unify_boolean(e1, e2):
    if (e1.text == 'true' or e1.text == 1) and (e2.text == 'true' or e1.text == 1):
        return 'true'
    elif (e1.text == 'false' or e1.text == 0) and (e2.text == 'false' or e1.text == 0):
        return 'false'
    else:
        raise UnificationException('Boolean {}: {} vs {}'.format(e1.tag, e1.text, e2.text))

def unify_atts(ael, bel, abel, strictatts=True):
    for (aside, bside) in [(ael, bel), (bel, ael)]:
        for att in aside.attrib:
            if att in bside.attrib:
                if aside.attrib[att] == bside.attrib[att]:
                    abel.set(att, aside.attrib[att])
                else:
                    raise UnificationException('Attribute {} value mismatch: {} vs {}'.format(att,
                                                                                              aside.attrib[att],
                                                                                              bside.attrib[att]))
            elif strictatts:
                # @@@ not covered yet
                raise UnificationException('Attribute {} missing value in one of the inputs'.format(att))
            else:
                abel.set(att, aside.attrib[att])

def copy_atts(source, target):
    for att in source.attrib:
        target.set(att, source.get(att))

def unify_att(e1, e2, att):
    if not e1.attrib[att] == e2.attrib[att]:
        raise UnificationException('{}/@{}: {} vs {}'.format(e1.tag,
                                                             att,
                                                             e1.attrib[att],
                                                             e2.attrib[att]))
    else:
        return e1.attrib[att]

def unify_cardinality(aelement, belement, abelement, context=''):
    logging.info('Cardinality check for {}'.format(context))

    for att in ['minOccurs', 'maxOccurs']:
        amin = aelement.get(att)
        bmin = belement.get(att)
        if amin == bmin:
            if amin is None:
                pass
            else:
                abelement.set(att, amin)
        if amin != bmin:
            raise UnificationException('Incompatible {} cardinality in {}: {} vs {}'.format(att,
                                                                                            context,
                                                                                            amin,
                                                                                            bmin))
        elif amin is not None:
            abelement.set(att, amin)

def reverse(direction):
    if direction == 'send':
        return 'receive'
    else:
        return 'send'

def cppa(el):
    return '{{{}}}{}'.format(NSMAP['cppa'],el)

def xml(el):
    return '{{{}}}{}'.format(NSMAP['xml'],el)

def ns(ns,el):
    return '{{{}}}{}'.format(ns,el)

def get_description_value_if_present(el):
    descL = el.xpath('child::cppa:Description',
                     namespaces=NSMAP)
    if len(descL)>0:
        return descL[0].text
    else:
        return '-'

def create_username(acppid, aelid, bcppid, belid, len=15):
    m = hashlib.sha224()
    m.update('{}_{}_{}_{}'.format(acppid, aelid, bcppid, belid))
    longvalue = base64.b64encode(m.digest())
    return str(longvalue)[:len]

def create_random_password(len=20):
    return str(uuid.uuid4())[:len]

def remove_all_whitespace(inputstring):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', inputstring)